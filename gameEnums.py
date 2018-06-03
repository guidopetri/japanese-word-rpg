#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python 3.6.4

from enum import Enum

class StatusEffect(Enum):
	normal=1
	berserk=2
	slow=3
	fast=4
	givePoison=5
	hpUp=6
	dmgUp=7
	staminaUp=8

class playerClasses(Enum):
	fighter='fighter'
	rogue='rogue'
	wizard='wizard'
	
class useItems(Enum):
	#item name=(identifier,price)
	potion=('1','10')
	coffee=('2','50')
	poison_flask=('3','50')
	protein_shake=('4','50')
	sharpening_oil=('5','50')
	energy_bar=('6','50')
