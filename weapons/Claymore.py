from character import *


def Rainslasher(chara: character) -> character:
    '''Lv. 5	Increases DMG against opponents affected by Hydro or Electro by 36%.'''
    chara += weapons(510)
    chara.elementalMastery += 165
    chara.Bonus += 0.36
    return chara