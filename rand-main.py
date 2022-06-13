import time
from collections import Counter
from typing import Iterable

from matplotlib import pyplot as plt, rcParams

from param import *

rcParams['font.sans-serif'] = ['SimHei']
rcParams['axes.unicode_minus'] = False


def maxMainStat(mains: dict[str, list[str]], chara: character) -> character:
    mains['Circlet of Logos'] = artifacts('Circlet of Logos', 'CRIT Rate')
    default_character1 = sum(mains.values(), chara)
    mains['Circlet of Logos'] = artifacts('Circlet of Logos', 'CRIT DMG')
    default_character2 = sum(mains.values(), chara)
    if default_character1.effect() > default_character2.effect():
        return default_character1
    else:
        return default_character2


def init(chara: character):
    global default_character, default_dmg, error, show1

    default_character = maxMainStat(DEFAULT_ARTIFACTS, chara)  # sum(DEFAULT_ARTIFACTS.values(), chara)
    default_dmg = setDEFAULT_DMG(default_character.effect())
    if TIMED:
        print(default_character)
    show1 = 0
    if show1:
        global fig, ax1, ax2
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()

    error = []


def onemonth(oldarti: dict, chara: character, result: list) -> dict:
    '''每月清背包'''
    oldarti = deepcopy(oldarti)
    oldchara = sum(oldarti.values(), chara)
    olddamage = oldchara.effect()
    baskets = []
    for i in range(9 * 30):
        if generateSuit():
            part = generatePart()
            mainStat = generateMainStat(part)
            if mainStat in MAINS[part]:
                subStats = generateSubStats(mainStat)
                theNew = artifacts(part, mainStat, subStats)
                if part not in PART[0:2] or theNew.__repr__().find('CRIT') != -1:
                    baskets.append(theNew)
    if DEBUG:
        global cnt, basket
        basket += len(baskets)
    flag = True
    for i in range(10):
        if not flag:
            break
        flag = False
        if DEBUG:
            cnt += 1
        for theNew in baskets:
            newchara = oldchara + theNew
            newchara -= oldarti[theNew.part]
            newdamage = newchara.damage()
            if newdamage > olddamage:
                oldchara = newchara
                olddamage = newdamage
                oldarti[theNew.part] = theNew
                flag = True
    result.append((olddamage, oldchara.bigdamage()))
    return oldarti


def main(chara: character):
    global result
    result = [[] for i in range(MONTH)]
#     import cProfile
#     cProfile.run('''codes''')
#     exit()

    artiss = [deepcopy(DEFAULT_ARTIFACTS) for i in range(PERSONS)]
    for k in range(MONTH):
        if DEBUG:
            global cnt, basket
            cnt, basket = 0, 0
        artiss = [onemonth(artis, chara, result[k]) for artis in artiss]
        if DEBUG:
            print(f'{cnt/PERSONS = }, {basket = }')

    # if DEBUG:
    #     print(artiss[0].values())
    #     print(chara)
    # 标题名
    myprint(toFilename(chara.intro.strip(), ' / '))
    realmains = {}
    data = {'ATK': [], 'CRIT Rate': [], 'CRIT DMG': [], 'Elemental Mastery': []}
    for artis in artiss:
        charaw = sum(artis.values(), chara)
        data['ATK'].append(charaw.ATK())
        data['Elemental Mastery'].append(charaw.elementalMastery)
        data['CRIT Rate'].append(charaw.CRIT_Rate)
        data['CRIT DMG'].append(charaw.CRIT_DMG)
        for arti in artis.values():
            realmains[f'{arti.part}, {arti.mainStat}'] = realmains.get(
                f'{arti.part}, {arti.mainStat}', 0) + 1
    # 仅主期望
    myprint(f'{default_dmg = }')
    # 不同主词条比例
    myprint({x: y / PERSONS for x, y in realmains.items() if len(MAINS[x.split(',')[0]]) > 1})
    # 平均属性
    with open(f'{FILE}.vb', 'a', encoding='utf-8') as fout:
        fout.write(stdform({k: np.average(v) for k, v in data.items()}) + '\n')
    # 圣遗物b词条，圣遗物副b词条
    with open(f'{FILE}.vb', 'a', encoding='utf-8') as fout:
        a = np.array([countEffective(k.values(), chara) for k in artiss])
        ave = np.average(a, 0)
        fout.write(str(ave) + '\n')


def printMonthly(chara: character):
    fig3, ax3 = plt.subplots()
    # 本表
    this = []
    for i in range(MONTH):
        # 中位数
        damages = sorted([k[0] for k in result[i]])
        if DEBUG:
            print(f'{len(damages) = }')
        middamage = midNum(damages)
        bigdamages = sorted([k[1] for k in result[i]])
        midbigdamage = midNum(bigdamages)
        # 双指标
        this.append([f'{i+1} month(s)', middamage, Effect2Weight(middamage), midbigdamage])
        # 排序、累加
        t = Counter(damages)
        if DEBUG:
            print(f'{sum(t.values()) = }')
        if chara.intro.split()[0] != 'CRIT':
            t = {Effect2Weight(k): t[k] for k in sorted(t)}
        if DEBUG:
            print(f'{sum(t.values()) = }')
        ax3.plot(t.keys(), np.cumsum(list(t.values())))
    # 第一个表为基准
    global first
    if not first:
        first = this
    # 表头
    myprint('\t'.join(map(lambda x: '%12s' % x, [f'{PERSONS = }', chara.effect.__name__, Effect2Weight.__name__, chara.bigdamage.__name__, 'increment'])))
    for k in range(MONTH):
        this[k].append(formIfNumhalfk(this[k][1] / first[k][1] - 1))
        myprint('\t'.join(map(lambda x: '%12s' % formIfNumhalfk(x), this[k])))
    myprint('sum_error:', sum(map(lambda x: abs(x), error)))

    # 图标题双行
    ax3.set_title(to2rows(chara.intro))
    # x轴
    if chara.intro.split()[0] != 'CRIT':
        ax3.set_xlabel(r'b词条($\sqrt[31]{2}$)')
    else:
        ax3.set_xlabel('CRIT')
    if TIMED:
        plt.show()
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
    print(out)
    with open(f'{FILE}.vb', 'a', encoding='utf-8') as fout:
        fout.write(out + '\n')


def midNum(lis: Iterable, len=PERSONS):
    return (lis[len // 2] + lis[-len // 2]) / 2


if __name__ == '__main__':
    global first
    first = None
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
