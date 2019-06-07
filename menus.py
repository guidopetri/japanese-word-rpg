#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 3.6.4


import gameplayFuncs
from gameEnums import colors
import backend
import pygame
import sys


def main_menu():
    all_words = backend.loadWords()
    (player_data, current_player) = backend.loadPlayer()

    init_status = pygame.init()
    print(init_status)
    if init_status[1] > 0:
        print("had {0} initializing errors, exiting".format(init_status[1]))
        sys.exit()
    print("pygame initialized successfully")

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
                    gameplayFuncs.battle(play_surface,
                                         sys_font,
                                         current_player,
                                         all_words,
                                         20)
                elif event.key == pygame.K_2:
                    gameplayFuncs.shop(play_surface,
                                       sys_font,
                                       current_player)
                elif event.key == pygame.K_3:
                    gameplayFuncs.inventory(play_surface,
                                            sys_font,
                                            current_player)
                elif event.key == pygame.K_4:
                    gameplayFuncs.church(play_surface,
                                         sys_font,
                                         current_player)
                elif event.key == pygame.K_0:
                    backend.savePlayer(player_data,
                                       current_player)
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
        pygame.display.flip()
    return
