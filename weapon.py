from character import *
from weapons.Bow import *
from weapons.Claymore import *
from weapons.Polearm import *
from weapons.Sword import *


def Weapons(chara: character, weapons) -> character:
    chara.intro += weapons.__name__ + '\n'
    return weapons(chara)
