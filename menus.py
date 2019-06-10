#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 3.6.4

import pygame
import sys


def main_menu():
    import gameplay_funcs
    import backend

    all_words = backend.load_words()
    (player_data, current_player) = backend.load_player()

    init_status = pygame.init()

    if init_status[1] > 0:
        print("had {0} initializing errors, exiting".format(init_status[1]))
        sys.exit()

    width, height = 800, 600
    play_surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Word RPG")
    sys_font = pygame.font.SysFont('Arial', 32)
    selected = None

    while True:
        selected = choose_from_options(play_surface,
                                       'welcome to Edo',
                                       ['battle',
                                        'shop',
                                        'inventory',
                                        'church',
                                        'quit'],
                                       (width / 2, height / 4),
                                       selected)

        if selected == 0:
            gameplay_funcs.battle(play_surface,
                                  sys_font,
                                  current_player,
                                  all_words,
                                  20)
        elif selected == 1:
            gameplay_funcs.shop(play_surface,
                                current_player)
        elif selected == 2:
            gameplay_funcs.inventory(play_surface,
                                     sys_font,
                                     current_player)
        elif selected == 3:
            gameplay_funcs.church(play_surface,
                                  current_player)
        elif selected == 4:
            backend.save_player(player_data,
                                current_player)
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

    font = pygame.font.SysFont('Arial', 32)

    x, y = position

    k = len(options)
    line_size = font.get_linesize()
    all_texts = options + [question]

    size_rects = []
    for i, text in enumerate(all_texts):
        size_rects.append(pygame.Rect(0,
                                      i * line_size,
                                      *font.size(text)))
    size = get_size(size_rects)

    bg, bg_rect = message_bg(size, position)

    question = font.render(question,
                           True,
                           colors.offblack.value)
    question_rect = question.get_rect()
    question_rect.midtop = (bg_rect.width / 2, 5)
    bg.blit(question, question_rect)

    # required for aligning the arrow to the options
    option_lefts = []

    n = 0
    for text in options:
        n += 1
        option_text = font.render(text,
                                  True,
                                  colors.offblack.value)
        option_rect = option_text.get_rect()
        option_rect.midtop = (bg_rect.width / 2, 5 + n * line_size)
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
        surface.fill(colors.offwhite.value)
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

        pygame.display.flip()

    return selected


def get_size(rects):

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

    font = pygame.font.SysFont('Arial', 32)

    msg = font.render(text,
                      True,
                      colors.offblack.value)
    msg_rect = msg.get_rect()

    bg, bg_rect = message_bg((msg_rect.width + 50, msg_rect.height + 10),
                             position)
    msg_rect.center = (bg_rect.width / 2, bg_rect.height / 2)

    bg.blit(msg, msg_rect)

    return bg, bg_rect


def message_bg(size, position):
    from game_enums import colors

    width, height = size
    x, y = position

    border = pygame.Surface((width, height))
    border.fill(colors.bgblue.value)
    border_rect = border.get_rect()
    border_rect.midtop = (x, y)

    bg = pygame.Surface((width - 10, height - 10))
    bg.fill(colors.bgyellow.value)
    bg_rect = bg.get_rect()
    bg_rect.midtop = (width / 2, 5)

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
