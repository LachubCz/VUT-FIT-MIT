import matplotlib
import matplotlib.pyplot as plt


def process_file(input_file):
    f = open(input_file, "r", encoding='utf-8')
    lines = f.readlines()
    episodes = []
    cer = []
    for line in lines:
        if '' in line:  #todo
            episodes.append(int(line.split(' ')[2]))  #todo
            cer.append(float(line.split(' ')[4].split(':')[1][:-1]))  #todo
    return episodes, cer


if __name__ == '__main__':
    episodes1, cer1 = process_file('')  #todo
    episodes2, cer2 = process_file('')  #todo

    font = {'family' : 'normal','size': 15}
    matplotlib.rc('font', **font)

    fig, ax = plt.subplots()

    plt.plot(episodes1, cer1, label='')  #todo
    plt.plot(episodes2, cer2, label='')  #todo

    ax.set_ylabel('Chyba')
    ax.set_xlabel('Počet trénovacích epizod')

    ax.set_ylim(top=17, bottom=8)  #todo
    ax.legend(fontsize='small')

    fig.savefig("training.pdf", bbox_inches='tight', pad_inches=0)
    plt.show(bbox_inches='tight', pad_inches=0)
