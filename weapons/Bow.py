from character import *


def Thundering_Pulse(chara: character) -> character:
    '''Lv. 1	Increases ATK by 20% and grants the might of the Thunder Emblem. At stack levels 1/2/3, the Thunder Emblem increases Normal Attack DMG by 12/24/40%. The character will obtain 1 stack of Thunder Emblem in each of the following scenarios: Normal Attack deals DMG (stack lasts 5s), casting Elemental Skill (stack lasts 10s); Energy is less than 100% (stack disappears when Energy is full). Each stack's duration is calculated independently.'''
    chara += weapons(608)
    chara.CRIT_DMG += 0.662
    chara.exATKs += 0.2
    chara.Bonus += 0.4
    return chara


def Rust(chara: character) -> character:
    '''Lv. 5	Increases Normal Attack DMG by 80% but decreases Charged Attack DMG by 10%.'''
    chara += weapons(510)
    chara.exATKs += 0.413
    chara.Bonus += 0.8
    return chara


def Slingshot(chara: character) -> character:
    '''Lv. 5	If a Normal or Charged Attack hits a target within 0.3s of being fired, increases DMG by 60%. Otherwise, decreases DMG by 10%.'''
    chara += weapons(354)
    chara.CRIT_Rate += 0.312
    chara.Bonus += 0.6
    return chara