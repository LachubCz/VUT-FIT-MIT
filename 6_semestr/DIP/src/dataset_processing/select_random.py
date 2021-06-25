import sys
import argparse
import random


def parseargs():
    print(' '.join(sys.argv))
    parser = argparse.ArgumentParser()

    parser.add_argument('--input-file', required=True, type=str)
    parser.add_argument('--output-file', required=True, type=str)
    parser.add_argument('--percentage', required=True, type=float)

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = parseargs()

    input_file = args.input_file
    output_file = args.output_file
    percentage = args.percentage

    f = open(input_file, "r", encoding='utf-8')
    lines = f.readlines()

    random.shuffle(lines)

    f = open(output_file, "w", encoding='utf-8')
    for line in lines[:int(len(lines)*percentage)]:
        f.write("{}".format(line))
    f.close()
