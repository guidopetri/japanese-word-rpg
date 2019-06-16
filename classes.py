#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 3.6.4


import random
from game_enums import status_effect, player_classes


class enemy_word():

    def __init__(self, level):
        self.level = level
        self.exp_yield = self.level * random.randrange(5, 11)
        self.gold_yield = self.level * random.randrange(1, 4)
        self.health = self.level * random.randrange(2, 5)
        self.max_hp = self.health
        self.status = status_effect.normal
        self.alive = True
        self.words = []
        self.word_count = 0

    def pick_word(self, words_dict):

        # TODO: improve below lines to be more efficient

        if self.status == status_effect.normal:
            words = [x for y in words_dict.values() for x in y]
        elif self.status == status_effect.berserk:
            words = [x for y in words_dict.values() for x in y if len(x) > 10]
        elif self.status == status_effect.slow:
            words = [x for y in words_dict.values() for x in y if len(x) < 6]

        if self.words and self.words[-1] != ' ':
            self.words.append(' ')
        self.words.extend(random.choice(words))
        self.word_count += 1

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.alive = False
            return

        quarter_hp = int(self.max_hp / 4)

        if self.status == status_effect.normal:
            if self.health in range(quarter_hp, 2 * quarter_hp):
                print(" BERSERK!!")
                self.status = status_effect.berserk
        if self.status == status_effect.berserk:
            if self.health < quarter_hp:
                self.status = status_effect.slow
                print(" ..... slow .....")

    def print_word(self):
        print(self.words)


class PlayerCharacter():

    def __init__(self, player_name=None, player_class=None):
        from collections import defaultdict

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
        self.story_chapter = 1
        self.inventory = defaultdict(int)
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
            self.level_up()

    def gain_gold(self, amount):
        self.total_gold += int(amount * self.gold_multiplier)

    def level_up(self):
        print(" LEVEL UP!!")
        self.level += 1
        self.health = self.max_hp
        self.calculate_level_threshold()
        print(" NEXT LEVEL AT %s!!" % self.exp_threshold)
        self.calculate_score_multiplier()

    def calculate_score_multiplier(self):
        self.score_multiplier = 1.0 * (self.level ** 1.3)

    def calculate_level_threshold(self):
        self.exp_threshold = 43.65 * ((self.level + 1) ** 3)

    def score_points(self, amount):
        self.score += int(amount * self.score_multiplier)

    def toJSON(self):
        return self.__dict__


class Item():

    id_ = 0

    def __init__(self, name, price, is_use, is_special,
                 is_equip, desc, unlock_chapter):
        self.id = Item.id_
        Item.id_ += 1
        self.name = name
        self.price = price
        self.is_use = is_use
        self.is_special = is_special
        self.is_equip = is_equip
        self.desc = desc
        self.unlock_chapter = unlock_chapter

    def __eq__(self, other):
        return self.name == other

    def print_price(self):
        return '{}: $G{}'.format(self.name, self.price)
