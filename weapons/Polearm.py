from character import *


def Staff_of_Homa(chara: character) -> None:
	"""Lv. 1	HP increased by 20%. Additionally, provides an ATK Bonus based on 0.8% of the wielder's Max HP. When the wielder's HP is less than 50%, this ATK Bonus is increased by an additional 1% of Max HP."""
	chara += weapons(608)
	chara.exHPs += 0.2
	chara.CRIT_DMG += 0.662
	chara.Homa = True


def Dragons_Bane(chara: character) -> None:
	"""Lv. 5	Increases DMG against opponents affected by Hydro or Pyro by 36%."""
	chara += weapons(454)
	chara.elementalMastery += 221
	chara.Bonus += 0.36


def Deathmatch(chara: character) -> None:
	"""Lv. 1	If there are at least 2 opponents nearby, ATK is increased by 16% and DEF is increased by 16%. If there are fewer than 2 opponents nearby, ATK is increased by 24%.
	对单"""
	chara += weapons(454)
	chara.CRIT_Rate += 0.368
	chara.exATKs += 0.24


def Primordial_Jade_Winged_Spear(chara: character) -> None:
	"""Lv. 1	On hit, increases ATK by 3.2% for 6s. Max 7 stacks. This effect can only occur once every 0.3s. While in possession of the maximum possible stacks, DMG dealt is increased by 12%."""
	chara += weapons(674)
	chara.CRIT_Rate += 0.221
	chara.exATKs += 0.032 * 7
	chara.Bonus += 0.12