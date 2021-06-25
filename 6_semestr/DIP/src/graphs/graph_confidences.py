import os
import sys
import argparse
import itertools
import matplotlib.pyplot as plt


def parseargs():
    print(' '.join(sys.argv))
    parser = argparse.ArgumentParser()

    parser.add_argument('--datasets', nargs='+', required=True)
    parser.add_argument('--legend', action='store_true')

    args = parser.parse_args()

    return args


def get_confidences(filename):
    f = open(filename, "r", encoding='utf-8')
    lines = f.readlines()
    weights = []
    for i, line in enumerate(lines):
        line = line.strip()
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
                        break
                else:
                    probability = []
                    transcriptions = []
                    break

            if len(probability) != 0 or len(transcriptions) != 0:
                weights.append(probability)

    weights = list(itertools.chain(*weights))
    confidences = {i:0 for i in range(1001)}

    for weight in weights:
        confidences[int(weight*100)] += 1

    return confidences


if __name__ == '__main__':
    args = parseargs()

    for dataset in args.datasets:
        label = os.path.splitext(os.path.basename(dataset))[0]
        confidences = get_confidences(dataset)
        plt.plot([confidences[i] for i in range(101)], label=label)

    if args.legend:
        plt.legend()
    plt.savefig("confidences.pdf", bbox_inches='tight')
    plt.show()
