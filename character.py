from copy import deepcopy
from math import log2
from random import random

from sympy import flatten

from tools import *

STAT_NAME = {
    'HP': 6,
    'ATK': 6,
    'DEF': 6,
    'HP%': 4,
    'ATK%': 4,
    'DEF%': 4,
    'Elemental Mastery': 4,
    'Energy Recharge': 4,
    'CRIT Rate': 3,
    'CRIT DMG': 3,
}
VALUE = {
    'ATK': 311.0,
    'HP': 4780.0,
    'DEF': 370.4,
    'ATK%': 0.466,
    'HP%': 0.466,
    'DEF%': 0.583,
    'CRIT Rate': 0.311,
    'CRIT DMG': 0.622,
    'Healing Bonus': 0.359,
    'Elemental Mastery': 186.5,
    'Energy Recharge': 0.518,
    'Physical DMG Bonus': 0.583,
    'Hydro DMG Bonus': 0.466,
    'Anemo DMG Bonus': 0.466,
    'Electro DMG Bonus': 0.466,
    'Cyro DMG Bonus': 0.466,
    'Geo DMG Bonus': 0.466,
    'Pyro DMG Bonus': 0.466,
}

VALUE4 = {
    'ATK': 232,
    'HP': 3571,
    'ATK%': 0.348,
    'HP%': 0.348,
    'DEF%': 0.435,
    'CRIT Rate': 0.232,
    'CRIT DMG': 0.464,
    'Healing Bonus': 0.268,
    'Elemental Mastery': 139,
    'Energy Recharge': 0.387,
    'Physical DMG Bonus': 0.435,
    'Hydro DMG Bonus': 0.348,
    'Anemo DMG Bonus': 0.348,
    'Electro DMG Bonus': 0.348,
    'Cyro DMG Bonus': 0.348,
    'Geo DMG Bonus': 0.348,
    'Pyro DMG Bonus': 0.348,
}

PART = ['Flower of Life',
        'Plume of Death',
        'Sands of Eon',
        'Goblet of Eonothem',
        'Circlet of Logos',
        ]

STATS: list[str] = flatten([[k] * v for k, v in STAT_NAME.items()])


def generateValue() -> list[float]:
    ret = [7 + int(random() * 4) for _ in range(4)]
    minEnhance = 4 if artifacts.star == 5 else 2
    for i in range(minEnhance):
        ret[int(random() * 4)] += 7 + int(random() * 4)
    if random() < 0.2:
        ret[int(random() * 4)] += 7 + int(random() * 4)
    return [i / 10 for i in ret]


def stdSubValue(sub: str) -> float:
    if artifacts.star == 5:
        if sub in ['HP', 'ATK', 'DEF']:
            return VALUE[sub] / 16
        return VALUE[sub] / 8
    elif artifacts.star == 4:
        if sub in ['HP', 'ATK', 'DEF']:
            return VALUE[sub] / 20
        return VALUE[sub] / 10


def generateSuit() -> int:
    """不妨认为60%都是可用4+1套装"""
    return random() < 0.6


def generatePart() -> str:
    return PART[int(random() * 5)]


def generateMainStat(part: str) -> str:
    if part == 'Flower of Life':
        return 'HP'
    if part == 'Plume of Death':
        return 'ATK'
    if part == 'Sands of Eon':
        # 26.67 : 26.67 : 26.67 : 10 : 10
        x = random()
        if x < 0.1:
            return 'Elemental Mastery'
        if x < 0.2:
            return 'Energy Recharge'
        return ['ATK%', 'DEF%', 'HP%'][int(random() * 3)]
    if part == 'Goblet of Eonothem':
        # 21.25 : 21.25 : 20 : 2.5 : 5*7
        x = random() * 100
        if x < 21.25:
            return 'ATK%'
        if x < 42.5:
            return 'HP%'
        if x < 62.5:
            return 'DEF%'
        if x < 65:
            return 'Elemental Mastery'
        return ['Physical DMG Bonus', 'Hydro DMG Bonus', 'Anemo DMG Bonus', 'Electro DMG Bonus', 'Cyro DMG Bonus',
                'Geo DMG Bonus', 'Pyro DMG Bonus'][int(random() * 7)]
    if part == 'Circlet of Logos':
        x = random() * 100
        if x < 4:
            return 'Elemental Mastery'
        if x < 34:
            return ['CRIT DMG', 'Healing Bonus', 'CRIT Rate'][int(random() * 3)]
        return ['ATK%', 'HP%', 'DEF%'][int(random() * 3)]


def generateSubStats(mainStat: str) -> list[str]:
    stats = []
    while len(stats) < 4:
        x = int(random() * 44)
        if STATS[x] not in stats + [mainStat]:
            stats.append(STATS[x])
    return stats


class artifacts:
    five = None
    star = 5
    mainVALUE = VALUE

    def __init__(self, part: str, mainStat: str, subStats: list[str] = [], subValue: list[float] = [], enhanceCount=0, sub: list[str] = []) -> None:
        self.part = part
        self.mainStat = mainStat
        self.mainValue = artifacts.mainVALUE[mainStat]
        self.enhanceCount = enhanceCount
        if sub:
            self.sub = sub
            self.subStats = []
            self.subValue = []
            self.subs = []
            for x in sub:
                y = x.split('+')
                if y[1][-1] == '%':
                    v = float(y[1][:-1]) / 100
                    if y[0] in ['HP', 'ATK', 'DEF']:
                        s = y[0] + '%'
                    else:
                        s = y[0]
                else:
                    v = int(y[1])
                    s = y[0]
                self.subStats.append(s)
                self.subValue.append(v)
                self.subs.append((s, v))
        else:
            self.subStats = subStats
            if not subStats:
                # print('no substats...')
                return
            if subValue:
                self.subValue = subValue
            else:
                self.subValue = [
                    x * y for x, y in zip(generateValue(), [stdSubValue(x) for x in subStats])]
            self.subs = zip(self.subStats, self.subValue)
            self.sub = list([f"{k.replace('%', '')}+{formIfNum01(v)}" for k, v in self.subs])
            # print(self.sub)

    def __repr__(self) -> str:
        if self.subStats:
            return f'\n{self.part}\n{self.mainStat} : {self.mainValue},\n{self.subStats[0]} : {self.subValue[0]},\n{self.subStats[1]} : {self.subValue[1]},\n{self.subStats[2]} : {self.subValue[2]},\n{self.subStats[3]} : {self.subValue[3]}.\n'
        else:
            return f'\n{self.part}\n{self.mainStat} : {self.mainValue}.\n'

    def stats(self) -> str:
        return f'{self.mainStat} {self.subStats}'

    @classmethod
    def modifyStar(cls, star: int) -> None:
        artifacts.star = star
        if star == 5:
            artifacts.mainVALUE = VALUE
        elif star == 4:
            artifacts.mainVALUE = VALUE4


class weapons:
    def __init__(self, BaseATK: float) -> None:
        self.BaseATK = BaseATK


class character:
    def __init__(self, BaseHP: float, BaseATK: float, BaseDEF: float, element: str) -> None:
        self.BaseHP = BaseHP
        self.BaseATK = BaseATK
        self.BaseDEF = BaseDEF
        self.element = element
        self.Bonus = 0
        self.CRIT_Rate = 0.05
        self.CRIT_DMG = 0.5
        self.EnergyRecharge = 1
        self.elementalMastery = 0
        self.healingBonus = 0
        self.exReactionBonus = 1
        self.exATK = 0
        self.exHP = 0
        self.exDEF = 0
        self.exATKs = 0
        self.exHPs = 0
        self.exDEFs = 0

        self.intro: str = ''
        self.rate = 0
        self.reactionRatio = 0
        self.BaseReactionBonus = 0
        self.head = [self.effect, self.bigdamage]

    def __add__(self, other):
        ret = deepcopy(self)
        ret += other
        return ret

    def __iadd__(self, other):
        if isinstance(other, weapons):
            self.BaseATK += other.BaseATK
        if isinstance(other, artifacts):
            if other.mainStat.find('Bonus') != -1:
                if self.element in other.mainStat:
                    self.Bonus += other.mainValue
            else:
                self += (other.mainStat, other.mainValue)
            for i in range(len(other.subStats)):
                self += (other.subStats[i], other.subValue[i])
        if isinstance(other, tuple):
            if other[0] == 'ATK':
                self.exATK += other[1]
            if other[0] == 'HP':
                self.exHP += other[1]
            if other[0] == 'DEF':
                self.exDEF += other[1]
            if other[0] == 'ATK%':
                self.exATKs += other[1]
            if other[0] == 'HP%':
                self.exHPs += other[1]
            if other[0] == 'DEF%':
                self.exDEFs += other[1]
            if other[0] == 'CRIT Rate':
                self.CRIT_Rate += other[1]
            if other[0] == 'CRIT DMG':
                self.CRIT_DMG += other[1]
            if other[0] == 'Healing Bonus':
                self.healingBonus += other[1]
            if other[0] == 'Elemental Mastery':
                self.elementalMastery += other[1]
            if other[0] == 'Energy Recharge':
                self.EnergyRecharge += other[1]
        return self

    def __sub__(self, other: artifacts):
        ret = deepcopy(self)
        ret -= other
        return ret

    def __isub__(self, other: artifacts):
        if isinstance(other, artifacts):
            if other.mainStat.find('Bonus') != -1:
                if self.element in other.mainStat:
                    self.Bonus += -other.mainValue
            else:
                self += (other.mainStat, -other.mainValue)
            for i in range(len(other.subStats)):
                self += (other.subStats[i], -other.subValue[i])
            return self

    def HP(self) -> float:
        return self.BaseHP * (1 + self.exHPs) + self.exHP

    def ATK(self) -> float:
        return self.BaseATK * (1 + self.exATKs) + self.exATK

    def RATE(self) -> float:
        return self.ATK() * self.rate

    def BONUS(self) -> float:
        return 1 + self.Bonus

    def CRIT(self) -> float:
        def real_CRIT_Rate():
            if self.CRIT_Rate > 1:
                return 1
            if self.CRIT_Rate < 0:
                return 0
            return self.CRIT_Rate
        return 1 + real_CRIT_Rate() * self.CRIT_DMG

    def reaction(self) -> float:
        return self.reactionRatio * self.totalReactionBonus() + 1 - self.reactionRatio

    def ReactionBonus(self):
        return self.exReactionBonus + 2.78 * self.elementalMastery / (1400 + self.elementalMastery)

    def totalReactionBonus(self):
        return self.ReactionBonus() * self.BaseReactionBonus

    @staticmethod
    def resistance() -> float:
        return 0.9

    @staticmethod
    def defend() -> float:
        return 0.5

    def effect(self) -> float:
        return self.RATE() * self.BONUS() * self.CRIT() * self.reaction() * self.resistance() * self.defend()  # 伤害期望

    def bigdamage(self) -> float:
        return self.effect() / self.CRIT() * (1 + self.CRIT_DMG)  # 大数字

    def __repr__(self) -> str:
        return f'{self.BaseHP = }, {self.HP() = }, {self.exHPs = }, {self.exHP = }\n{self.BaseATK = }, {self.ATK() = }, {self.exATKs = }, {self.exATK = }\n{self.BaseDEF = }\n{self.element = }, {self.elementalMastery = }\n{self.Bonus = }\n{self.CRIT_Rate = }, {self.CRIT_DMG = }\n{self.effect() = }, {Effect2Weight(self.effect()) = }\n{self.bigdamage() = }\n'


DOUBLEW = 31
default_dmg = 1


def setDEFAULT_DMG(dmg: float) -> float:
    global default_dmg
    default_dmg = dmg
    return default_dmg


def Effect2Weight(damage: float, rel: float = None) -> float:
    if rel is None:
        rel = default_dmg
    return DOUBLEW * (log2(damage) - log2(rel))


def Weight2Effect(weight: float, rel: float = None) -> float:
    if rel is None:
        rel = default_dmg
    return rel * 2**(weight / DOUBLEW)


def countEffective(case: list[artifacts], chara: character):
    ret = []
    charaw = sum(case, chara)
    damage = charaw.effect()
    for v in case:
        raw_chara = charaw - v
        ret.append(Effect2Weight(raw_chara.effect(), damage))
        # print(ret[-1])
    for v in case:
        v.mainValue = 0
        raw_chara = charaw - v
        v.mainValue = artifacts.mainVALUE[v.mainStat]
        ret.append(Effect2Weight(raw_chara.effect(), damage))
        # print(ret[-1])
    return ret
