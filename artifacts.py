from character import *


def Artifacts(chara: character, artifact) -> None:
	chara.intro += artifact.__name__ + '\n'
	artifact(chara)


def Crimson_Witch_of_Flames(chara: character) -> None:
	"""
	Crimson Witch of Flames
	2-Piece Set:	Pyro DMG Bonus +15%
	4-Piece Set:	Increases Overloaded and Burning DMG by 40%. Increases Vaporize and Melt DMG by 15%. Using Elemental Skill increases the 2-Piece Set Bonus by 50% of its starting value for 10s. Max 3 stacks.
	{'Sands of Eon, HP%': 0.4525, 'Sands of Eon, Elemental Mastery': 0.5475}"""
	chara.Bonus += 0.225
	chara.exReactionBonus += 0.15


def Wanderers_Troupe2(chara: character) -> None:
	"""
	Wanderer's Troupe
	2-Piece Set:	Increases Elemental Mastery by 80.

	Crimson Witch of Flames
	2-Piece Set:	Pyro DMG Bonus +15%

	{'Sands of Eon, Elemental Mastery': 0.4225, 'Sands of Eon, HP%': 0.5775}"""
	chara.Bonus += 0.15
	chara.elementalMastery += 80


def Shimenawas_Reminiscence(chara: character) -> None:
	"""
	Shimenawa's Reminiscence
	2-Piece Set:	ATK +18%.
	4-Piece Set:	When casting an Elemental Skill, if the character has 15 or more Energy, they lose 15 Energy and Normal/Charged/Plunging Attack DMG is increased by 50% for 10s. This effect will not trigger again during that duration.

	{'Sands of Eon, Elemental Mastery': 0.785, 'Sands of Eon, HP%': 0.215}"""
	chara.exATKs += 0.18
	chara.Bonus += 0.5


def Blizzard_Strayer(chara: character) -> None:
	"""
	Blizzard Strayer
	2-Piece Set:	Cryo DMG Bonus +15%
	4-Piece Set:	When a character attacks an opponent affected by Cryo, their CRIT Rate is increased by 20%. If the opponent is Frozen, CRIT Rate is increased by an additional 20%."""
	chara.Bonus += 0.15
	chara.CRIT_Rate += 0.4


def ATK2(chara: character) -> None:
	chara.exATKs += 0.18
	chara.Bonus += 0.15


def Viridescent_Venerer(chara: character) -> None:
	"""
	2-Piece Set:	Anemo DMG Bonus +15%
	4-Piece Set:	Increases Swirl DMG by 60%. Decreases opponent's Elemental RES to the element infused in the Swirl by 40% for 10s."""
	chara.Bonus += 0.15


def Berserker4(chara: character) -> None:
	"""
	2-Piece Set:	CRIT Rate +12%
	4-Piece Set:	When HP is below 70%, CRIT Rate increases by an additional 24%."""
	artifacts.modifyStar(4)
	# artifacts.five = 'Sands of Eon'
	artifacts.five = 'Goblet of Eonothem'
	# artifacts.five = 'Circlet of Logos'
	chara.intro += f'{artifacts.five = }\n'
	chara.CRIT_Rate += 0.36


def Berserker5(chara: character) -> None:
	"""
	2-Piece Set:	CRIT Rate +12%
	4-Piece Set:	When HP is below 70%, CRIT Rate increases by an additional 24%."""
	chara.CRIT_Rate += 0.36


def Resolution_of_Sojourner4(chara: character) -> None:
	"""
	2-Piece Set:	ATK +18%.
	4-Piece Set:	Increases Charged Attack CRIT Rate by 30%."""
	artifacts.modifyStar(4)
	# artifacts.five = 'Sands of Eon'
	artifacts.five = 'Goblet of Eonothem'
	# artifacts.five = 'Circlet of Logos'
	chara.intro += f'{artifacts.five = }\n'
	chara.exATKs += 0.18
	chara.CRIT_Rate += 0.3


def Emblem_of_Severed_Fate(chara: character) -> None:
	"""2-Piece Set:	Energy Recharge +20%
	4-Piece Set:	Increases Elemental Burst DMG by 25% of Energy Recharge. A maximum of 75% bonus DMG can be obtained in this way."""
	chara.EnergyRecharge += 0.2
	'''剩下的去pram做'''


def Echoes_of_an_Offering(chara: character) -> None:
	"""2-Piece Set:	ATK +18%.
	4-Piece Set:	When Normal Attacks hit opponents, there is a 36% chance that it will trigger Valley Rite, which will increase Normal Attack DMG by 70% of ATK. This effect will be dispelled 0.05s after a Normal Attack deals DMG. If a Normal Attack fails to trigger Valley Rite, the odds of it triggering the next time will increase by 20%. This trigger can occur once every 0.2s."""
	chara.exATKs += 0.18
	chara.addRate(0.3)
