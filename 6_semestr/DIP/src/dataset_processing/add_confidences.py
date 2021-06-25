import sys
import argparse


def parseargs():
    print(' '.join(sys.argv))
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', required=True, type=str)
    parser.add_argument('--output', required=True, type=str)

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = parseargs()

    f = open(args.input, "r", encoding='utf-8')
    lines = f.readlines()

    f = open(args.output, "w", encoding='utf-8')
    for line in lines:
        splitted = line.split(' ', 1)
        splitted[0] += ' 1.0 '
        f.write(splitted[0]+splitted[1])
        if len(splitted) == 1:
            print(line)
    f.close()
