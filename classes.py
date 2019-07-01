#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 3.6.4

import random
from game_enums import status_effect, player_classes


class enemy_word(object):

    def __init__(self, level):
        from collections import defaultdict
        self.level = level or 1
        self.exp_yield = self.level * random.randrange(5, 11)
        self.gold_yield = self.level * random.randrange(1, 4)
        self.health = self.level * random.randrange(2, 5)
        self.max_hp = self.health
        self.status = defaultdict(int)
        self.alive = True
        self.words = []
        self.word_count = 0
        self.atk_ivl = random.randrange(3, 8) // self.level

    def pick_word(self, words_dict):

        if status_effect.berserk in self.status:
            trimmed = [words_dict[key] for key in words_dict if key > 10]
        elif status_effect.slow in self.status:
            trimmed = [words_dict[key] for key in words_dict if key < 6]
        else:
            trimmed = words_dict.values()

        words = sum(trimmed, [])

        if self.words and self.words[-1] != ' ':
            self.words.append(' ')
        self.words.extend(random.choice(words))
        self.word_count += 1

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.alive = False
            return

        quarter_hp = self.max_hp // 4

        if self.status[status_effect.berserk]:
            if self.health < quarter_hp:
                self.status[status_effect.berserk] = 0
                self.status[status_effect.slow] = -1
                print(" ..... slow .....")
        elif self.health in range(quarter_hp, 2 * quarter_hp):
            print(" BERSERK!!")
            self.status[status_effect.berserk] = -1

    def print_word(self):
        print(self.words)


class PlayerCharacter(object):

    def __init__(self, player_name=None, player_class=None):
        from collections import defaultdict, OrderedDict

        self.name = player_name
        self.char_class = player_class
        self.health = 10
        self.max_hp = 10
        self.level = 1
        self.kills = 0
        self.score = 0
        self.total_exp = 0
        self.alive = True
        self.total_gold = 0
        self.gold_multiplier = 1.0
        self.dmg_multiplier = 1.0
        self.status = defaultdict(int)
        self.difficulty = 0.93
        self.story_chapter = 1
        self.has_ship = False
        self.level_pending = False
        self.inventory = defaultdict(int)
        self.equipment = OrderedDict([('head', None),
                                      ('body', None),
                                      ('legs', None),
                                      ('weapon', None)
                                      ])
        self.held_items = ['potion',
                           'poison flask',
                           'coffee',
                           None,
                           None,
                           None]
        self.calculate_class_bonuses()
        self.calculate_score_multiplier()
        self.calculate_level_threshold()

    def calculate_class_bonuses(self):
        if self.char_class == player_classes.fighter:
            self.max_hp = int(self.health * 1.1)
            self.health = int(self.health * 1.1)
            self.dmg_multiplier *= 1.1
        elif self.char_class == player_classes.rogue:
            self.gold_multiplier *= 1.2
        elif self.char_class == player_classes.wizard:
            self.dmg_multiplier *= 1.3

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.alive = False

    def gain_exp(self, amount):
        self.total_exp += amount
        if self.exp_threshold - self.total_exp <= 0:
            self.level_pending = True

    def gain_gold(self, amount):
        self.total_gold += int(amount * self.gold_multiplier)

    def level_up(self):
        self.level_pending = False

        self.level += 1

        hp_increase = random.randrange(1, 4)
        self.max_hp += hp_increase
        self.health = self.max_hp

        self.calculate_level_threshold()
        self.calculate_score_multiplier()

        stats_delta = {'level': 1,
                       'health': hp_increase}
        return stats_delta

    @property
    def stats(self):
        # tuple of stat name, then stat value
        stats = [('level', self.level),
                 ('health', self.health),
                 ]
        return stats

    def calculate_score_multiplier(self):
        self.score_multiplier = 1.0 * (self.level ** 1.3)

    def calculate_level_threshold(self):
        self.exp_threshold = 43.65 * ((self.level + 1) ** 3)

    def score_points(self, amount):
        self.score += int(amount * self.score_multiplier)


class Item(object):

    id_ = 0

    def __init__(self, name, price, is_use, is_special,
                 is_equip, desc, unlock_chapter, equip_type=None):
        self.id = Item.id_
        Item.id_ += 1
        self.name = name
        self.price = price
        self.is_use = is_use
        self.is_special = is_special
        self.is_equip = is_equip
        self.desc = desc
        self.unlock_chapter = unlock_chapter
        self.equip_type = equip_type

    def __eq__(self, other):
        return self.name == other

    def print_price(self):
        name = self.name
        if self.name == 'dyslexia potion':
            name = ''.join(random.sample(name, k=len(name)))
        return '{}: $G{}'.format(name, self.price)


class LocationType(object):

    def __init__(self, name, block_mv, ship_mv, block_fov, level):
        self.name = name
        self.block_mv = block_mv
        self.ship_mv = ship_mv
        self.block_fov = block_fov
        self.level = level


class MapLocation(object):

    def __init__(self, kind):
        self.kind = kind
