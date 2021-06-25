import numpy as np
import threading
from datasets.charset import transcriptions_to_labels
from datasets.datasets_helper import sparse_tuples_from_sequences
from datasets.datasets_helper import pad_sequences_and_get_lengths
from datasets.text_dataset import TextDataset


class TextDatasetSequential(TextDataset):
    def __init__(self, queue, batch_size, data_format="TF", pad_to_max_width=False, transcriptions_file=None, images_path=None,
                 lmdb_database=None, chars=None, max_width=2048, sort=True, verbose=False):
        super().__init__(max_width=max_width, transcriptions_file=transcriptions_file, images_path=images_path,
                         lmdb_database=lmdb_database, chars=chars, verbose=verbose)
        self.type = 'sequential'
        self.thread = None
        self.queue = queue
        self.batch_size = batch_size
        self.data_format = data_format
        self.pad_to_max_width = pad_to_max_width
        self.rejected = 0
        self.sort = sort
        sort_width_container = []
        for ids_index, (id, transcription, id_embedding) in enumerate(zip(self.ids, self.transcriptions, self.ids_embedding)):
            img = self.load_image(ids_index)
            if img.shape[1] <= self.max_width:
                sort_width_container.append((id, transcription, id_embedding, img.shape[1]))
            else:
                self.rejected += 1
        if self.sort:
            sort_width_container = sorted(sort_width_container, key=lambda x: x[-1], reverse=True)

        if verbose:
            print(f"Rejected images {self.rejected}")

        self.ids = [x[0] for x in sort_width_container]
        self.transcriptions = [x[1] for x in sort_width_container]
        self.ids_embedding = [x[2] for x in sort_width_container]
        self.last_image = self.load_image(len(self.ids) - 1)
        self.ids_index = 0
        self.stop_thread = False
        self.start_loading_thread()

    def reset(self):
        self.ids_index = 0
        while self.thread.isAlive():
            self.stop_thread = True
        self.stop_thread = False
        self.start_loading_thread()

    def start_loading_thread(self):
        self.thread = threading.Thread(target=self.loading_thread)
        self.thread.daemon = True
        self.thread.start()

    def loading_thread(self):
        while not self.stop_thread:
            batch = self.create_new_batch()
            self.queue.put(batch)
            if batch['actual_batch_size'] < self.batch_size:
                break

    def get_batch(self):
        return self.queue.get()

    def create_new_batch(self):
        ids = []
        images = []
        transcriptions = []
        ids_embedding = []
        for x in range(self.batch_size):
            id, image, transcription, id_embedding = self.load_next()
            ids.append(id)
            images.append(image)
            transcriptions.append(transcription)
            ids_embedding.append(id_embedding)

        if self.pad_to_max_width:
            images_container = np.zeros([self.batch_size, self.height, self.max_width, self.channels], dtype=np.uint8)
            for img_container, img in zip(images_container, images):
                padding = (self.max_width - img.shape[1]) // 2
                img_container[:, padding:padding + img.shape[1]] = img
            images = images_container

        else:
            if self.sort:
                max_width = images[0].shape[1]
            else:
                widths = [image.shape[1] for image in images]
                max_width = max(widths)
            max_width = int(np.ceil(max_width / 64) * 64) + 64
            images_container = np.zeros([self.batch_size, self.height, max_width, self.channels], dtype=np.uint8)
            for img_container, img in zip(images_container, images):
                img_container[:, 32:32 + img.shape[1]] = img
            images = images_container

        labels = transcriptions_to_labels(self.from_char, self.to_char, transcriptions)
        sequences = sparse_tuples_from_sequences(labels)

        if self.ids_index > len(self.ids) - 1:
            actual_batch_size = self.batch_size - (self.ids_index - len(self.ids))
        else:
            actual_batch_size = self.batch_size

        if self.data_format == "TF":
            seq_lengths = np.full(images.shape[0], images.shape[2] / self.output_subsampling, dtype=np.int32)
            return images, ids, labels, sequences, seq_lengths, actual_batch_size
        elif self.data_format == "TF-dense":
            sequences, seq_lengths = pad_sequences_and_get_lengths(labels, int(images.shape[2] / 4))
            return images, ids, labels, sequences, seq_lengths, actual_batch_size
        elif self.data_format == "PyTorch":
            images = np.transpose(images, (0, 3, 1, 2))
            labels_concatenated = np.concatenate(labels)
            labels_lengths = np.asarray([x.shape[0] for x in labels])
            weights = np.ones(len(labels))
            occurences = np.ones(len(labels))
            return {'images': images, 'ids': ids, 'labels_concatenated': labels_concatenated,
                    'labels_lengths': labels_lengths, 'labels': labels, 'actual_batch_size': actual_batch_size,
                    'ids_embedding': ids_embedding, 'transcriptions': transcriptions, 'weights': weights,
                    'occurences': occurences}
        else:
            raise Exception(f'Not implemented: "{format}". Possible formats are: TF, TF-dense, PyTorch.')

    def load_next(self):
        if self.ids_index > len(self.ids) - 1:
            self.ids_index += 1
            return self.ids[-1], self.last_image, self.transcriptions[-1], self.ids_embedding[-1]
        image = self.load_image(self.ids_index)
        transcription = self.transcriptions[self.ids_index]
        id_embedding = self.ids_embedding[self.ids_index]
        self.ids_index += 1
        return self.ids[self.ids_index - 1], image, transcription, id_embedding

    def __del__(self):
        if self.thread is not None:
            while self.thread.isAlive():
                self.stop_thread = True
