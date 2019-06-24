#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 3.6.4

import pygame
import sys
import config


def select_player(play_surface):
    import os
    import pickle
    from backend import save_player

    width = config.width
    height = config.height

    player_names = [file[:-4] for file in os.listdir('players/')]
    player_names.extend(['new player'])

    selected = -1

    while selected == -1:
        selected = choose_from_options(play_surface,
                                       'who are you?',
                                       player_names,
                                       (width / 2, height / 4))

    if player_names[selected] == 'new player':
        create_player(play_surface)
    else:
        with open('players/{}.sav'.format(player_names[selected]), 'rb') as f:
            player = pickle.load(f)
            config.player = player

    save_player()


def create_player(play_surface):
    from game_enums import player_classes, colors
    from classes import PlayerCharacter

    width = config.width
    height = config.height

    font = pygame.font.SysFont(config.fontname, config.fontsize)
    line_size = font.get_linesize()

    pc_classes = [x.value for x in player_classes]

    question = font.render("what's your name?",
                           True,
                           colors.offblack.value)
    question_rect = question.get_rect(midtop=(width / 2, height / 4))

    bg, bg_rect = message_bg((width / 2, line_size * 2 + 10),
                             (width / 2, height / 4 - 5))

    name_text = []
    stop = False

    while not stop:
        name = font.render(''.join(name_text),
                           True,
                           colors.offblack.value)
        name_rect = name.get_rect(midtop=(width / 2,
                                          height / 4 + line_size))

        play_surface.fill(colors.offblack.value)
        play_surface.blit(bg, bg_rect)
        play_surface.blit(question, question_rect)
        play_surface.blit(name, name_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name_text:
                    stop = True
                elif event.key == pygame.K_BACKSPACE and name_text:
                    name_text = name_text[:-1]
                elif event.unicode.isalnum():
                    name_text.append(event.unicode)
        pygame.display.flip()

    play_surface.fill(colors.offblack.value)
    selected = -1

    while selected == -1:
        selected = choose_from_options(play_surface,
                                       'what class is your character?',
                                       pc_classes,
                                       (width / 2, height / 4))

    player = PlayerCharacter(player_name=''.join(name_text),
                             player_class=pc_classes[selected])

    config.player = player


def intro_screen(play_surface):
    pass


def main_menu(play_surface):
    import gameplay_funcs
    from game_enums import colors
    import backend

    all_words = backend.load_words()
    backend.load_player()

    width, height = config.width, config.height
    selected = None

    play_options = ['battle',
                    'shop',
                    'inventory',
                    'castle',
                    'church',
                    'quit']

    while True:
        play_surface.fill(colors.offblack.value)
        selected = choose_from_options(play_surface,
                                       'welcome to Edo',
                                       play_options,
                                       (width / 2, height / 4),
                                       selected)

        if selected == -1:
            selected = None
        elif selected == play_options.index('battle'):
            gameplay_funcs.battle(play_surface,
                                  all_words)
        elif selected == play_options.index('shop'):
            gameplay_funcs.shop(play_surface)
        elif selected == play_options.index('inventory'):
            gameplay_funcs.inventory(play_surface)
        elif selected == play_options.index('church'):
            gameplay_funcs.church(play_surface)
        elif selected == play_options.index('castle'):
            gameplay_funcs.castle(play_surface)
        elif selected == play_options.index('quit'):
            backend.save_player()
            pygame.quit()
            sys.exit()
    return


def yn_question(surface, question, position):
    selected = choose_from_options(surface,
                                   question,
                                   ['yes',
                                    'no'],
                                   position)
    return not selected


def choose_from_options(surface, question, options, position, selected=None):
    from game_enums import colors

    font = pygame.font.SysFont(config.fontname, config.fontsize)

    x, y = position

    k = len(options)
    line_size = font.get_linesize()
    all_texts = options + [question]

    size = max_size_texts(all_texts)

    bg, bg_rect = message_bg(size, position)

    question = font.render(question,
                           True,
                           colors.offblack.value)
    question_rect = question.get_rect(midtop=(bg_rect.width / 2, 5))
    bg.blit(question, question_rect)

    # required for aligning the arrow to the options
    option_lefts = []

    n = 0
    for text in options:
        n += 1
        option_text = font.render(text,
                                  True,
                                  colors.offblack.value)
        option_rect = option_text.get_rect(midtop=(bg_rect.width / 2,
                                                   5 + n * line_size))
        option_lefts.append(option_rect.left)
        bg.blit(option_text, option_rect)

    arrow = font.render('>',
                        True,
                        colors.offblue.value)
    arrow_rect = arrow.get_rect()
    # some math to later put the arrow next to the option
    arrow_x = x - 10 - bg_rect.width / 2

    selected = selected or 0
    no_selection = True

    while no_selection:
        surface.blit(bg, bg_rect)

        arrow_rect.midtop = (arrow_x + option_lefts[selected],
                             y + 7 + line_size * (selected + 1))

        surface.blit(arrow, arrow_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1 + k) % k
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % k
                elif event.key == pygame.K_RETURN:
                    no_selection = False
                elif event.key == pygame.K_BACKSPACE:
                    return -1

        pygame.display.flip()

    return selected


def max_size_rects(rects):

    def find_length(rects, axis):
        minmax_coords = []
        for side in axis:
            coords = []
            for rect in rects:
                coords.append(getattr(rect, side))
            minmax_coords.append(coords)
        return max(minmax_coords[1]) - min(minmax_coords[0])

    max_height = find_length(rects, ['top', 'bottom'])
    max_width = find_length(rects, ['left', 'right'])

    return (max_width + 50, max_height + 10)


def message_box(text, position):
    from game_enums import colors

    font = pygame.font.SysFont(config.fontname, config.fontsize)

    msg = font.render(text,
                      True,
                      colors.offblack.value)
    msg_rect = msg.get_rect()

    bg, bg_rect = message_bg((msg_rect.width + 50, msg_rect.height + 10),
                             position)
    msg_rect.center = (bg_rect.width / 2, bg_rect.height / 2)

    bg.blit(msg, msg_rect)

    return bg, bg_rect


def max_size_texts(texts):
    font = pygame.font.SysFont(config.fontname, config.fontsize)

    longest_str = max([x for x in texts], key=len)
    width = font.size(longest_str)[0]  # get only the width
    width += 50  # some padding
    height = len(texts) * font.get_linesize() + 10

    return width, height


def multiple_message_box(texts, initial_position):
    from game_enums import colors

    font = pygame.font.SysFont(config.fontname, config.fontsize)
    line_size = font.get_linesize()

    size = max_size_texts(texts)

    bg, bg_rect = message_bg(size, initial_position)

    for i, text in enumerate(texts):
        msg = font.render(text,
                          True,
                          colors.offblack.value)
        msg_rect = msg.get_rect(midtop=(bg_rect.width / 2,
                                        5 + i * line_size))
        bg.blit(msg, msg_rect)

    return bg, bg_rect


def conversation_box(name_text, texts):
    from game_enums import colors
    from copy import copy

    width = config.width
    height = config.height

    font = pygame.font.SysFont(config.fontname, config.fontsize)
    line_size = font.get_linesize()

    box_height = 2 * line_size + 10

    size = (width, box_height)

    og_bg, og_bg_rect = message_bg(size, (width / 2, height - box_height))

    name = font.render(name_text,
                       True,
                       colors.offpurple.value)
    name_rect = name.get_rect(topleft=(10,
                                       5))

    for text in get_text_split(texts, config.width):
        msg = font.render(text,
                          True,
                          colors.offblack.value)
        msg_rect = msg.get_rect(topleft=(10,
                                         5 + line_size))

        bg, bg_rect = copy(og_bg), copy(og_bg_rect)

        bg.blit(name, name_rect)
        bg.blit(msg, msg_rect)

        yield bg, bg_rect


def message_bg(size, position):
    from game_enums import colors

    width, height = size
    x, y = position

    border = pygame.Surface((width, height))
    border.fill(colors.bgblue.value)
    border_rect = border.get_rect(midtop=(x, y))

    bg = pygame.Surface((width - 10, height - 10))
    bg.fill(colors.bgyellow.value)
    bg_rect = bg.get_rect(midtop=(width / 2, 5))

    border.blit(bg, bg_rect)

    return border, border_rect


def wait_for_input(key=None):
    no_break = True

    while no_break:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if key is None or event.key == key:
                    no_break = False

    return


def item_options(surface, item):
    from game_enums import colors

    width = config.width
    height = config.height

    font = pygame.font.SysFont(config.fontname, config.fontsize)
    line_size = font.get_linesize()

    title_text = 'what would you like to do with {}?'.format(item)
    options = ['use', 'equip', 'hold', 'discard']

    max_width = font.size(title_text)[0]

    size = (max_width + 10, line_size * (1 + (len(options) + 1) // 2))

    bg, bg_rect = message_bg(size,
                             (width / 2, height / 2))

    title = font.render(title_text,
                        True,
                        colors.offblack.value)
    title_rect = title.get_rect(midtop=(bg_rect.width / 2, 5))

    lefts = []

    for i, text in enumerate(options):
        msg = font.render(text,
                          True,
                          colors.offblack.value)
        # quick mafs
        msg_rect = msg.get_rect(midtop=(bg_rect.width * (i // 2 + 1) / 3,
                                        bg_rect.height * (i % 2 + 1) / 3))
        lefts.append(msg_rect.left)
        bg.blit(msg, msg_rect)

    bg.blit(title, title_rect)

    arrow = font.render('>',
                        True,
                        colors.offblue.value)
    arrow_rect = arrow.get_rect()
    arrow_x = bg_rect.left - 10

    selected = 0
    no_selection = True

    while no_selection:
        surface.blit(bg, bg_rect)

        # TODO: check this math
        arrow_rect.midtop = ((arrow_x + lefts[selected]),  # width
                             (bg_rect.height * (selected % 2 + 1) / 3)
                             + height / 2,  # height
                             )

        surface.blit(arrow, arrow_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    selected = (selected + 1) % 2 + (selected // 2) * 2
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    selected = (selected + 2) % 4
                elif event.key == pygame.K_RETURN:
                    no_selection = False
                elif event.key == pygame.K_BACKSPACE:
                    return -1

        pygame.display.flip()

    return options[selected]


def get_text_split(texts, max_width):
    font = pygame.font.SysFont(config.fontname, config.fontsize)

    result = []

    if isinstance(texts, str):
        texts = [texts]

    for text in texts:
        while font.size(text)[0] > max_width:
            dev = font.size(text)[0] / max_width
            lim = round(len(text) // dev)
            if ' ' not in text[:lim]:
                return []
            last_space = text[:lim].rindex(' ')
            new_text = text[:last_space]
            result.append(new_text)
            text = text[last_space + 1:]
        result.append(text)

    return result


def get_items(surface, added_items):
    from items import items
    from game_enums import colors
    from copy import copy

    player = config.player
    width = config.width
    height = config.height

    original_surface = copy(surface)

    for item in added_items:
        if items[item].is_special:
            player.inventory[item] = True
        else:
            player.inventory[item] += 1
        message, message_rect = message_box("you got {}".format(item),
                                            (width / 2, height / 4))
        surface.fill(colors.offblack.value)
        surface.blit(original_surface, (0, 0))
        surface.blit(message, message_rect)
        pygame.display.flip()
        wait_for_input()

    return
