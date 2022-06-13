import ast
from colorsys import hls_to_rgb

from matplotlib import pyplot as plt
from numpy import cumsum

from param import *

if CHARACTER != 'Hu Tao':
    print("CHARACTER != 'Hu Tao'")
    exit()

HuTao = getChara()

Staff_of_Homa(HuTao)
# Dragons_Bane(HuTao)


Wanderers_Troupe2(HuTao)
# Crimson_Witch_of_Flames(HuTao)
# Shimenawas_Reminiscence(HuTao)

DEFAULT_LIST = {
    'Flower of Life': artifacts('Flower of Life', 'HP'),
    'Plume of Death': artifacts('Plume of Death', 'ATK'),
    'Sands of Eon': artifacts('Sands of Eon', 'Elemental Mastery'),
    'Goblet of Eonothem': artifacts('Goblet of Eonothem', 'Pyro DMG Bonus'),
    'Circlet of Logos': artifacts('Circlet of Logos', 'CRIT Rate'),
}
nowlist = {
    'Flower of Life': artifacts('Flower of Life', 'HP', sub=['CRIT DMG+14.0%', 'HP+5.8%', 'Elemental Mastery+56', 'CRIT Rate+9.7%']),
    'Plume of Death': artifacts('Plume of Death', 'ATK', sub=['CRIT Rate+6.6%', 'CRIT DMG+5.4%', 'Elemental Mastery+79', 'HP+239']),
    'Sands of Eon': artifacts('Sands of Eon', 'HP%', sub=['ATK+5.3%', 'CRIT Rate+7.0%', 'HP+777', 'CRIT DMG+10.9%']),
    'Goblet of Eonothem': artifacts('Goblet of Eonothem', 'Pyro DMG Bonus', sub=['CRIT Rate+6.6%', 'HP+956', 'ATK+10.5%', 'Elemental Mastery+23']),
    'Circlet of Logos': artifacts('Circlet of Logos', 'CRIT Rate', sub=['Elemental Mastery+40', 'CRIT DMG+14.0%', 'Energy Recharge+6.5%', 'HP+13.4%']),
}
MAINS = {
    'Flower of Life': ['HP'],
    'Plume of Death': ['ATK'],
    'Sands of Eon': ['Elemental Mastery', 'HP%'],
    'Goblet of Eonothem': ['Pyro DMG Bonus'],
    'Circlet of Logos': ['CRIT Rate'],
}
DEFAULT_ARTIFACT = sum(DEFAULT_LIST.values(), HuTao)
default_dmg = DEFAULT_ARTIFACT.effect()
setDEFAULT_DMG(default_dmg)
# print(DEFAULT_ARTIFACT)

charaw = sum(nowlist.values(), HuTao)
# print(charaw)
damage = charaw.effect()

show1 = 0
if show1:
    fig, ax1 = plt.subplt.plots()
    ax2 = ax1.twinx()

DEBUGGING = 0

with open('pre.txt') as fin:
    pred = ast.literal_eval(fin.read())


testCase = [
    artifacts('Plume of Death', 'ATK', sub=[
              'ATK+9.9%', 'HP+4.7%', 'CRIT Rate+3.1%', 'HP+299'], enhanceCount=4),
    artifacts('Plume of Death', 'ATK', sub=[
              'CRIT Rate+3.5%', 'DEF+5.1%', 'Elemental Mastery+21', 'DEF+16'], enhanceCount=4),
    artifacts('Sands of Eon', 'HP%', sub=[
              'ATK+5.3%', 'CRIT Rate+7.0%', 'HP+777', 'CRIT DMG+10.9%']),
    artifacts('Sands of Eon', 'HP%', sub=[
              'DEF+42', 'CRIT Rate+3.1%', 'ATK+18', 'HP+239'], enhanceCount=3),
    artifacts('Sands of Eon', 'HP%', sub=[
              'HP+418', 'ATK+33', 'CRIT Rate+2.7%', 'Energy Recharge+4.5%'], enhanceCount=3),
    artifacts('Goblet of Eonothem', 'Pyro DMG Bonus', sub=[
              'DEF+5.1%', 'CRIT Rate+11.3%', 'HP+448', 'ATK+39']),
    artifacts('Goblet of Eonothem', 'Pyro DMG Bonus', sub=[
              'ATK+5.3%', 'HP+239', 'HP+5.3%', 'Elemental Mastery+16'], enhanceCount=4),
    artifacts('Circlet of Logos', 'CRIT Rate', sub=[
              'DEF+6.6%', 'HP+239', 'HP+4.7%', 'CRIT DMG+7.0%'], enhanceCount=5),
]


def ifcrit(case: list[artifacts]):
    ret = []
    off = random()
    for i in range(len(case)):
        k = case[i]
        k.line = '-'
        k.color = hls_to_rgb((random() * 0.5 + i) / len(case), random() * 0.4 + 0.4, random() * 0.1 + 0.9)
        ret.append(k)
        if k.sub.__str__().find('CRIT Rate') != -1:
            if k.enhanceCount > 1:
                k = deepcopy(k)
                k.subValue[k.subStats.index('CRIT Rate')] += 0.033
                k.enhanceCount -= 1
                k.line = '--'
                ret.append(k)
                print(k)
            if k.enhanceCount > 1:
                k = deepcopy(k)
                k.subValue[k.subStats.index('CRIT Rate')] += 0.033
                k.enhanceCount -= 1
                k.line = '-.'
                ret.append(k)
                print(k)
            if k.enhanceCount > 1:
                k = deepcopy(k)
                k.subValue[k.subStats.index('CRIT Rate')] += 0.033
                k.enhanceCount -= 1
                k.line = ':'
                ret.append(k)
                print(k)
            if k.enhanceCount > 1:
                k = deepcopy(k)
                k.subValue[k.subStats.index('CRIT Rate')] += 0.033
                k.enhanceCount -= 1
                k.line = ':'
                ret.append(k)
                print(k)
    return ret


oldlist = deepcopy(nowlist)
oldchara = sum(oldlist.values(), HuTao)
olddamage = oldchara.effect()


def calc(ar: list[artifacts], ard: list[artifacts]):
    for a in ar:
        out = {}
        for t, v in pred[a.enhanceCount].items():
            newa = deepcopy(a)
            newa.subValue = tuple(
                a.subValue[i] + t[i] * stdSubValue(a.subStats[i]) for i in range(4))
            # print(newa)
            newchara = oldchara + newa
            newchara -= oldlist[newa.part]
            newdamage = newchara.damage()
            out[newdamage] = out.get(newdamage, 0) + v
        out = {Effect2Weight(k): out[k] / 16**a.enhanceCount for k in sorted(out)}
        if len(out) == 1:
            plt.plot(out.keys(), out.values(), '+', label=f'{a.part}, {a.mainStat}')
        else:
            if a in ard:
                plt.plot(out.keys(), cumsum(list(out.values())), a.line, color=a.color, label=f'{a.part}, {a.mainStat}, {a.enhanceCount}')
            else:
                plt.plot(out.keys(), cumsum(list(out.values())), a.line, color=a.color, label=None)


if __name__ == '__main__':
    case = 1
    if case == 1:
        # print(testCase[0])
        # print(f'{pred = }')
        # print(f'{len(pred[5]) = }')
        case = ifcrit(testCase)
        print(len(case))
        calc(case, testCase)
        plt.vlines(Effect2Weight(olddamage), 0, 1)
        # legend(bbox_to_anchor=(0.7, 0), loc='lower left')
        plt.legend()
        plt.show()
    if case == 2:
        countEffective(oldlist.values(), HuTao)
