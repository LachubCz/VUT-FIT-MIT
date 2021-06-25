import matplotlib
import matplotlib.pyplot as plt


if __name__ == '__main__':
    font = {'family' : 'normal','size': 15}
    matplotlib.rc('font', **font)

    fig, ax = plt.subplots()
    ax.set_ylabel('CER [%]')
    ax.set_xlabel('% cílových anotovaných dat')
    ax.set_xlim(left=0, right=2000)

    plt.axhline(y=2.58, color='#ff7f0e', linestyle='dotted')
    plt.axhline(y=6.43, color='#ff7f0e', linestyle='dotted')

    plt.plot([10, 50, 100, 500, 1000, 2000], [6.43, 3.84, 3.21, 2.62, 2.58, 2.38], color='#ff7f0e', label='Cílová anotovaná data')
    plt.plot([10, 50, 100, 500, 1000, 2000], [2.82, 2.85, 2.86, 2.96, 3.06, 3.34], color='#1f77b4', label='Související anotovaná data')
    plt.plot([10, 50, 100, 500, 1000, 2000], [6.43, 3.84, 3.21, 2.62, 2.58, 2.38], 'rs', color='#ff7f0e')
    plt.plot([10, 50, 100, 500, 1000, 2000], [2.82, 2.85, 2.86, 2.96, 3.06, 3.34], 'rs',  color='#1f77b4')

    ax.legend(fontsize='small')

    fig.savefig("comparison_lines.pdf", bbox_inches='tight')
    plt.show()
