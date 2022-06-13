from artifacts import Crimson_Witch_of_Flames
from character import artifacts, character
from weapons.Polearm import Staff_of_Homa

CHARACTER = 'Hu Tao'
WEAPONS = [
    Staff_of_Homa,  # 护摩之杖
    # Dragons_Bane,  # 匣里灭辰
    # Deathmatch  # 决斗枪
]
ARTIFACT_SETS = [
    Crimson_Witch_of_Flames,  # 炽烈的炎之魔女
    # Wanderers_Troupe2,  # 流浪大地的乐团2+炽烈的炎之魔女2
    # Shimenawas_Reminiscence  # 追忆之注连
    # Berserker4,  # 战狂
    # Resolution_of_Sojourner4,  # 行者之心
]
MAINS = {
    'Flower of Life': ['HP'],
    'Plume of Death': ['ATK'],
    'Sands of Eon': ['Elemental Mastery', 'HP%'],
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


class Hutao(character):
    def __init__(self, BaseHP: float, BaseATK: float, BaseDEF: float, element: str) -> None:
        super().__init__(BaseHP, BaseATK, BaseDEF, element)

    def ATK(self) -> float:
        if self.Homa:
            return self.BaseATK * (1 + self.exATKs) + self.exATK + self.HP() * (0.0626 + 0.018)
        else:
            return self.BaseATK * (1 + self.exATKs) + self.exATK + self.HP() * 0.0626


def getChara() -> Hutao:
    HuTao = Hutao(15552, 106, 876, 'Pyro')
    HuTao.CRIT_DMG += .384
    HuTao.Bonus += 0.33
    HuTao.Homa = False
    HuTao.rate = 2.4257
    HuTao.BaseReactionBonus = 1.5
    HuTao.reactionRatio = 1
    return HuTao
