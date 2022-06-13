import numpy as np

from artifacts import Emblem_of_Severed_Fate
from character import artifacts, character
from weapons.Polearm import Primordial_Jade_Winged_Spear

CHARACTER = 'Raiden Shogun'
WEAPONS = [
    Primordial_Jade_Winged_Spear
]
ARTIFACT_SETS = [
    Emblem_of_Severed_Fate
]
MAINS = {
    'Flower of Life': ['HP'],
    'Plume of Death': ['ATK'],
    'Sands of Eon': ['Energy Recharge'],
    'Goblet of Eonothem': ['ATK%'],
    'Circlet of Logos': ['CRIT Rate', 'CRIT DMG'],
}
DEFAULT_ARTIFACTS = {
    'Flower of Life': artifacts('Flower of Life', 'HP'),
    'Plume of Death': artifacts('Plume of Death', 'ATK'),
}


class Shogun(character):
    def __init__(self, BaseHP: float, BaseATK: float, BaseDEF: float, element: str) -> None:
        super().__init__(BaseHP, BaseATK, BaseDEF, element)
        self.head = [self.effect, self.damage, self.charge]

    def BONUS(self) -> float:
        return 1 + self.Bonus + min(self.EnergyRecharge, 3) * 0.25 + (self.EnergyRecharge - 1) * 0.4

    def charge(self) -> float:
        return 2.5 * (0.6 * (self.EnergyRecharge - 1) + 1) * 5

    def damage(self) -> float:
        return self.RATE() * self.BONUS() * self.CRIT() * self.resistance() * self.defend()  # 伤害期望

    def effect(self) -> float:
        return np.exp(np.average(np.log(np.array([self.damage(), self.charge()])), weights=(1, 1)))


def getChara() -> Shogun:
    shogun = Shogun(12907, 337, 789, 'Electro')
    shogun.EnergyRecharge += 0.32
    shogun.BaseReactionBonus = 1
    shogun.reactionRatio = 0
    shogun.Bonus += 0.003 * 90
    shogun.rate = 7.21 + 0.07 * 60
    return shogun
