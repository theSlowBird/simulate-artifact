from artifacts import Blizzard_Strayer
from character import artifacts, character
from weapons.Sword import Mistsplitter_Reforged, Amenoma_Kageuchi, Blackcliff_Longsword, Harbinger_of_Dawn

CHARACTER = 'Kamisato Ayaka'
WEAPONS = [
    Mistsplitter_Reforged,  # 雾切之回光
    Amenoma_Kageuchi,  # 天目影打刀
    Blackcliff_Longsword,  # 黑岩长剑
    Harbinger_of_Dawn  # 黎明神剑
]
ARTIFACT_SETS = [
    Blizzard_Strayer  # 冰风迷途的勇士
]
MAINS = {
    'Flower of Life': ['HP'],
    'Plume of Death': ['ATK'],
    'Sands of Eon': ['ATK%'],
    'Goblet of Eonothem': ['Cyro DMG Bonus'],
    'Circlet of Logos': ['CRIT DMG', 'ATK%'],
}
DEFAULT_ARTIFACTS = {
    'Flower of Life': artifacts('Flower of Life', 'HP'),
    'Plume of Death': artifacts('Plume of Death', 'ATK'),
    'Sands of Eon': artifacts('Sands of Eon', 'ATK%'),
    'Goblet of Eonothem': artifacts('Goblet of Eonothem', 'Cyro DMG Bonus'),
    'Circlet of Logos': artifacts('Circlet of Logos', 'CRIT DMG'),
}


def getChara() -> character:
    Ayaka = character(12858, 342, 784, 'Cyro')
    Ayaka.CRIT_DMG += .384
    Ayaka.rate = 2.0214
    Ayaka.Bonus += 0.18
    Ayaka.CRIT_Rate += 0.15
    Ayaka.BaseReactionBonus = 1.5
    Ayaka.reactionRatio = 0
    return Ayaka
