import sys
import random
import argparse


def parseargs():
    print(' '.join(sys.argv))
    parser = argparse.ArgumentParser()

    parser.add_argument('--first', required=True, type=str)
    parser.add_argument('--second', required=True, type=str)
    parser.add_argument('--third', required=True, type=str)
    parser.add_argument('--output', required=True, type=str)

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = parseargs()

    first_file = args.first
    second_file = args.second
    third_file = args.third
    output_file = args.output

    f = open(first_file, "r", encoding='utf-8')
    lines_first = f.readlines()

    f = open(second_file, "r", encoding='utf-8')
    lines_second = f.readlines()

    f = open(third_file, "r", encoding='utf-8')
    lines_third = f.readlines()

    lines_all = lines_first + lines_second + lines_third
    random.shuffle(lines_all)

    f = open(output_file, "w", encoding='utf-8')
    for line in lines_all:
        f.write(line)
    f.close()
