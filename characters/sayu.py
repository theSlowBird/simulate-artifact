import math

from artifacts import Viridescent_Venerer
from character import artifacts, character
from weapons.Claymore import Rainslasher

CHARACTER = 'Sayu'
WEAPONS = [
    Rainslasher,  # 雨裁
]
ARTIFACT_SETS = [
    # Wanderers_Troupe2,  # 流浪大地的乐团2+翠绿之影2
    # ATK2,  # ATK2+翠绿之影2
    Viridescent_Venerer,  # 翠绿之影2
]
MAINS = {
    'Flower of Life': ['HP'],
    'Plume of Death': ['ATK'],
    'Sands of Eon': ['Elemental Mastery', 'ATK%'],
    'Goblet of Eonothem': ['Anemo DMG Bonus', 'Elemental Mastery', 'ATK%'],
    'Circlet of Logos': ['CRIT Rate', 'CRIT DMG', 'Elemental Mastery', 'ATK%', 'Healing Bonus'],
}
DEFAULT_ARTIFACTS = {
    'Flower of Life': artifacts('Flower of Life', 'HP'),
    'Plume of Death': artifacts('Plume of Death', 'ATK'),
    'Sands of Eon': artifacts('Sands of Eon', 'Elemental Mastery'),
    'Goblet of Eonothem': artifacts('Goblet of Eonothem', 'Elemental Mastery'),
    'Circlet of Logos': artifacts('Circlet of Logos', 'Elemental Mastery'),
}


class Sayu(character):
    def __init__(self, BaseHP: float, BaseATK: float, BaseDEF: float, element: str) -> None:
        super().__init__(BaseHP, BaseATK, BaseDEF, element)
        self.head = [self.effect, self.damage, self.cure]
        self.intro += 'Lv.12\n'

    # self.intro += 'Lv.13\n'

    def RATE(self) -> float:
        # return self.ATK() * (0.94 + self.elementalMastery * 0.002)
        return self.ATK() * (1.04 + self.elementalMastery * 0.002)

    # return self.ATK() * (1.11 + self.elementalMastery * 0.002)

    def cure(self) -> float:
        # return self.ATK() * 1.438 + 1100 + self.elementalMastery * 3
        return self.ATK() * 1.597 + 1280 + self.elementalMastery * 3

    # return self.ATK() * 1.697 + 1376 + self.elementalMastery * 3

    def damage(self) -> float:
        return self.RATE() * self.BONUS() * self.CRIT() * self.resistance() * self.defend()  # 伤害期望

    def effect(self) -> float:
        return math.sqrt(self.damage() * self.cure())


def getChara() -> Sayu:
    sayu = Sayu(11854, 244, 745, 'Anemo')
    sayu.elementalMastery += 96
    sayu.BaseReactionBonus = 1
    sayu.reactionRatio = 0
    return sayu
