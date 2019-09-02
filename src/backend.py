#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 3.6.4

import classes
import os
import config


def load_words():

    import pickle

    with open('src/words.pckl', 'rb') as f:
        all_words = pickle.load(f)

    return all_words


def load_player():
    import pickle

    savepath = config.savepath

    # name = input('what's your name?\n')
    name = 'Sid'
    if os.path.exists(savepath + 'players/{}.sav'.format(name)):
        with open(savepath + 'players/{}.sav'.format(name), 'rb') as f:
            player = pickle.load(f)
    else:
        print("player doesn't exist")
        player_class = input("what's your class?\n")
        player = classes.PlayerCharacter(player_name=name,
                                         player_class=player_class)
    config.player = player
    return


def save_player():
    import pickle

    player = config.player
    savepath = config.savepath

    with open(savepath + 'players/{}.sav'.format(player.name), 'wb') as f:
        pickle.dump(player, f, protocol=-1)

    return


def create_dirs():
    import os

    savepath = config.savepath

    game_paths = [savepath,
                  savepath + 'players',
                  ]

    for path in game_paths:
        if not os.path.exists(path):
            os.mkdir(path)
