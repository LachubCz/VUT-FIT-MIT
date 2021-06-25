import cv2
import os
import sys
import lmdb
import itertools
import numpy as np
from scipy.sparse import coo_matrix
from datasets.charset import get_chars_mapping


class TextDataset(object):
    def __init__(self, max_width=1024, transcriptions_file=None, images_path=None, lmdb_database=None, chars=None, verbose=False,
                 transformer=None, weights=False, alignment=False):
        self.max_width = max_width
        self.transcriptions_file = transcriptions_file
        self.images_path = images_path
        self.lmdb_database = lmdb_database
        self.chars = chars
        self.ids = []
        self.ids_embedding = []
        self.weights = []
        self.transcriptions = []
        self.transformer = None
        rejected = 0
        if self.lmdb_database is not None:
            env = lmdb.open(self.lmdb_database, map_size=int(1e9))
            self.txn = env.begin()

        with open(self.transcriptions_file, 'r', encoding="utf-8") as f:
            lines = f.readlines()
            line = lines[0].strip()
            line_split = line.split(" ", 2)
            image_name = line_split[0]
            img = self.load_original_image(image_name)
            self.height = img.shape[0]
            if len(img.shape) > 2:
                self.channels = img.shape[2]
            else:
                self.channels = 1

            embedding = True
            for i, line in enumerate(lines):
                line = line.strip()
                line_split = line.split(" ")
                if len(line_split) > 1:
                    try:
                        int(line_split[1])
                    except ValueError:
                        embedding = False
                    break

            for i, line in enumerate(lines):
                line = line.strip()
                if not embedding and not weights and not alignment:
                    line_split = line.split(" ", 1)
                    if len(line_split) > 1:
                        self.ids.append(line_split[0])
                        self.ids_embedding.append(0)
                        self.weights.append(1)
                        self.transcriptions.append(line_split[1])
                    else:
                        rejected += 1
                elif weights:
                    line_split = line.split(" ", 1)
                    if len(line_split) > 1:
                        annotations = line_split[1]
                        annotations_split = annotations.split('\0')
                        probability = []
                        transcriptions = []
                        for ann in annotations_split:
                            ann_split = ann.split(' ', 1)
                            if len(ann_split) > 1:
                                if ann_split[1] != '':
                                    probability.append(float(ann_split[0]))
                                    transcriptions.append(ann_split[1])
                                else:
                                    probability = []
                                    transcriptions = []
                                    rejected += 1
                                    break
                            else:
                                probability = []
                                transcriptions = []
                                rejected += 1
                                break

                        if len(probability) != 0 or len(transcriptions) != 0:
                            self.ids.append(line_split[0])
                            self.ids_embedding.append(0)
                            self.weights.append(probability)
                            self.transcriptions.append(transcriptions)
                    else:
                        rejected += 1
                elif alignment:
                    split = line.split(' ', 3)
                    if len(split) == 4:
                        id = split[0]
                        dim1 = split[1][1:-1]
                        dim2 = split[2][:-1]
                        gt = np.zeros((int(dim1), int(dim2)))
                        labels = split[3].split('(')[1:]
                        for label in labels:
                            position, value = label.replace(' ', '').split(')')
                            pos1, pos2 = position.split(',')
                            gt[int(pos1)][int(pos2)] = float(value.replace(':', ''))

                        self.ids.append(id)
                        self.ids_embedding.append(0)
                        self.weights.append(1)
                        self.transcriptions.append(coo_matrix(gt))
                    else:
                        rejected += 1
                else:
                    line_split = line.split(" ", 2)
                    if len(line_split) > 2:
                        self.ids.append(line_split[0])
                        embedding_id = int(line_split[1])
                        self.ids_embedding.append(embedding_id)
                        self.weights.append(1)
                        self.transcriptions.append(line_split[2])
                    else:
                        rejected += 1

        if transformer is not None:
            self.transformer = transformer(self.height)
        if not alignment:
            if not weights:
                self.from_char, self.to_char = get_chars_mapping(self.transcriptions, self.chars)
            else:
                self.from_char, self.to_char = get_chars_mapping(list(itertools.chain(*self.transcriptions)), self.chars)

        if verbose:
            if embedding:
                print("EMBEDDING DATASET")
            if weights:
                print("WEIGHTED DATASET")
            print("Dataset {} loaded".format(self.transcriptions_file))
            print("Rejected images", rejected)

    def load_original_image(self, image_name):
        if self.images_path is not None:
            img = cv2.imread(os.path.join(self.images_path, image_name), 1)
        elif self.lmdb_database is not None:
            data = self.txn.get(image_name.encode())
            if data is None:
                print(f"Unable to load from DB '{image_name}'.", file=sys.stderr)
            img = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), 1)
            if img is None:
                print(f"Unable to decode image '{image_name}'.", file=sys.stderr)
        else:
            print("No data to evaluate.", file=sys.stderr)
            sys.exit(1)
        if self.transformer is not None:
            img = self.transformer(images=[img])[0]
        return img

    def load_image(self, index):
        if not index < len(self.ids):
            return None
        return self.load_original_image(self.ids[index])

    def get_shape(self):
        return [self.height, self.max_width, self.channels]

    def get_number_of_embeddings(self):
        return max(self.ids_embedding) + 1
