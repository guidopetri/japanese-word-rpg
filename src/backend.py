#!/usr/bin/env python3

import config


def load_words():

    import pickle

    with open('src/words.pckl', 'rb') as f:
        all_words = pickle.load(f)

    return all_words


def save_player():
    import pickle

    player = config.player
    savepath = config.savepath

    with open(savepath + 'players/{}.sav'.format(player.name), 'wb') as f:
        pickle.dump(player, f, protocol=-1)

    return


def save_map(game_map):
    import pickle

    player = config.player
    savepath = config.savepath

    with open(savepath + 'maps/{}_map.sav'.format(player.name), 'wb') as f:
        pickle.dump(game_map, f, protocol=-1)

    return


def load_map():
    import pickle

    player = config.player
    savepath = config.savepath

    with open(savepath + 'maps/{}_map.sav'.format(player.name), 'rb') as f:
        game_map = pickle.load(f)

    return game_map


def create_dirs():
    import os

    savepath = config.savepath

    game_paths = [savepath + 'players',
                  savepath + 'maps',
                  ]

    for path in game_paths:
        os.makedirs(path, exist_ok=True)
