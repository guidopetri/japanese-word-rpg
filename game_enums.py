#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 3.6.4


from enum import Enum, IntEnum
import pygame


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


# class use_items(Enum):
#     # item name = identifier
#     potion = 0
#     coffee = 1
#     poison_flask = 2
#     protein_shake = 3
#     sharpening_oil = 4
#     energy_bar = 5


# class _item_prices(dict):
#     potion = 10
#     coffee = 50
#     poison_flask = 50
#     protein_shake = 50
#     sharpening_oil = 50
#     energy_bar = 50

#     @classmethod
#     def __getitem__(cls, item):
#         return getattr(cls, item)


class colors(Enum):
    offwhite = pygame.Color(230, 230, 230)
    offblack = pygame.Color(20, 20, 20)
    offblue = pygame.Color(50, 50, 255)
    offred = pygame.Color(255, 50, 50)
    bgyellow = pygame.Color(252, 232, 131)
    bgblue = pygame.Color(131, 131, 252)
    white = pygame.Color(255, 255, 255)
    black = pygame.Color(0, 0, 0)
    magenta = pygame.Color(255, 0, 255)


# item_prices = _item_prices()
# special_items = ['hero trophy']
