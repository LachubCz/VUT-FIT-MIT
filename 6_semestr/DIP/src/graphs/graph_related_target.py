import matplotlib
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
    labels = [10, 50, 100, 500, 1000, 2000]  #todo
    datasets = [[189805, 189805, 189805, 189805, 189805, 189805], [919, 4597, 9194, 45970, 91940, 183880]]  #todo

    font = {'family' : 'normal','size': 15}
    matplotlib.rc('font', **font)

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()

    rects1 = ax.bar(x - width/2, datasets[0], width,
                    label='Související anotovaná data')

    rects2 = ax.bar(x + width/2, datasets[1], width,
                    label='Cílová anotovaná data')

    ax.set_ylabel('Počet řádků')
    ax.set_xlabel('% cílových anotovaných dat')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    fig.tight_layout()

    fig.savefig("variations_target_related.pdf", bbox_inches='tight')
    plt.show()
