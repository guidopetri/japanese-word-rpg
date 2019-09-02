#!/usr/bin/env python3

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
    add_protect = 9
    del_protect = 10
    sub_protect = 11
    perm_protect = 12


class player_classes(Enum):
    fighter = 'fighter'
    rogue = 'rogue'
    wizard = 'wizard'


class colors(Enum):
    offwhite = pygame.Color(230, 230, 230)
    offblack = pygame.Color(20, 20, 20)
    offblue = pygame.Color(50, 50, 255)
    offred = pygame.Color(255, 50, 50)
    brightgreen = pygame.Color(50, 255, 50)
    deepgreen = pygame.Color(50, 150, 50)
    bgyellow = pygame.Color(252, 232, 131)
    bgblue = pygame.Color(131, 131, 252)
    white = pygame.Color(255, 255, 255)
    black = pygame.Color(0, 0, 0)
    magenta = pygame.Color(255, 0, 255)
    offpurple = pygame.Color(204, 136, 153)
    riverblue = pygame.Color(100, 100, 200)
