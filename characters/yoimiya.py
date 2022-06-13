from artifacts import Shimenawas_Reminiscence
from character import artifacts, character
from tools import formIfNumhalfk
from weapons.Bow import Thundering_Pulse, Rust, Slingshot

CHARACTER = 'Yoimiya'
WEAPONS = [
    Thundering_Pulse,  # 飞雷之弦振
    Rust,  # 弓藏
    Slingshot,  # 弹弓
]
ARTIFACT_SETS = [
    Shimenawas_Reminiscence  # 追忆之注连
]
MAINS = {
    'Flower of Life': ['HP'],
    'Plume of Death': ['ATK'],
    'Sands of Eon': ['Elemental Mastery', 'ATK%'],
    'Goblet of Eonothem': ['Pyro DMG Bonus'],
    'Circlet of Logos': ['CRIT Rate', 'CRIT DMG'],
}
DEFAULT_ARTIFACTS = {
    'Flower of Life': artifacts('Flower of Life', 'HP'),
    'Plume of Death': artifacts('Plume of Death', 'ATK'),
    'Sands of Eon': artifacts('Sands of Eon', 'Elemental Mastery'),
    'Goblet of Eonothem': artifacts('Goblet of Eonothem', 'Pyro DMG Bonus'),
    'Circlet of Logos': artifacts('Circlet of Logos', 'CRIT Rate'),
}


class Yoimiya(character):
    def __init__(self, BaseHP: float, BaseATK: float, BaseDEF: float, element: str) -> None:
        super().__init__(BaseHP, BaseATK, BaseDEF, element)
        self.YunJin = 2587 * (0.6834 + 0.075)  # 火水双岩
        if self.YunJin:
            self.Bonus += 0.3  # 三命+双岩
        self.intro += f'YunJin = {formIfNumhalfk(self.YunJin)}\n'

    def baseRateReaction(self) -> float:
        return self.ATK() * 1.6174 * (0.6359 + 1.2199 + 0.8282 * 2) + self.YunJin * 4 + (self.ATK() * 1.6174 * (0.6359 + 1.5859 + 1.8887) + self.YunJin * 3) * self.totalReactionBonus()

    def effect(self) -> float:
        return self.baseRateReaction() * self.BONUS() * self.CRIT() * self.resistance() * self.defend()  # 伤害期望


def getChara() -> Yoimiya:
    yoimiya = Yoimiya(10164, 323, 615, 'Pyro')
    yoimiya.CRIT_Rate += .192
    yoimiya.Bonus += 0.1
    yoimiya.BaseReactionBonus = 1.5
    yoimiya.reactionRatio = 1
    return yoimiya
