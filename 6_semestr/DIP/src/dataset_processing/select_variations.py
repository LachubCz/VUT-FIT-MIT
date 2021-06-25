import sys
import argparse


def parseargs():
    print(' '.join(sys.argv))
    parser = argparse.ArgumentParser()

    parser.add_argument('--input-file', required=True, type=str)
    parser.add_argument('--output-file', required=True, type=str)
    parser.add_argument('--threshold', required=True, type=float)

    args = parser.parse_args()

    return args


def create_variations(id, good):
    string = '{} ' .format(id)
    for item in good:
        string += '{} {}\0' .format(item[0], item[1])
    string = string[:-1]
    return string


if __name__ == '__main__':
    args = parseargs()

    input_file = args.input_file
    output_file = args.output_file
    threshold = args.threshold

    f = open(input_file, "r", encoding='utf-8')
    lines = f.readlines()

    last_id = None
    stack = 0
    good = []
    f = open(output_file, "w", encoding='utf-8')
    for i, line in enumerate(lines):
        if i % (1000*16) == 0:
            print("PROCESSED LINES {}" .format(i/16))
        id, prob, transcript = line.replace('\n', '').split(' ', 2)
        prob = float(prob)

        if last_id is not None:
            if last_id != id:
                f.write("{}\n" .format(create_variations(last_id, good)))
                last_id = id
                stack = prob
                good = []
                good.append((round(prob, 2), transcript))
            else:
                if stack < threshold:
                    stack += prob
                    good.append((round(prob, 2), transcript))
        else:
            last_id = id
            stack = prob
            good.append((round(prob, 2), transcript))
    f.write("{}\n" .format(create_variations(last_id, good)))
    f.close()
