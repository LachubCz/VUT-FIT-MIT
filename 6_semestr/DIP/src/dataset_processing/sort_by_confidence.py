import sys
import argparse
import operator


def parseargs():
    print(' '.join(sys.argv))
    parser = argparse.ArgumentParser()

    parser.add_argument('--input-file', required=True, type=str)
    parser.add_argument('--output-file', required=True, type=str)
    parser.add_argument('--threshold', required=True, type=float)

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = parseargs()

    input_file = args.input_file
    output_file = args.output_file
    threshold = args.threshold

    f = open(input_file, "r", encoding='utf-8')
    lines = f.readlines()

    complex = []
    for line in lines:
        length = len(line.split(' ', maxsplit=2)[2])
        if length > 1:
            confidence = float(line.split(' ')[1])
            complex.append([line, confidence, length])

    sorted_lines = sorted(complex, key=operator.itemgetter(1, 2), reverse=True)

    f = open(output_file, "w", encoding='utf-8')
    for line in sorted_lines[:int(len(sorted_lines)*threshold)]:
        line = line[0].split(' ', maxsplit=2)[0] + ' ' + line[0].split(' ', maxsplit=2)[2]
        f.write("{}".format(line))
    f.close()
