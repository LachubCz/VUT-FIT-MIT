import matplotlib
import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':
    font = {'family' : 'normal','size': 15}
    matplotlib.rc('font', **font)

    data = [[7.12, 3.09],
            [6.57, 3.70],
            [6.25, 3.64]]  #todo

    X = np.arange(2)
    fig, ax = plt.subplots()
    ax.set_ylim(top=8)
    ax.bar(X + 0.00, data[0], width = 0.25, label='Počáteční model')

    xlocs, xlabs = plt.xticks()
    ylocs, ylabs = plt.yticks()

    plt.text(xlocs[1]-0.079, data[0][0]+0.15, data[0][0])
    plt.text(xlocs[2]-0.023, data[1][0]+0.15, data[1][0])
    plt.text(xlocs[3]+0.022, data[2][0] + 0.15, data[2][0])
    plt.text(xlocs[5]+0.12, data[0][1]+0.15, data[0][1])
    plt.text(xlocs[6]+0.2, data[1][1]+0.15, data[1][1])
    plt.text(xlocs[7]+0.22, data[2][1]+0.15, data[2][1])

    ax.bar(X + 0.25, data[1], width = 0.25, label='8 hypotéz')
    ax.bar(X + 0.50, data[2], width = 0.25, label='16 hypotéz')
    plt.xticks([0.25, 1.25],
               ['Malá datová sada', 'Velká datová sada'])

    ax.set_ylabel('CER [%]')
    ax.legend(fontsize='small')

    fig.savefig("comparison_bars.pdf", bbox_inches='tight', pad_inches=0)
    plt.show()
