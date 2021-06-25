import cv2
import sys
import math
import lmdb
import argparse
import configparser
import numpy as np
from scipy.special import softmax
from src.src_helper import setGPU
from pero_ocr.utils import compose_path
from pero_ocr.decoding import decoding_itf
from pero_ocr.decoding.decoding_itf import prepare_dense_logits
from pero_ocr.ocr_engine.pytorch_ocr_engine import PytorchEngineLineOCR


def parseargs():
    print(' '.join(sys.argv))
    parser = argparse.ArgumentParser()

    parser.add_argument('--config-path', required=True, type=str)
    parser.add_argument('--lmdb', required=True, type=str)
    parser.add_argument('--input-file-path', required=True, type=str)
    parser.add_argument('--output-file-path', required=True, type=str)

    args = parser.parse_args()

    return args


def process_batch(f, batch_img, batch_txt, ocr_engine, decoder):
    _, processed_logits, _ = ocr_engine.process_lines(batch_img)
    for i, item in enumerate(processed_logits):
        logits = prepare_dense_logits(item)
        hypotheses = decoder(logits)
        hypotheses.sort()
        hyps = list(zip(hypotheses.transcripts(), softmax(hypotheses.posteriors())))

        stack = 0
        for hyp in hyps:
            transcript = hyp[0]
            score = hyp[1]
            f.write("{} {} {}\n".format(batch_txt[i], score, transcript))
            stack += hyp[1]


if __name__ == '__main__':
    args = parseargs()

    config_path = args.config_path
    lmdb_db = args.lmdb
    input_file_path = args.input_file_path
    output_file_path = args.output_file_path
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

    f = open(input_file_path, "r")
    lines = f.readlines()

    batch_img = []
    batch_txt = []
    f = open(output_file_path, "w", encoding='utf-8')
    for e, line in enumerate(lines):
        if e % batch_size == 0:
            batch_img = []
            batch_txt = []
        image_name = line.split(' ')[0]
        batch_txt.append(image_name)
        data = txn.get(image_name.encode())
        img = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), 1)
        batch_img.append(img)
        if e != 0 and (e + 1) % batch_size == 0:
            process_batch(f, batch_img, batch_txt, ocr_engine, decoder)

    if batch_size != len(batch_img) and len(batch_img) != 0:
        process_batch(f, batch_img, batch_txt, ocr_engine, decoder)

    f.close()
