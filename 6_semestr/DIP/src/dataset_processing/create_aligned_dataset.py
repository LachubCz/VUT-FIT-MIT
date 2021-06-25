import cv2
import sys
import math
import lmdb
import time
import argparse
import configparser
import numpy as np
from scipy.special import softmax
from src.src_helper import setGPU
from scipy.sparse import coo_matrix
from pero_ocr.utils import compose_path
from pero_ocr.decoding import decoding_itf
from pero_ocr.decoding.decoding_itf import prepare_dense_logits
from pero_ocr.ocr_engine.pytorch_ocr_engine import PytorchEngineLineOCR
from pero_ocr.document_ocr.layout import log_softmax
from pero_ocr.force_alignment import align_text


def parseargs():
    print(' '.join(sys.argv))
    parser = argparse.ArgumentParser()

    parser.add_argument('--config-path', required=True, type=str)
    parser.add_argument('--lmdb', required=True, type=str)
    parser.add_argument('--input-file-path', required=True, type=str)
    parser.add_argument('--output-file-path', required=True, type=str)
    parser.add_argument('--limit', default=16, type=int)
    parser.add_argument('--type', choices=['variations', 'simple'], default='variations', type=str)

    args = parser.parse_args()

    return args


def process_batch(f, batch_img, batch_txt, ocr_engine, decoder, variations, limit):
    chars = [i for i in range(len(ocr_engine.characters))]
    char_to_num = dict(zip(ocr_engine.characters, chars))
    
    _, processed_logits, _ = ocr_engine.process_lines(batch_img)
    for i, item in enumerate(processed_logits):
        logits = prepare_dense_logits(item)

        hyps = variations[batch_txt[i]]
        ground_truth = np.zeros(logits.shape)
        blank_idx = logits.shape[1]-1
        for hyp in hyps[:limit]:
            neg_logprobs = log_softmax(logits)
            label = []
            for item in hyp[1]:
                if item in char_to_num.keys():
                    if char_to_num[item] >= blank_idx:
                        label.append(0)
                    else:
                        label.append(char_to_num[item])
                else:
                    label.append(0)
            try:
                positions = align_text(-neg_logprobs, np.array(label), blank_idx)
            except (ValueError, IndexError):
                continue
            ground_truth[positions, label] += hyp[0]


        f.write("{} {} {}\n" .format(batch_txt[i],
                                     logits.shape,
                                     ' '.join(str(coo_matrix(np.around(ground_truth, decimals=2))).replace('\n', ' ').split())))


def parse_variations_file(file_path):
    f = open(file_path, "r")
    lines = f.readlines()

    last_id = None
    good = []
    dictionary = dict()
    for i, line in enumerate(lines):
        if i % (1000 * 16) == 0:
            print("PROCESSED LINES {}".format(i / 16))
        id, prob, transcript = line.replace('\n', '').split(' ', 2)
        prob = float(prob)

        if last_id is not None:
            if last_id != id:
                dictionary[last_id] = good
                last_id = id
                good = []
                good.append((prob, transcript))
            else:
                good.append((prob, transcript))
        else:
            last_id = id
            good.append((prob, transcript))

    return dictionary


def parse_simple_file(file_path):
    f = open(file_path, "r")
    lines = f.readlines()

    dictionary = dict()
    for line in lines:
        id, transcript = line.replace('\n', '').split(' ', 1)
        dictionary[id] = [(1, transcript)]

    return dictionary


if __name__ == '__main__':
    args = parseargs()

    config_path = args.config_path
    lmdb_db = args.lmdb
    input_file_path = args.input_file_path
    output_file_path = args.output_file_path
    limit = args.limit

    batch_size = 32

    config = configparser.ConfigParser()
    config.read(config_path)

    setGPU()

    ocr_chars = decoding_itf.get_ocr_charset(compose_path(config['OCR']['OCR_JSON'], config_path))
    decoder = decoding_itf.decoder_factory(config['DECODER'], ocr_chars, allow_no_decoder=False, use_gpu=True, config_path=config_path)
    confidence_threshold = config['DECODER'].getfloat('CONFIDENCE_THRESHOLD', fallback=math.inf)

    json_file = compose_path(config['OCR']['OCR_JSON'], config_path)
    ocr_engine = PytorchEngineLineOCR(json_file, gpu_id=0)

    env = lmdb.open(lmdb_db)
    txn = env.begin()

    if args.type == 'variations':
        variations = parse_variations_file(input_file_path)
    else:
        variations = parse_simple_file(input_file_path)

    f = open(input_file_path, "r")
    lines = f.readlines()

    batch_img = []
    batch_txt = []
    f = open(output_file_path, "w", encoding='utf-8')
    for e, image_name in enumerate(variations.keys()):
        if e % batch_size == 0:
            batch_img = []
            batch_txt = []
        batch_txt.append(image_name)
        data = txn.get(image_name.encode())
        img = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), 1)
        batch_img.append(img)
        if e != 0 and (e + 1) % batch_size == 0:
            process_batch(f, batch_img, batch_txt, ocr_engine, decoder, variations, limit)

    if batch_size != len(batch_img) and len(batch_img) != 0:
        process_batch(f, batch_img, batch_txt, ocr_engine, decoder, variations, limit)

    f.close()
