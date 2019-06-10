#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 3.6.4

import pygame
import sys


def main_menu():
    import gameplay_funcs
    from game_enums import colors
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

    welcome_text = sys_font.render("welcome to Edo",
                                   True,
                                   colors.offblack.value)
    welcome_rect = welcome_text.get_rect()
    welcome_rect.midtop = (width / 2, height / 2 - 135)

    battle_text = sys_font.render("1: battle",
                                  True,
                                  colors.offblack.value)
    battle_rect = battle_text.get_rect()
    battle_rect.midtop = (width / 2, height / 2 - 90)

    shop_text = sys_font.render("2: shop",
                                True,
                                colors.offblack.value)
    shop_rect = shop_text.get_rect()
    shop_rect.midtop = (width / 2, height / 2 - 45)

    inventory_text = sys_font.render("3: inventory",
                                     True,
                                     colors.offblack.value)
    inventory_rect = inventory_text.get_rect()
    inventory_rect.midtop = (width / 2, height / 2)

    church_text = sys_font.render("4: church",
                                  True,
                                  colors.offblack.value)
    church_rect = church_text.get_rect()
    church_rect.midtop = (width / 2, height / 2 + 45)

    quit_text = sys_font.render("0: quit",
                                True,
                                colors.offblack.value)
    quit_rect = quit_text.get_rect()
    quit_rect.midtop = (width / 2, height / 2 + 90)

    background_surface = pygame.Surface((welcome_rect.width + 100, 305))
    background_surface.fill(colors.bgblue.value)
    background_rect = background_surface.get_rect()
    background_rect.midtop = (width / 2, height / 2 - 157)

    background = pygame.Surface((welcome_rect.width + 90, 295))
    background.fill(colors.bgyellow.value)
    background_rect2 = background.get_rect()
    background_rect2.midtop = (background_rect.width / 2, 5)

    background_surface.blit(background, background_rect2)

    while True:
        play_surface.fill(colors.offblack.value)
        play_surface.blit(background_surface, background_rect)
        play_surface.blit(welcome_text, welcome_rect)
        play_surface.blit(battle_text, battle_rect)
        play_surface.blit(shop_text, shop_rect)
        play_surface.blit(inventory_text, inventory_rect)
        play_surface.blit(church_text, church_rect)
        play_surface.blit(quit_text, quit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    gameplay_funcs.battle(play_surface,
                                          sys_font,
                                          current_player,
                                          all_words,
                                          20)
                elif event.key == pygame.K_2:
                    gameplay_funcs.shop(play_surface,
                                        sys_font,
                                        current_player)
                elif event.key == pygame.K_3:
                    gameplay_funcs.inventory(play_surface,
                                             sys_font,
                                             current_player)
                elif event.key == pygame.K_4:
                    gameplay_funcs.church(play_surface,
                                          current_player)
                elif event.key == pygame.K_0:
                    backend.save_player(player_data,
                                        current_player)
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
        pygame.display.flip()
    return


def yn_question(surface, question, position):
    from game_enums import colors

    font = pygame.font.SysFont('Arial', 32)

    x, y = position

    question = font.render(question,
                           True,
                           colors.offblack.value)
    question_rect = question.get_rect()
    question_rect.midtop = (x, y + 5)

    yes = font.render('Yes',
                      True,
                      colors.offblack.value)
    yes_rect = yes.get_rect()
    yes_rect.midtop = (x, y + 5 + font.get_linesize())

    no = font.render('No',
                     True,
                     colors.offblack.value)
    no_rect = no.get_rect()
    no_rect.midtop = (x, y + 5 + (2 * font.get_linesize()))

    arrow = font.render('>',
                        True,
                        colors.offblack.value)
    arrow_rect = arrow.get_rect()

    size = get_size([question_rect,
                     yes_rect,
                     no_rect])

    bg, bg_rect = message_bg(size, position)

    selected = 0
    no_selection = True

    while no_selection:
        surface.fill(colors.offwhite.value)
        surface.blit(bg, bg_rect)

        arrow_rect.midtop = (x - yes_rect.width,
                             y + 5 + font.get_linesize() * (selected + 1))

        surface.blit(question, question_rect)
        surface.blit(yes, yes_rect)
        surface.blit(no, no_rect)
        surface.blit(arrow, arrow_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1 + 2) % 2
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % 2
                elif event.key == pygame.K_RETURN:
                    no_selection = False

        pygame.display.flip()

    return not selected


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

    return (max_width + 10, max_height + 10)


def message_box(text, position):
    from game_enums import colors

    font = pygame.font.SysFont('Arial', 32)

    msg = font.render(text,
                      True,
                      colors.offblack.value)
    msg_rect = msg.get_rect()

    bg, bg_rect = message_bg((msg_rect.width + 20, msg_rect.height + 10),
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
