#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 3.6.4


import random
from game_enums import status_effect, use_items, player_classes


class enemy_word():
    def __init__(self, level):
        self.level = level
        self.exp_yield = self.level * random.randrange(5, 11)
        self.gold_yield = self.level * random.randrange(1, 4)
        self.health = self.level * random.randrange(2, 5)
        self.max_hp = self.health
        self.status = status_effect.normal
        self.alive = True
        return

    def pick_word(self, words_dict):
        all_words = [x for y in words_dict.values() for x in y]
        long_words = [x for y in words_dict.values() for x in y if len(x) > 10]
        short_words = [x for y in words_dict.values() for x in y if len(x) < 6]
        if self.status == status_effect.normal:
            self.word = random.choice(all_words)
        elif self.status == status_effect.berserk:
            self.word = random.choice(long_words)
        elif self.status == status_effect.slow:
            self.word = random.choice(short_words)
        return

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.alive = False
            return
        if (self.health < self.max_hp / 2) and (self.health > self.max_hp / 4) and (self.status == status_effect.normal):  # noqa
            print(" BERSERK!!")
            self.status = status_effect.berserk
        if (self.health < self.max_hp / 4) and (self.status == status_effect.berserk):  # noqa
            self.status = status_effect.slow
            print(" ..... slow .....")
        return

    def print_word(self):
        print(self.word)
        return


class PlayerCharacter():
    def __init__(self, player_name=None, player_class=None, player_dict=None):
        if player_dict is None and player_name is not None:
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
            self.status = status_effect.normal
            self.status_duration = 0
            self.difficulty = 0.93
            self.init_inventory()
            self.calculate_class_bonuses()
        elif player_dict is not None and player_name is None:
            self.name = player_dict['name']
            self.char_class = player_dict['char_class']
            self.health = player_dict['health']
            self.max_hp = player_dict['max_hp']
            self.level = player_dict['level']
            self.kills = player_dict['kills']
            self.score = player_dict['score']
            self.total_exp = player_dict['total_exp']
            self.alive = player_dict['alive']
            self.total_gold = player_dict['total_gold']
            self.gold_multiplier = player_dict['gold_multiplier']
            self.dmg_multiplier = player_dict['dmg_multiplier']
            self.status = player_dict['status']
            self.status_duration = player_dict['status_duration']
            self.inventory = player_dict['inventory']
            self.difficulty = player_dict['difficulty']
        self.calculate_score_multiplier()
        self.calculate_level_threshold()
        return

    def calculate_class_bonuses(self):
        if self.char_class == player_classes.fighter:
            self.max_hp = int(self.health * 1.1)
            self.health = int(self.health * 1.1)
            self.dmg_multiplier *= 1.1
        elif self.char_class == player_classes.rogue:
            self.gold_multiplier *= 1.2
        elif self.char_class == player_classes.wizard:
            self.dmg_multiplier *= 1.3
        return

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.alive = False
        return

    def gain_exp(self, amount):
        self.total_exp += amount
        if self.exp_threshold - self.total_exp <= 0:
            self.level_up()
        return

    def gain_gold(self, amount):
        self.total_gold += int(amount * self.gold_multiplier)
        return

    def level_up(self):
        print(" LEVEL UP!!")
        self.level += 1
        self.health = self.max_hp
        self.calculate_level_threshold()
        print(" NEXT LEVEL AT %s!!" % self.exp_threshold)
        self.calculate_score_multiplier()
        return

    def calculate_score_multiplier(self):
        self.score_multiplier = 1.0 * (self.level ** 1.3)
        return

    def calculate_level_threshold(self):
        self.exp_threshold = 43.65 * ((self.level + 1) ** 3)
        return

    def score_points(self, amount):
        self.score += int(amount * self.score_multiplier)
        return

    def toJSON(self):
        return_dict = {'name': self.name,
                       'char_class': self.char_class,
                       'health': self.health,
                       'max_hp': self.max_hp,
                       'level': self.level,
                       'kills': self.kills,
                       'score': self.score,
                       'total_exp': self.total_exp,
                       'alive': self.alive,
                       'total_gold': self.total_gold,
                       'gold_multiplier': self.gold_multiplier,
                       'dmg_multiplier': self.dmg_multiplier,
                       'inventory': self.inventory,
                       'status': self.status,
                       'status_duration': self.status_duration,
                       'difficulty': self.difficulty
                       }
        return return_dict

    def init_inventory(self):
        self.inventory = {}
        for item in use_items:
            self.inventory[item] = 0
        return
