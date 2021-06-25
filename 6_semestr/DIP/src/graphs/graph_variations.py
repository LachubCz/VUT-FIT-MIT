import os
import sys
import argparse
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def parseargs():
    print(' '.join(sys.argv))
    parser = argparse.ArgumentParser()

    parser.add_argument('--datasets', nargs='+', required=True)
    parser.add_argument('--legend', action='store_true')

    args = parser.parse_args()

    return args


def get_counts(filename):
    f = open(filename, "r", encoding='utf-8')
    lines = f.readlines()
    counts = {i: 0 for i in range(1, 17)}
    weights = []
    for line in lines:
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

    for weight in weights:
        counts[len(weight)] += 1
    return counts


if __name__ == '__main__':
    args = parseargs()

    datasets = []
    for dataset in args.datasets:
        dict = get_counts(dataset)
        datasets.append([dict[i] for i in range(1, 17)])

    labels = [i for i in range(1, 17)]

    font = {'family' : 'normal','size': 15}
    matplotlib.rc('font', **font)

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()

    rects1 = ax.bar(x - width/2, datasets[0], width,
                    label=os.path.splitext(os.path.basename(args.datasets[0]))[0])
    rects2 = ax.bar(x + width/2, datasets[1], width,
                    label=os.path.splitext(os.path.basename(args.datasets[1]))[0])

    ax.set_ylabel('Počet řádků')
    ax.set_xlabel('Počet měkkých pseudo-štítků')

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    if args.legend:
        ax.legend()

    plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    fig.tight_layout()

    fig.savefig("variations.pdf", bbox_inches='tight')
    plt.show()
