from character import *


def Mistsplitter_Reforged(chara: character) -> character:
    '''Lv. 1	Gain a 12% Elemental DMG Bonus for all elements and receive the might of the Mistsplitter's Emblem. At stack levels 1/2/3, the Mistsplitter's Emblem provides a 8/16/28% Elemental DMG Bonus for the character's Elemental Type. The character will obtain 1 stack of Mistsplitter's Emblem in each of the following scenarios: Normal Attack deals Elemental DMG (stack lasts 5s), casting Elemental Burst (stack lasts 10s); Energy is less than 100% (stack disappears when Energy is full). Each stack's duration is calculated independently.'''
    chara += weapons(674)
    chara.CRIT_DMG += 0.441
    chara.Bonus += 0.4
    return chara


def Amenoma_Kageuchi(chara: character) -> character:
    '''Lv. 5	After casting an Elemental Skill, gain 1 Succession Seed. This effect can be triggered once every 5s. The Succession Seed lasts for 30s. Up to 3 Succession Seeds may exist simultaneously. After using an Elemental Burst, all Succession Seeds are consumed and after 2s, the character regenerates 12 Energy for each seed consumed.'''
    chara += weapons(454)
    chara.exATK += 0.551
    return chara


def Blackcliff_Longsword(chara: character) -> character:
    '''Lv. 1	After defeating an opponent, ATK is increased by 12% for 30s. This effect has a maximum of 3 stacks, and the duration of each stack is independent of the others.
    对单白板'''
    chara += weapons(565)
    chara.CRIT_DMG += 0.368
    return chara


def Harbinger_of_Dawn(chara: character) -> character:
    '''Lv. 5	When HP is above 90%, increases CRIT Rate by 28%.
    控血'''
    chara += weapons(401)
    chara.CRIT_DMG += 0.469
    chara.CRIT_Rate += 0.28
    return chara
