#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# python 3.6.4

import menus
import pygame
import config

# pygame.joystick.init() is breaking my execution for some reason.
pygame.display.init()
pygame.font.init()
# pygame.mixer.init()

play_surface = pygame.display.set_mode((config.width, config.height))
pygame.display.set_caption("Word RPG")

menus.intro_screen(play_surface)
menus.select_player(play_surface)
menus.main_menu(play_surface)
