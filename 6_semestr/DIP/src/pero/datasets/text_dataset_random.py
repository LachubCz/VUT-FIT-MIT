import numpy as np
import threading
import time
import itertools
from datasets.charset import transcriptions_to_labels
from datasets.datasets_helper import sparse_tuples_from_sequences
from datasets.datasets_helper import pad_sequences_and_get_lengths
from datasets.text_dataset import TextDataset


class TextDatasetRandom(TextDataset):
    def __init__(self, max_buffer_size, data_format="TF", transcriptions_file=None, images_path=None,
                 lmdb_database=None, chars=None, max_width=2048, verbose=False, sleep=0.0005, transformer=None,
                 weights=False, alignment=False):
        super().__init__(max_width=max_width, transcriptions_file=transcriptions_file, images_path=images_path,
                         lmdb_database=lmdb_database, chars=chars, verbose=verbose, transformer=transformer,
                         weights=weights, alignment=alignment)
        self.type = 'random'
        self.max_buffer_size = max_buffer_size
        self.data_format = data_format
        self.transcriptions_buffer = self.max_buffer_size * [None]
        self.images_buffer = self.max_buffer_size * [None]
        self.ids_embedding_buffer = self.max_buffer_size * [None]
        self.weights_buffer = self.max_buffer_size * [None]
        self.line_width_buffer = np.zeros(self.max_buffer_size, dtype=np.float32)
        self.next_pos = 0
        self.read_counter = 0
        self.total_lines = 0
        self.rejected_lines = 0
        self.stop_thread = False
        self.buffer_filled = False
        self.lock = threading.Lock()
        self.sleep = sleep
        self.thread = threading.Thread(target=self.loading_thread)
        self.thread.daemon = True
        self.thread.start()
        self.permutation = np.random.permutation(self.max_buffer_size)
        self.use_weights = weights
        self.use_alignments = alignment

    def load_next(self):
        ids_index = self.read_counter % len(self.ids)
        image = self.load_image(ids_index)
        self.read_counter += 1
        self.total_lines += 1
        if image.shape[1] > self.max_width:
            self.rejected_lines += 1
            return

        if not self.use_weights and not self.use_alignments:
            transcription = transcriptions_to_labels(self.from_char, self.to_char, [self.transcriptions[ids_index]])[0]
        elif not self.use_alignments:
            transcription = []
            for item in self.transcriptions[ids_index]:
                transcription.append(transcriptions_to_labels(self.from_char, self.to_char, [item])[0])
        else:
            transcription = self.transcriptions[ids_index]
        id_embedding = self.ids_embedding[ids_index]
        weight = self.weights[ids_index]
        with self.lock:
            self.transcriptions_buffer[self.next_pos] = transcription
            self.images_buffer[self.next_pos] = image
            self.line_width_buffer[self.next_pos] = image.shape[1]
            self.ids_embedding_buffer[self.next_pos] = id_embedding
            self.weights_buffer[self.next_pos] = weight
        self.next_pos = (self.next_pos + 1) % self.max_buffer_size
        if not self.buffer_filled and (self.next_pos == 0 or self.read_counter == len(self.ids)):
            if self.read_counter == len(self.ids):
                self.stop_thread = True
                self.max_buffer_size = self.next_pos
                self.transcriptions_buffer = self.transcriptions_buffer[:self.max_buffer_size]
                self.images_buffer = self.images_buffer[:self.max_buffer_size]
                self.line_width_buffer = self.line_width_buffer[:self.max_buffer_size]
                self.ids_embedding_buffer = self.ids_embedding[:self.max_buffer_size]
                self.weights_buffer = self.weights[:self.max_buffer_size]
                self.permutation = np.random.permutation(self.max_buffer_size)
            self.buffer_filled = True

        if self.buffer_filled:
            time.sleep(self.sleep)

    def loading_thread(self):
        while not self.stop_thread:
            self.load_next()

    def get_batch(self, batch_size, pad_to_max_width=False, tolerance=8):
        if self.permutation.shape[0] < batch_size:
            self.permutation = np.random.permutation(self.max_buffer_size)

        if pad_to_max_width:
            selected = self.permutation[:batch_size]
            self.permutation = self.permutation[batch_size:]
            images = np.zeros([batch_size, self.height, self.max_width, self.channels], dtype=np.uint8)
            with self.lock:
                for img, i in zip(images, selected):
                    padding = (self.max_width - self.images_buffer[i].shape[1]) // 2
                    img[:, padding:padding + self.images_buffer[i].shape[1]] = self.images_buffer[i]
                labels = [self.transcriptions_buffer[x] for x in selected]
                ids_embedding = [self.ids_embedding_buffer[x] for x in selected]
                weights = [self.weights_buffer[x] for x in selected]

        else:
            one_selected = self.permutation[:1]
            self.permutation = self.permutation[1:]
            selected = np.zeros(0)
            with self.lock:
                while selected.shape[0] < batch_size:
                    selected, = np.nonzero(np.abs(self.line_width_buffer - self.line_width_buffer[one_selected]) < tolerance)
                    if tolerance <= 1:
                        tolerance = 2
                    else:
                        tolerance *= 2
                selected = np.random.choice(selected, size=batch_size, replace=False)
                max_width = np.max(self.line_width_buffer[selected])
                max_width = int(np.ceil(max_width / 64) * 64) + 64
                images = np.zeros([batch_size, self.height, max_width, self.channels], dtype=np.uint8)
                for img, i in zip(images, selected):
                    img[:, 32:32+self.images_buffer[i].shape[1]] = self.images_buffer[i]

                labels = [self.transcriptions_buffer[x] for x in selected]
                ids_embedding = [self.ids_embedding_buffer[x] for x in selected]
                weights = [self.weights_buffer[x] for x in selected]

        if self.data_format == "TF":
            seq_lengths = np.full(images.shape[0], images.shape[2] / self.output_subsampling, dtype=np.int32)
            sequences = sparse_tuples_from_sequences(labels)
            return images, sequences, seq_lengths
        elif self.data_format == "TF-dense":
            sequences, seq_lengths = pad_sequences_and_get_lengths(labels, int(images.shape[2] / self.output_subsampling))
            return images, sequences, seq_lengths
        elif self.data_format == "PyTorch":
            images = np.transpose(images, (0, 3, 1, 2))
            if not self.use_weights and not self.use_alignments:
                labels_concatenated = np.concatenate(labels)
                labels_lengths = np.asarray([x.shape[0] for x in labels])
                occurences = np.ones(len(labels))
            elif self.use_weights:
                try:
                    labels_concatenated = np.concatenate(list(itertools.chain(*labels)))
                except:
                    labels_concatenated = np.array([])
                labels_lengths = []
                occurences = np.zeros(len(labels))
                for i, x in enumerate(labels):
                    if len(x) == 0:
                        occurences[i] = 1
                    else:
                        for y in x:
                            labels_lengths.append(y.shape[0])
                            occurences[i] += 1
                labels_lengths = np.asarray(labels_lengths)
                weights = list(itertools.chain(*weights))
            else:
                labels_lengths = []
                for i, label in enumerate(labels):
                    labels[i] = label.toarray()
                    labels_lengths.append(labels[i].shape[0])

                labels_lengths = np.array(labels_lengths)
                max_length = np.max(labels_lengths)
                for i, label in enumerate(labels):
                    new_label = np.zeros((max_length, 512))
                    new_label[:label.shape[0], :] = label
                    for e, item in enumerate(new_label):
                        sum = np.sum(item)
                        if sum != 1:
                            new_label[e, -1] = 1 - sum
                    labels[i] = new_label
                labels = np.array(labels)
                labels_concatenated = np.concatenate(labels, axis=0)
                occurences = np.ones(len(labels))
            return {'images': images, 'labels_concatenated': labels_concatenated, 'labels_lengths': labels_lengths,
                    'labels': labels, 'ids_embedding': ids_embedding, 'weights': weights, 'occurences': occurences}
        else:
            raise Exception(f'Not implemented: "{format}". Possible formats are: TF, TF-dense, PyTorch.')

    def __del__(self):
        while self.thread.isAlive():
            self.stop_thread = True
