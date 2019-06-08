#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 3.6.4

from enum import Enum, IntEnum


class status_effect(IntEnum):
    normal = 1
    berserk = 2
    slow = 3
    fast = 4
    give_poison = 5
    hp_up = 6
    dmg_up = 7
    stamina_up = 8


class player_classes(Enum):
    fighter = 'fighter'
    rogue = 'rogue'
    wizard = 'wizard'


class use_items(Enum):
    # item name = (identifier, price)
    potion = ('1', '10')
    coffee = ('2', '50')
    poison_flask = ('3', '50')
    protein_shake = ('4', '50')
    sharpening_oil = ('5', '50')
    energy_bar = ('6', '50')
