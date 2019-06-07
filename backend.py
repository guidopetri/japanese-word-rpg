#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 3.6.4


import json
import classes


def load_words():
    with open('wordsLen.ini', 'r') as f:
        all_words = json.loads(f.read())
    return all_words


def load_player():
    try:
        with open('player.ini', 'r') as f:
            player_data = json.loads(f.read())

        print([x for x in player_data.keys()], sep=' ', end='\n')
        player_name = 'Sid'  # input("who are you?\n")
        try:
            player = classes.PlayerCharacter(playerDict=player_data[player_name])  # noqa
        except KeyError:
            print("player doesn't exist")
            player_name = input("what's your name?\n")
            player_class = input("what's your class?\n")
            player = classes.PlayerCharacter(playerName=player_name,
                                             playerClass=player_class)
    except FileNotFoundError:
        player_data = {}
        player_name = input("what's your name?\n")
        player = classes.PlayerCharacter(playerName=player_name)
    return player_data, player


def save_player(player_data, player):
    player_data[player.name] = player.toJSON()

    with open('player.ini', 'w') as f:
        json.dump(player_data, f)
    return
