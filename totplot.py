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
    with open('variance_simulate/Yoimiya/YunJin = 1962.0__PERSONS = 4006__Yoimiya.vb', 'r', encoding='utf-8') as fin:
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


if __name__ == '__main__':
    main()
