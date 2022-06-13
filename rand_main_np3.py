import time
from collections import Counter

import numpy as np
from matplotlib import pyplot as plt, rcParams

from artifacts import Artifacts
from param import *
from character import *
from weapon import Weapons

rcParams['font.sans-serif'] = ['SimHei']
rcParams['axes.unicode_minus'] = False


def maxMainStat(mains: dict[str, artifacts], chara: character) -> character:
    default_characters = []
    for sands in MAINS['Sands of Eon']:
        for goblet in MAINS['Goblet of Eonothem']:
            for circlet in MAINS['Circlet of Logos']:
                mains['Sands of Eon'] = artifacts('Sands of Eon', sands)
                mains['Goblet of Eonothem'] = artifacts('Goblet of Eonothem', goblet)
                mains['Circlet of Logos'] = artifacts('Circlet of Logos', circlet)
                default_characters.append(deepcopy((sum(mains.values(), chara), mains)))
    default_characters = sorted(default_characters, key=lambda x: x[0].effect())
    for k in default_characters:
        myprint(list(map(formIfNumhalfk, [func() for func in k[0].head])), [x.mainStat for x in k[1].values()])
    global DEFAULT_ARTIFACTS
    DEFAULT_ARTIFACTS = default_characters[-1][1]
    return default_characters[-1][0]


def init(chara: character):
    global default_dmg, error, dft_dmgs

    default_character = maxMainStat(deepcopy(DEFAULT_ARTIFACTS), chara)
    default_dmg = setDEFAULT_DMG(default_character.effect())
    print(default_character)
    dft_dmgs = []
    for func in default_character.head:
        dft_dmgs.append(func())
    print(list(map(formIfNumhalfk, dft_dmgs)))

    error = []


def onemonth(oldarti: dict, chara: character, result: list) -> dict:
    '''每月清背包'''
    oldarti = deepcopy(oldarti)
    oldchara = sum(oldarti.values(), chara)
    oldeffect = oldchara.effect()
    baskets = []
    for i in range(9 * 30):
        if generateSuit():
            part = generatePart()
            if artifacts.star == 4 and part == artifacts.five:
                artifacts.modifyStar(5)
            mainStat = generateMainStat(part)
            if mainStat in MAINS[part]:
                subStats = generateSubStats(mainStat)
                theNew = artifacts(part, mainStat, subStats)
                if part not in PART[0:2] or theNew.__repr__().find('CRIT') != -1:
                    baskets.append(theNew)
            if artifacts.five:
                # print('five')
                artifacts.modifyStar(4)
    flag = True
    for i in range(10):
        if not flag:
            break
        flag = False
        for theNew in baskets:
            newchara = oldchara + theNew
            newchara -= oldarti[theNew.part]
            neweffect = newchara.effect()
            if neweffect > oldeffect:
                oldchara = newchara
                oldeffect = neweffect
                oldarti[theNew.part] = theNew
                flag = True
    result.append(tuple((func() for func in oldchara.head)))
    return oldarti


def main(chara: character):
    global result
    result = [[] for i in range(MONTH)]
    #     import cProfile
    #     cProfile.run('''codes''')
    #     exit()

    artiss = [deepcopy(DEFAULT_ARTIFACTS) for i in range(PERSONS)]
    for k in range(MONTH):
        artiss = [onemonth(artis, chara, result[k]) for artis in artiss]

    # 标题名
    myprint(toFilename(chara.intro.strip(), ' / '))
    realmains = {}
    data = {'ATK': [], 'CRIT Rate': [], 'CRIT DMG': [], 'Elemental Mastery': [], 'Energy Recharge': []}
    for artis in artiss:
        charaw = sum(artis.values(), chara)
        data['ATK'].append(charaw.ATK())
        data['Elemental Mastery'].append(charaw.elementalMastery)
        data['CRIT Rate'].append(charaw.CRIT_Rate)
        data['CRIT DMG'].append(charaw.CRIT_DMG)
        data['Energy Recharge'].append(charaw.EnergyRecharge)
        for arti in artis.values():
            realmains[f'{arti.part}, {arti.mainStat}'] = realmains.get(
                f'{arti.part}, {arti.mainStat}', 0) + 1
    # 仅主期望
    myprint(f'{default_dmg = }')
    # 不同主词条比例，冠杯沙、从多到少
    realmains = {k: realmains[k] for k in sorted(realmains, key=lambda x: (x.split(',')[0], -realmains[x]))}
    myprint({x: formIfNumhalfk(y / PERSONS) for x, y in realmains.items() if len(MAINS[x.split(',')[0]]) > 1})
    # 平均属性
    with open(f'{FILE}.vb', 'a', encoding='utf-8') as fout:
        fout.write(stdform({k: np.average(v) for k, v in data.items()}) + '\n')
    # 圣遗物b词条，圣遗物副b词条
    with open(f'{FILE}.vb', 'a', encoding='utf-8') as fout:
        a = np.array([countEffective(k.values(), chara) for k in artiss])
        ave = np.average(a, 0)
        fout.write(str(ave) + '\n')


def printMonthly(chara: character):
    reslt = np.array(result)
    fig3, ax3 = plt.subplots()
    # 本表
    table = np.empty([MONTH, len(dft_dmgs)])
    stds = np.empty([MONTH, len(dft_dmgs)])
    for i in range(MONTH):
        # 中位数
        rslt = np.sort(reslt[i], axis=0)  # 按列排序
        effects = rslt[..., 0]  # 每行第0列
        datas = np.mean(rslt, axis=0)
        std = np.std(rslt, axis=0)
        table[i, ...] = datas
        stds[i, ...] = std
        # 排序、累加
        t = Counter(effects)
        if chara.intro.split()[0] != 'CRIT':
            t = {Effect2Weight(k): t[k] for k in sorted(t)}
        ax3.plot(t.keys(), np.cumsum(list(t.values())))
    # 第一个表为基准
    global firstTable
    try:
        if not firstTable:
            firstTable = table
    except ValueError:
        pass
    # 表头
    head = list(map(lambda x: x.__name__, chara.head))
    head = np.array([head, ['Weight'] * len(head)])
    head = list(np.array(np.nditer(head, order='F')))
    head = [f'{PERSONS = }'] + head + ['increment']
    tab = [head]
    # tableWidth = max([len(k) for k in head]) + 1
    # print(f'{tableWidth = }')
    # tableFormat = f'%-{tableWidth}s'
    # myprint(''.join(map(lambda x: tableFormat % x, head)))
    for k in range(MONTH):
        out = np.array(table[k])
        out = np.array([out, list(map(lambda x: Effect2Weight(x[0], x[1]), zip(out, dft_dmgs)))])
        out = list(np.array(np.nditer(out, order='F')))
        out = [f'{k + 1} month(s)'] + out + [table[k][0] / firstTable[k][0] - 1]
        tab.append(out)
    # myprint(''.join(map(lambda x: tableFormat % formIfNumhalfk(x), out)))
    printTable(tab)
    myprint('param =', repr(toFilename(chara.intro)))
    myprint(f'{table = }')
    myprint(f'{stds = }')
    myprint('sum_error:', sum(map(lambda x: abs(x), error)))

    # 图标题双行
    ax3.set_title(to2rows(chara.intro))
    # x轴
    if chara.intro.split()[0] != 'CRIT':
        ax3.set_xlabel(r'b词条($\sqrt[31]{2}$)')
    else:
        ax3.set_xlabel('CRIT')
    # 图形使用png
    fig3.savefig('%s.png' % toFilename(chara.intro), dpi=400)
    fig4, ax4 = plt.subplots()
    ax4.grid()
    ax4.set_xlabel('betterer时间/月')
    ax4.set_ylabel(r'目标函数/平均值$\pm$标准差(68.27%)')
    ax4.set_title(to2rows(chara.intro))
    ax4.plot(np.arange(MONTH) + 1, table[..., 0])
    ax4.fill_between(np.arange(MONTH) + 1, table[..., 0] - stds[..., 0], table[..., 0] + stds[..., 0], alpha=0.3)
    fig4.savefig('N %s.png' % toFilename(chara.intro), dpi=400)


def to2rows(intro: str, sep: str = ' / ', formerSep: str = '\n'):
    pnt = 0
    dis = len(intro)
    for cnt in range(666):
        pnt = intro.find(formerSep, pnt + 1)
        if pnt != -1 and abs(pnt * 2 - len(intro)) < dis:
            dis = abs(pnt * 2 - len(intro))
        else:
            intro = intro.strip().split(formerSep)
            return '\n'.join([sep.join(intro[:cnt]), sep.join(intro[cnt:])])


def toFilename(intro: str, sep: str = '__'):
    return intro.strip().replace('\n', sep)


def myprint(*args: any, sep: str = ' ') -> None:
    out = sep.join(map(str, args))
    out = out.replace("'", '"')
    print(out)
    with open(f'{FILE}.vb', 'a', encoding='utf-8') as fout:
        fout.write(out + '\n')


def printTable(tab: list[list]):
    for i in range(len(tab)):
        for j in range(len(tab[i])):
            tab[i][j] = formIfNumhalfk(tab[i][j])
    tab = np.array(tab)
    for j in np.arange(tab.shape[1]):
        l = max([len(tab[i, j]) for i in np.arange(tab.shape[0])])
        for i in np.arange(tab.shape[0]):
            tab[i, j] = '%-*s' % (l, tab[i, j])
    ret = '\n'.join(['   '.join(x) for x in tab])
    myprint(ret)


def main2():
    global firstTable
    firstTable = None
    CHARA = getChara()
    CHARA.intro += f'{PERSONS = }\n'
    CHARA.intro += CHARACTER + '\n'
    global FILE
    FILE = toFilename(CHARA.intro, '__')
    with open(f'{FILE}.vb', 'w') as fout:
        pass
    for weapon in WEAPONS:
        for artifact in ARTIFACT_SETS:
            begin = time.perf_counter()
            chara = deepcopy(CHARA)
            Weapons(chara, weapon)
            Artifacts(chara, artifact)
            chara.intro += generateSuit.__doc__ + '\n'
            chara.intro += onemonth.__doc__ + '\n'
            init(chara)
            main(chara)
            printMonthly(chara)
            end = time.perf_counter()
            myprint(f'{end - begin = }')


if __name__ == '__main__':
    main2()

# per 200*6
# 21.6937246 __sub__
# 8.2545784 __iadd__
# 6.4254665 __isub__
# 6.4305854
