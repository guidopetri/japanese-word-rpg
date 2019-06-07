#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 3.6.4


import json
import classes
import os


def load_words():
    with open('wordsLen.ini', 'r') as f:
        all_words = json.load(f)

    return all_words


def load_player():
    if os.path.exists('player.ini'):
        with open('player.ini', 'r') as f:
            data = json.load(f)
    else:
        data = {}

    # name = input('what's your name?\n')
    name = 'Sid'
    if name in data:
        player = classes.PlayerCharacter(player_dict=data[name])
    else:
        print("player doesn't exist")
        player_class = input("what's your class?\n")
        player = classes.PlayerCharacter(player_name=name,
                                         player_class=player_class)

    return data, player


def save_player(player_data, player):
    player_data[player.name] = player.toJSON()

    with open('player.ini', 'w') as f:
        json.dump(player_data, f)

    return
