import time
from collections import Counter

import numpy as np
from matplotlib import pyplot as plt, rcParams

from artifacts import Artifacts
from character import *
from param import *
from tools import stdform
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
    # print(np.array(default_characters)[..., 0])
    # print(np.array(default_characters)[..., 1])
    global DEFAULT_ARTIFACTS
    DEFAULT_ARTIFACTS = default_characters[-1][1]
    return default_characters[-1][0]


def init(chara: character):
    global default_dmg, error, dft_dmgs

    default_character = maxMainStat(deepcopy(DEFAULT_ARTIFACTS), chara)  # sum(DEFAULT_ARTIFACTS.values(), chara)
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

    # if DEBUG:
    #     print(artiss[0].values())
    #     print(chara)
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
    table = []
    for i in range(MONTH):
        # 中位数
        rslt = np.sort(reslt[i], axis=0)  # 按列排序
        effects = rslt[..., 0]  # 每行第0列
        # print(f'{effects = }')
        datas = midNums(rslt)  # [mideffect, midbigdamage, ...]
        # 双指标
        # table.append([f'{i+1} month(s)', mideffect, Damage2Weight(mideffect), midbigdamage])
        table.append(datas)
        # 排序、累加
        t = Counter(effects)
        if chara.intro.split()[0] != 'CRIT':
            t = {Effect2Weight(k): t[k] for k in sorted(t)}
        ax3.plot(t.keys(), np.cumsum(list(t.values())))
    # 第一个表为基准
    global firstTable
    if not firstTable:
        firstTable = table
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
        out = np.array([out, list(map((lambda x: Effect2Weight(x[0], x[1])), zip(out, dft_dmgs)))])
        out = list(np.array(np.nditer(out, order='F')))
        out = [f'{k + 1} month(s)'] + out + [table[k][0] / firstTable[k][0] - 1]
        tab.append(out)
    # myprint(''.join(map(lambda x: tableFormat % formIfNumhalfk(x), out)))
    printTable(tab)
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


def to2rows(intro: str, sep: str = ' / '):
    pnt = 0
    dis = len(intro)
    for cnt in range(666):
        pnt = intro.find('\n', pnt + 1)
        if pnt != -1 and abs(pnt * 2 - len(intro)) < dis:
            dis = abs(pnt * 2 - len(intro))
        else:
            intro = intro.strip().split('\n')
            return '\n'.join([sep.join(intro[:cnt]), sep.join(intro[cnt:])])


def toFilename(intro: str, sep: str = '__'):
    return intro.strip().replace('\n', sep)


def myprint(*args, sep=' '):
    out = sep.join(map(str, args))
    out = out.replace("'", '"')
    print(out)
    with open(f'{FILE}.vb', 'a', encoding='utf-8') as fout:
        fout.write(out + '\n')


def midNums(lis: np.ndarray, length=PERSONS):
    # print(f'{lis[(length-1)//2:length//2+1] = }')
    # return np.average(lis[(length - 1) // 2:length // 2 + 1], 0)
    # weight = np.arange(1, PERSONS + 1) * np.arange(PERSONS, 0, -1)
    lis = lis[length // 4:-length // 4]
    x = np.arange(0, lis.shape[0]) / (lis.shape[0] - 1)
    z = np.polyfit(x, lis, 1)
    p = np.array([np.poly1d(z[..., i]) for i in range(lis.shape[1])])
    # print(z, p)
    # plt.plot(x, lis)
    # for i in range(lis.shape[1]):
    # 	plt.plot(x, np.polyval(p[i], x))
    # plt.show()
    # weight = np.exp(-np.abs(x-0.5)*3)
    # return np.average((lis.T * weight).T, 0) / np.average(weight)
    # print(np.polyval(p[np.arange(lis.shape[1])], 0.5), np.average(lis, 0), np.array([np.polyval(p[i], 0.5) for i in range(lis.shape[1])]))
    return np.array([np.polyval(p[i], 0.5) for i in range(lis.shape[1])])


def printTable(tab: list[list]):
    for i in range(len(tab)):
        for j in range(len(tab[i])):
            tab[i][j] = formIfNumhalfk(tab[i][j])
    tab = np.array(tab)
    for j in np.arange(tab.shape[1]):
        l = max([len(tab[i, j]) for i in np.arange(tab.shape[0])])
        for i in np.arange(tab.shape[0]):
            tab[i, j] = f'%-{l}s' % tab[i, j]
    ret = '\n'.join(['   '.join(x) for x in tab])
    myprint(ret)


if __name__ == '__main__':
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

# per 200*6
# 21.6937246 __sub__
# 8.2545784 __iadd__
# 6.4254665 __isub__
# 6.4305854
