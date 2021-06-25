# -*- coding: utf-8 -*-
from __future__ import print_function

import torch
import json
import numpy as np
import time
import os
import cv2
import sys
import argparse
import queue
import Levenshtein

from src.error_visualization import image_transcriptions_errors, console_transcriptions_errors
from src.src_helper import setGPU
from datasets.text_dataset_random import TextDatasetRandom
from datasets.text_dataset_sequential import TextDatasetSequential
from datasets.charset import character_set

from pytorch_ctc.training_ctc import CTCModelWrapper
from pytorch_ctc.optimizing import build_optimizer, HonzaSchleduler
from pytorch_ctc.optimizing import PlateauLRReducer, InterpolatingLRReducer, NOPReducer
from pytorch_ctc.ctc_helpers import greedy_decode_ctc

from datasets.augmentation.line_transformers_definitions import LINE_TRANSFORMERS


def parseargs():
    print(' '.join(sys.argv))
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--gpu-id', type=int,
                        help='If not set setGPU() is called. Set this to 0 on desktop, do not specify on SGE.')

    # Datasets definition
    # 
    parser.add_argument('--trn-data', required=True, type=str,
                        help='Text file with image names/keys and transcriptions for training. \
                              Line format: image.jpg [embedding_id] transcription')
    parser.add_argument('--tst-data', action='append', type=str,
                        help='Text files with image names/keys and transcriptions for testing. \
                              Line format: image.jpg [embedding_id] transcription')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--images-path', type=str, help='Directory with images specified in text files.')
    group.add_argument('-l', '--lmdb-path', type=str, help='LMDB with keys specified in text files.')
    parser.add_argument('-m', '--data-manipulator', default='NONE', choices=list(LINE_TRANSFORMERS.keys()), type=str,
                        help='Data data manipulator for training. No data manipulator is used for testing.')
    parser.add_argument('--max-line-width', default=2048, help='Maximum image width.', type=int)
    parser.add_argument('--pad-to-max-width', action='store_true', help='Pad all images to max-line-width.')
    parser.add_argument('--max-buffer-size', default=5000, type=int,
                        help='Maximum buffer size for trn dataset. Value -1 reads the whole dataset into memory.')

    parser.add_argument('-c', '--chars-set', default='all_chars', choices=list(character_set.keys()), type=str,
                        help='Blank is always appended to character set.')

    # Model definition
    #
    parser.add_argument('-n', '--net', required=True, type=str)
    parser.add_argument('--normalization-scale-std', default=0.1, type=float)

    # Training
    #
    parser.add_argument('--optimizer', default='Adam', type=str)
    parser.add_argument('--learning-rate', default=0.0003, type=float)
    parser.add_argument('--batch-size', default=16, type=int)
    parser.add_argument('--dropout-rate', default=0.0, type=float)
    parser.add_argument('--start-iteration', default=0, type=int)
    parser.add_argument('--max-iterations', default=500000, type=int)

    parser.add_argument('--warm-up-iterations', default=0, type=int)
    parser.add_argument('--warm-up-polynomial-order', default=3, type=int)

    parser.add_argument('--reduce-lr-on-plateau', choices=['none', 'counted', 'interpolating'], default='none', help='counted = change if not improving')
    parser.add_argument('--reduce-lr-patience', default=3, type=int,
                        help='How many times the loss can not improve before decaying LR')
    parser.add_argument('--reduce-lr-slope-threshold', default=-1e-2, type=float,
                        help='Maximal acceptable slope of linear interpolation of losses. Has to be negative')
    parser.add_argument('--reduce-lr-factor', default=0.42, type=float,
                        help='What to multiply LR with when loss stops improving')
    parser.add_argument('--min-lr', default=1e-10, type=float, help='If LR drops below this, training is stopped')
    parser.add_argument('--reducer-step', default=500, type=int)

    # Saving models and reporting during training
    # 
    parser.add_argument('-t', '--test', action='store_true')
    parser.add_argument('--test-step', default=500, type=int)
    parser.add_argument('-i', '--in-checkpoint', type=str)
    parser.add_argument('-o', '--out-checkpoint', type=str)
    parser.add_argument('-d', '--checkpoint-dir', default='.', type=str)
    parser.add_argument('--save-step', default=500, type=int)
    parser.add_argument('--print-trans', action='store_true')
    parser.add_argument('--show-trans', action='store_true')
    parser.add_argument('--show-dir', default='.', type=str)
    parser.add_argument('--arabic', action='store_true')

    parser.add_argument('--view-step', type=int, help='Set test_step, save_step to view_step.')

    args = parser.parse_args()
    return args


def main():
    args = parseargs()

    chars = character_set[args.chars_set]
    print('CHARACTERS_JSON', json.dumps(chars))
    print('CHARACTERS', ''.join(chars))
    print()

    print("INIT DATASETS")
    print()
    transformer = LINE_TRANSFORMERS[args.data_manipulator]
    trn_dataset, tst_datasets = init_datasets(args.max_buffer_size, args.trn_data, args.tst_data, args.images_path,
                                              args.lmdb_path, chars, args.batch_size, args.max_line_width,
                                              args.pad_to_max_width, transformer=transformer)

    if args.gpu_id is None:
        setGPU()
    else:
        os.environ['CUDA_VISIBLE_DEVICES'] = str(args.gpu_id)
    print(f'CUDA_VISIBLE_DEVICES={os.environ["CUDA_VISIBLE_DEVICES"]}')

    print()
    print("INIT TRAINING")

    model = CTCModelWrapper.build_model(
        net=args.net,
        num_output_symbols=len(trn_dataset.chars),
        input_channels=trn_dataset.get_shape()[-1],
        input_height=trn_dataset.get_shape()[0],
        dropout_rate=args.dropout_rate,
        num_embeddings=trn_dataset.get_number_of_embeddings(),
        normalization_scale_std=args.normalization_scale_std
    )
    optimizer = build_optimizer(args.optimizer, model, args.learning_rate)
    scheduler = HonzaSchleduler(optimizer, args.learning_rate, args.warm_up_iterations, args.warm_up_polynomial_order)
    model_wrapper = CTCModelWrapper(
        net=model,
        optimizer=optimizer,
        loss='weighted'
    )
    model_wrapper.decode_logits = greedy_decode_ctc

    if args.reduce_lr_on_plateau == 'counted':
        lr_reducer = PlateauLRReducer(
            patience=args.reduce_lr_patience,
            decay_factor=args.reduce_lr_factor,
            base_scheduler=scheduler,
        )
    elif args.reduce_lr_on_plateau == 'interpolating':
        lr_reducer = InterpolatingLRReducer(
            threshold=args.reduce_lr_slope_threshold,
            cooldown=args.reduce_lr_patience,
            decay_factor=args.reduce_lr_factor,
            base_scheduler=scheduler,
        )
    else:
        lr_reducer = NOPReducer()

    print()
    print("NET")
    print()
    print(model_wrapper.net)

    print()
    load_weights(model_wrapper, args.in_checkpoint, args.start_iteration, args.checkpoint_dir)
    print()

    if args.show_trans:
        init_show_dirs(args.show_dir)

    print()
    print("START TRAINING")
    print()

    if args.view_step is not None:
        args.test_step = args.view_step
        args.save_step = args.view_step

    def is_valid_iter(it_no, step):
        return it_no % step == 0

    train_time = 0.0
    total_nb_lines = 0.0

    trn_loss = 0.0
    train_net_time = 0.0
    test_timer = time.time()

    reducer_trn_loss = 0.0

    model_wrapper.set_train()
    for iteration in range(args.start_iteration, args.max_iterations + 1):
        test_and_show = args.test and (is_valid_iter(iteration, args.test_step) or iteration == args.start_iteration)
        show_train = is_valid_iter(iteration, args.test_step) and iteration > args.start_iteration
        run_reducer = is_valid_iter(iteration, args.reducer_step) and iteration > args.start_iteration
        save_checkpoint = is_valid_iter(iteration, args.save_step) and iteration > args.start_iteration

        if test_and_show or show_train or save_checkpoint:
            print()
            print(f"ITERATION {iteration}")
            print("---------------------------------------------------------------------------------------------------")

        if test_and_show:
            model_wrapper.set_eval()

            if args.tst_data is not None:
                for tst_dataset in tst_datasets:
                    test(model_wrapper, iteration, tst_dataset, args.batch_size, args.print_trans,
                         args.show_trans, args.show_dir, args.pad_to_max_width, args.arabic)
            model_wrapper.set_train()
            print()

        if show_train:
            test_time = time.time() - test_timer
            train_time += test_time
            net_speed = (args.test_step * data.shape[0] * data.shape[2] / data.shape[1]) / train_net_time
            trn_loss /= args.test_step
            print(f"TRAIN {iteration} ({total_nb_lines/1000:.1f}k lines seen) loss:{trn_loss:.3f} time:{test_time:.1f} net_speed:{net_speed}")
            print()
            train_net_time = 0.0
            trn_loss = 0.0
            test_timer = time.time()

        if run_reducer:
            lr_reducer.step(reducer_trn_loss)
            reducer_trn_loss = 0.0

        if save_checkpoint:
            save_weights(model_wrapper, args.out_checkpoint, iteration, args.checkpoint_dir)

        if test_and_show or show_train or save_checkpoint:
            print("---------------------------------------------------------------------------------------------------")
            print()

        if iteration == args.max_iterations:
            break

        if lr_reducer.has_reduced and scheduler.act_lr < args.min_lr:
            print(f'Learning rate has reached {scheduler.act_lr}, stopping the training.')
            break

        batch = trn_dataset.get_batch(args.batch_size, pad_to_max_width=args.pad_to_max_width)
        data = batch['images']
        labels_lengths = batch['labels_lengths']
        scheduler.update_learning_rate(iteration)
        net_t1 = time.time()
        _, loss = model_wrapper.train_step(batch)
        train_net_time += time.time() - net_t1
        loss = loss.mean()
        trn_loss += loss
        reducer_trn_loss += loss
        total_nb_lines += len(labels_lengths)

    train_time += time.time() - test_timer

    print("AVERAGE TIME OF 100 ITERATIONS: {}".format((train_time / (args.max_iterations - args.start_iteration)) * 100))


def test(training, iteration, dataset, batch_size, print_trans, show_trans, show_dir, pad_to_max_width=False, arabic=False):
    total_loss = 0
    total_nb_errors = 0
    total_ref_len = 0
    t1 = time.time()
    total_net_time = 0
    total_line_length = 0

    if dataset.type == 'sequential':
        batch_generator = SequentialDatasetTestGenerator(dataset, batch_size)
        train = False
    elif dataset.type == 'random':
        batch_generator = RandomDatasetTestGenerator(dataset, batch_size, pad_to_max_width)
        train = True
    else:
        raise ValueError(f'Unsupported dataset type: {dataset.type}')

    with torch.no_grad():
        for it_count, batch in enumerate(batch_generator, 1):
            data = batch['images']
            labels = batch['labels']

            net_t1 = time.time()
            outs, loss = training.test_step(batch)

            decoded = training.decode_logits(outs)
            if 'actual_batch_size' in batch:
                decoded = decoded[:batch['actual_batch_size']]
                labels = labels[:batch['actual_batch_size']]
                loss = loss[:batch['actual_batch_size']]

            total_loss += loss.mean().item()
            total_net_time += time.time() - net_t1
            err, count = compute_character_error(labels, decoded)
            total_nb_errors += err
            total_ref_len += count
            total_line_length += data.shape[0] * data.shape[2] / data.shape[1]

            if it_count == 1:
                show_batch_data = data
                show_batch_transcriptions = decode_labels(decoded, dataset.chars)
                show_batch_ground_truth = decode_labels(labels, dataset.chars)

    t2 = time.time()

    print('TEST {} {:d} loss:{:.5f} cer:{:.2f}% full_speed:{:.0f} net_speed:{:.0f} time:{:.1f}'.format(
        dataset.transcriptions_file,
        iteration,
        total_loss / it_count,
        100.0 * total_nb_errors / total_ref_len,  # CER
        total_line_length / (t2 - t1),
        total_line_length / total_net_time,
        t2 - t1
    ))

    if dataset.type == 'random':
        rejected = dataset.rejected_lines
        total = dataset.total_lines
        print(f'Training dataset rejection rate: {rejected/total * 100:.2f} % ({rejected}/{total})')

    if print_trans:
        print_transcriptions(show_batch_transcriptions, show_batch_ground_truth)

    if show_trans:
        show_transcriptions(show_batch_data, iteration, dataset.transcriptions_file, train, show_dir, show_batch_transcriptions, show_batch_ground_truth, arabic)


class SequentialDatasetTestGenerator:
    def __init__(self, dataset, batch_size):
        self.dataset = dataset
        self.batch_size = batch_size

    def __iter__(self):
        while True:
            batch = self.dataset.get_batch()
            yield batch

            if batch['actual_batch_size'] < self.batch_size:
                self.dataset.reset()
                break


class RandomDatasetTestGenerator:
    def __init__(self, dataset, batch_size, pad_to_max_width, nb_lines=2000):
        self.dataset = dataset
        self.batch_size = batch_size
        self.pad_to_max_width = pad_to_max_width
        self.nb_lines = nb_lines

    def __iter__(self):
        generated_lines = 0
        while generated_lines < self.nb_lines:
            batch = self.dataset.get_batch(self.batch_size, self.pad_to_max_width)
            generated_lines += batch['images'].shape[0]
            yield batch


def compute_character_error(reference, decoded):
    err = 0
    count = 0
    for r, d in zip(reference, decoded):
        err += Levenshtein.distance(''.join([chr(x) for x in r]), ''.join([chr(x) for x in d]))
        count += r.shape[0]
    return err, count


def init_datasets(max_buffer_size, trn_data, tst_data, images_path, lmdb_path, chars, batch_size, max_line_width,
                  pad_to_max_width, transformer=None):
    if images_path is None and lmdb_path is None:
        print("No data to evaluate for training phase.", file=sys.stderr)
        sys.exit(1)
    trn_dataset = None
    if trn_data is not None:
        trn_dataset = TextDatasetRandom(max_buffer_size, data_format="PyTorch", transcriptions_file=trn_data,
                                        images_path=images_path, lmdb_database=lmdb_path, chars=chars,
                                        max_width=max_line_width, verbose=True, transformer=transformer, alignment=True)
    max_queue_size = 400
    tst_datasets = None
    if tst_data is not None:
        tst_datasets = []
        for tst_data_path in tst_data:
            tst_queue = queue.Queue(max_queue_size)
            tst_dataset = TextDatasetSequential(tst_queue, batch_size, data_format="PyTorch",
                                                pad_to_max_width=pad_to_max_width, transcriptions_file=tst_data_path,
                                                images_path=images_path, lmdb_database=lmdb_path, chars=chars,
                                                max_width=max_line_width, verbose=True)
            tst_datasets.append(tst_dataset)

    c = 0
    if trn_data is not None:
        while not trn_dataset.buffer_filled:
            if c % 10 == 0:
                print("{} trn data loaded into buffer.".format(sum([x is not None for x in trn_dataset.images_buffer])))
            c += 1
            time.sleep(1)

    return trn_dataset, tst_datasets


def load_weights(training, in_checkpoint=None, start_iteration=0, checkpoint_dir=None):
    checkpoint_path = None
    if in_checkpoint is not None:
        checkpoint_path = in_checkpoint
    elif start_iteration:
        checkpoint_path = os.path.join(checkpoint_dir, "checkpoint_{:06d}.pth".format(start_iteration))
    if checkpoint_path is not None:
        print("LOAD WEIGHTS:", checkpoint_path)
        training.load_weights(checkpoint_path)


def save_weights(training, out_checkpoint, iteration, checkpoint_dir):
    if out_checkpoint is not None:
        checkpoint_path = out_checkpoint
    else:
        if not os.path.exists(checkpoint_dir):
            os.makedirs(checkpoint_dir)
        checkpoint_path = os.path.join(checkpoint_dir, "checkpoint_{:06d}.pth".format(iteration))
    training.save_weights(checkpoint_path)
    print("CHECKPOINT SAVED TO: {}".format(checkpoint_path))


def print_transcriptions(transcriptions, ground_truths):
    console_transcriptions, console_ground_truths = console_transcriptions_errors(transcriptions, ground_truths)
    for (t, g) in zip(console_transcriptions, console_ground_truths):
        print(f"Transcription: '{t}'")
        print(f"Ground-truth:  '{g}'")
        print()


def show_transcriptions(data, iteration, dataset_name, train, show_dir, transcriptions=None, ground_truths=None, arabic=False, batch_id=None):
    images = []
    data = np.transpose(data, (0, 2, 3, 1))
    for i in range(data.shape[0]):
        images.append(data[i])

    line_height = images[0].shape[0]
    image = np.concatenate(images, axis=0)

    if transcriptions is not None and ground_truths is not None:
        extension = image_transcriptions_errors(transcriptions, ground_truths, line_height=line_height, arabic=arabic)
        image = np.hstack((image, extension))

    dataset_name = os.path.split(dataset_name)[-1]
    train_test = "train"
    if not train:
        train_test = "test"

    print(show_dir, batch_id)
    if batch_id is None:
        image_path = os.path.join(show_dir, "test", train_test, "TEST_BATCH_{}_{:06d}.jpg".format(dataset_name, iteration))
    else:
        image_path = os.path.join(show_dir, "TEST_BATCH_{}_{:06d}_{:02d}.jpg".format(dataset_name, iteration, batch_id))

    if not train:
        print("SAVING TEST BATCH TO: {}".format(image_path))
    else:
        print("SAVING TRAIN BATCH TO: {}".format(image_path))
    cv2.imwrite(image_path, image)


def init_show_dirs(show_dir):
    trn_dir_path = os.path.join(show_dir, "train")
    if not os.path.exists(trn_dir_path):
        os.makedirs(trn_dir_path)
    tst_dir_path = os.path.join(show_dir, "test")
    if not os.path.exists(tst_dir_path):
        os.makedirs(tst_dir_path)
    tst_trn_dir_path = os.path.join(tst_dir_path, "train")
    if not os.path.exists(tst_trn_dir_path):
        os.makedirs(tst_trn_dir_path)
    tst_tst_dir_path = os.path.join(tst_dir_path, "test")
    if not os.path.exists(tst_tst_dir_path):
        os.makedirs(tst_tst_dir_path)


def decode_labels(labels, chars):
    texts = []

    for line_labels in labels:
        text = ""

        for label in line_labels:
            text += chars[label]

        texts.append(text)

    return texts


if __name__ == '__main__':
    main()
