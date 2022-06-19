import ast
import re

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator

from param import MONTH
from rand_main_np3 import to2rows


def paint(intro_, mean_, std_):
    l, r = 0, -1
    while sum([intro_[i][l] != intro_[i + 1][l] for i in range(len(intro_) - 1)]) == 0:
        l += 1
    while sum([intro_[i][r] != intro_[i + 1][r] for i in range(len(intro_) - 1)]) == 0:
        r -= 1
    fig4, ax4 = plt.subplots()
    ax4.grid()
    ax4.set_xlabel('betterer时间/月')
    ax4.set_ylabel(r'目标函数/平均值$\pm$标准差(68.27%)')
    prefix = intro_[0][:l - 3]
    suffix = intro_[0][r + 1:]
    ax4.set_title(to2rows(prefix + suffix, formerSep=' / '))
    for intro, table, stds in zip(intro_, mean_, std_):
        label = intro[l:r + 1]
        ax4.plot(np.arange(MONTH) + 1, table[..., 0], label=label)
        ax4.fill_between(np.arange(MONTH) + 1, table[..., 0] - stds[..., 0], table[..., 0] + stds[..., 0], alpha=0.3)

    fig4.legend(loc='lower right')
    ax4.xaxis.set_minor_locator(MultipleLocator(base=1))
    ax4.yaxis.set_minor_locator(AutoMinorLocator())
    plt.grid(which='minor', linestyle=':', linewidth=0.5)
    # plt.grid(which='major', linestyle='-', linewidth=1)
    plt.show()
    fig4.savefig(prefix.replace(' / ', '__'), dpi=400)


def main():
    with open('variance_simulate/Hu Tao/PERSONS = 4005__Hu Tao.vb', 'r', encoding='utf-8') as fin:
        data = fin.read()
    # print(data)
    intro = re.compile(r'PERSONS.*?/.*?(?=\n)').findall(data)
    print(intro)
    mean = re.compile(r'(?<=table = array\().*?(?=\))', re.DOTALL).findall(data)
    mean_ = [ast.literal_eval(x) for x in mean]
    # print(mean_)
    std = re.compile(r'(?<=stds = array\().*?(?=\))', re.DOTALL).findall(data)
    std_ = [ast.literal_eval(x) for x in std]
    # print(std_)
    paint(intro, np.asarray(mean_), np.asarray(std_))
    # print(np.genfromtxt(BytesIO(bytes(std[0], encoding='utf-8'))))
    xxx = '''[[40836.85627278, 53708.9835427 ],
       [44054.07158994, 55945.72753958],
       [45690.68354143, 56974.61333002],
       [46753.33256957, 57561.35239386],
       [47518.72490164, 57942.58191636],
       [48153.03834114, 58320.06543229],
       [48657.91759549, 58549.7983217 ],
       [49090.02177884, 58822.8597873 ],
       [49454.34155127, 58996.53493555],
       [49779.65226131, 59183.89295465],
       [50062.14027739, 59300.82077268],
       [50312.31198143, 59444.34452877]]'''
    # print(np.genfromtxt(BytesIO(bytes(xxx, encoding='utf-8'))))
    # print(ast.literal_eval(xxx))
    # print(np.fromstring())


if __name__ == '__main__':
    main()
