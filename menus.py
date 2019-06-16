#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 3.6.4

import pygame
import sys
import config


def main_menu():
    import gameplay_funcs
    from game_enums import colors
    import backend

    all_words = backend.load_words()
    backend.load_player()

    # pygame.joystick.init() is breaking my execution for some reason.
    pygame.display.init()
    pygame.font.init()
    # pygame.mixer.init()

    width, height = config.width, config.height
    play_surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Word RPG")
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


def wait_for_input():
    no_break = True

    while no_break:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                no_break = False

    return
