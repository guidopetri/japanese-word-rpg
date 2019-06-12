#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 3.6.4

import classes
from difflib import SequenceMatcher
import time
import random
import pygame
import sys


def battle(game_surface, player, all_words, game_time):
    from menus import message_box, wait_for_input, message_bg
    from menus import multiple_message_box
    from game_enums import colors, status_effect

    width = game_surface.get_width()
    height = game_surface.get_height()

    # make sure player can battle in the first place
    if not player.alive:
        message_text = "you're passed out! you can't battle!"
        message, message_rect = message_box(message_text,
                                            (width / 2, height / 4))

        game_surface.fill(colors.offblack.value)
        game_surface.blit(message, message_rect)

        pygame.display.flip()

        wait_for_input()
        return

    fast_mode = False
    poison_mode = False
    if player.status_duration > 0:
        if player.status == status_effect.stamina_up:
            game_time *= 1.5
        elif player.status == status_effect.hp_up:
            old_hp = player.health
            player.health += 0.5 * player.max_hp
            player.max_hp *= 1.5
        elif player.status == status_effect.dmg_up:
            player.dmg_multiplier *= 2
        elif player.status == status_effect.fast:
            fast_mode = True
        elif player.status == status_effect.give_poison:
            poison_mode = True
        player.status_duration -= 1
        if player.status_duration == 0:
            player.status = status_effect.normal
    if fast_mode:
        player.difficulty -= 0.13

    font = pygame.font.SysFont('Arial', 32)

    instructions_text = font.render("type it out!",
                                    True,
                                    colors.offblack.value)
    instructions_rect = instructions_text.get_rect()
    instructions_rect.midtop = (width / 2, height / 30)

    health_text = font.render("HP: %s" % player.health,
                              True,
                              colors.offblack.value)
    health_rect = health_text.get_rect()
    health_rect.midtop = (width / 4, height / 30)

    hit_text = font.render("HIT!!",
                           True,
                           colors.offblue.value)
    hit_rect = hit_text.get_rect()
    hit_rect.midtop = (width / 2, height / 2 + 45)

    ouch_text = font.render("OUCH!!",
                            True,
                            colors.offred.value)
    ouch_rect = ouch_text.get_rect()
    ouch_rect.midtop = (width / 2, height / 2 + 45)

    bg, bg_rect = message_bg((width * 3 / 4 + 10, height - 20),
                             (width / 2, 10))

    # 1176x888
    # each is 294x296
    img_coords = [(i, j) for i in range(0, 883, 294) for j in [0, 296, 592]]
    current_img = (0, 0, 0, 0)

    monster_images = pygame.image.load('media/monsters.png')
    monster_pixel_array = pygame.PixelArray(monster_images)
    monster_pixel_array.replace(colors.magenta.value,
                                pygame.Color(131, 232, 252), 0.4)  # wat
    del monster_pixel_array  # what the heck is this

    start_time = time.time()
    last_time = start_time
    time_left = game_time
    new_word = True
    typed_word = []
    gave_hit = False
    took_hit = False
    dead_enemy = False
    finished = False
    exit = False
    enemy = classes.enemy_word(random.randrange(1, 4))
    monster_choice = random.choice(img_coords)
    current_img = (monster_choice[0], monster_choice[1], 294, 296)
    monster_rect = pygame.Rect(0, 0, 294, 296)
    monster_rect.midtop = (width / 2, height / 10 - 5)

    while not finished:
        game_surface.fill(colors.offblack.value)
        game_surface.blit(bg, bg_rect)
        game_surface.blit(instructions_text, instructions_rect)
        if not enemy.alive:
            player.gain_exp(enemy.exp_yield)
            player.gain_gold(enemy.gold_yield)

            dead_text = font.render("ENEMY LEVEL %s KILLED!!"
                                    " 3 EXTRA SECONDS!!" % enemy.level,
                                    True,
                                    colors.offblack.value)
            dead_rect = dead_text.get_rect()
            dead_rect.midtop = (width / 2, 11 * height / 12)

            enemy = classes.enemy_word(random.randrange(1, 4))
            monster_choice = random.choice(img_coords)
            current_img = (monster_choice[0],
                           monster_choice[1],
                           294,
                           296)
            time_left += 3
            player.kills += 1
            dead_enemy = True
        if new_word:
            enemy.pick_word(all_words)
            word_text = font.render("%s" % enemy.word,
                                    True,
                                    colors.offblack.value)
            word_rect = word_text.get_rect()
            word_rect.midtop = (width / 2, height / 2 + 90)
            new_word = False
            typed_word = []
        time_left_text = font.render("%ss left" % time_left,
                                     True,
                                     colors.offblack.value)
        time_left_rect = time_left_text.get_rect()
        time_left_rect.midtop = (3 * width / 4, height / 30)

        game_surface.blit(time_left_text, time_left_rect)
        game_surface.blit(health_text, health_rect)

        game_surface.blit(monster_images,
                          monster_rect,
                          current_img)

        typed_text = font.render("".join(typed_word),
                                 True,
                                 colors.offblack.value)
        typed_rect = typed_text.get_rect()
        typed_rect.midtop = (width / 2, height / 2 + 135)

        game_surface.blit(word_text, word_rect)
        game_surface.blit(typed_text, typed_rect)

        if gave_hit:
            game_surface.blit(hit_text, hit_rect)

        if took_hit:
            game_surface.blit(ouch_text, ouch_rect)

        if dead_enemy:
            game_surface.blit(dead_text, dead_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    new_word = True
                    dead_enemy = False
                    if score_word(player.difficulty, enemy.word, "".join(typed_word)):  # noqa
                        gave_hit = True
                        took_hit = False
                        player.score_points(1)
                        enemy.take_damage(player.dmg_multiplier)
                        if poison_mode:
                            enemy.take_damage(1)
                    else:
                        took_hit = True
                        gave_hit = False
                        player.take_damage(1)
                        health_text = font.render("HP: %s" % player.health,  # noqa
                                                  True,
                                                  colors.offblack.value)  # noqa
                        health_rect = health_text.get_rect()
                        health_rect.midtop = (width / 4, height / 30)
                elif event.key == pygame.K_BACKSPACE:
                    typed_word = typed_word[:-1]
                elif event.key == pygame.K_1:
                    # for item usage during battle
                    pass
                elif event.key == pygame.K_2:
                    pass
                elif event.key == pygame.K_3:
                    pass
                elif event.key == pygame.K_4:
                    pass
                elif event.key == pygame.K_5:
                    pass
                elif event.key == pygame.K_6:
                    pass
                else:
                    typed_word.append(event.unicode)

        if time.time() - last_time > 1:
            last_time = time.time()
            time_left -= 1
        if time_left == 0:
            if time.time() - start_time >= game_time or not player.alive:
                finished = True
        pygame.display.flip()

    texts = ["your score was %s" % player.score,
             "and you killed %s monsters," % player.kills,
             "earning your level %s character" % player.level,
             "%s exp and %s gold." % (player.total_exp, player.total_gold)]

    end_text, end_rect = multiple_message_box(texts,
                                              (width / 2, height / 4))

    game_surface.fill(colors.offblack.value)
    game_surface.blit(end_text, end_rect)
    pygame.display.flip()

    time.sleep(3)

    for event in pygame.event.get():  # clear event queue
        pass

    wait_for_input()

    if 'old_hp' in locals():
        player.health = player.max_hp * (2 / 3) - (player.max_hp - player.health)  # noqa
        player.max_hp *= (2 / 3)
    if fast_mode:
        player.difficulty += 0.13
    return


def score_word(difficulty, word, user_input):
    return SequenceMatcher(None, word.lower(), user_input.lower()).ratio() >= difficulty  # noqa


def shop(game_surface, player):
    from game_enums import use_items, item_prices, colors
    from menus import choose_from_options, message_box, wait_for_input

    width = game_surface.get_width()
    height = game_surface.get_height()

    options = []
    for item in use_items:
        price = item_prices[item.name]
        item_str = item.name.replace('_', ' ') + ': $G' + str(price)
        options.append(item_str)

    gold_text = "Gold: $G{}".format(player.total_gold)
    gold, gold_rect = message_box(gold_text,
                                  (width * 5 / 6, height / 6))

    game_surface.fill(colors.offblack.value)
    game_surface.blit(gold, gold_rect)

    selected = choose_from_options(game_surface,
                                   "buy somethin', will ya?",
                                   options,
                                   (width / 2, height / 6))

    if selected == -1:
        return

    selected_name = use_items(selected).name
    selected_price = item_prices[selected_name]
    if player.total_gold >= item_prices[use_items(selected).name]:
        player.total_gold -= selected_price
        player.inventory[selected_name] += 1
        return

    # implicit else
    message_text = "you don't have enough money for that! now scram!"
    message, message_rect = message_box(message_text,
                                        (width / 2, height / 4))

    game_surface.fill(colors.offblack.value)
    game_surface.blit(message, message_rect)

    pygame.display.flip()

    wait_for_input()

    game_surface.fill(colors.offblack.value)

    return


def inventory(game_surface, player):
    from game_enums import use_items, colors
    from menus import choose_from_options, message_box, wait_for_input

    width = game_surface.get_width()
    height = game_surface.get_height()

    if sum([item for item in player.inventory.values()]) == 0:
        message_text = "You don't have anything in your inventory!"

    else:
        items = []
        options = []
        for item in use_items:
            amount = player.inventory[item.name]
            if amount <= 0:
                continue
            item_str = '{}x '.format(amount) + item.name.replace('_', ' ')
            items.append(item)
            options.append(item_str)

        gold_text = "Gold: $G{}".format(player.total_gold)
        gold, gold_rect = message_box(gold_text,
                                      (width * 5 / 6, height / 6))

        game_surface.fill(colors.offblack.value)
        game_surface.blit(gold, gold_rect)

        selected = choose_from_options(game_surface,
                                       "{}'s inventory".format(player.name),
                                       options,
                                       (width / 2, height / 6))

        if selected == -1:
            return

        selected_name = items[selected].name
        player.inventory[selected_name] -= 1
        get_effect(player, selected_name)

        message_text = "you used {}!".format(selected_name.replace('_', ' '))

    message, message_rect = message_box(message_text,
                                        (width / 2, height / 4))

    game_surface.fill(colors.offblack.value)
    game_surface.blit(message, message_rect)

    pygame.display.flip()

    wait_for_input()

    game_surface.fill(colors.offblack.value)

    return


def get_effect(player, choice):
    from game_enums import status_effect

    if choice == 'potion':
        player.health += 10
        if player.health > player.max_hp:
            player.health = player.max_hp
    elif choice == 'coffee':
        player.status = status_effect.fast
        player.status_duration = 5
    elif choice == 'poison_flask':
        player.status = status_effect.give_poison
        player.status_duration = 10
    elif choice == 'protein_shake':
        player.status = status_effect.hp_up
        player.status_duration = 2
    elif choice == 'sharpening_oil':
        player.status = status_effect.dmg_up
        player.status_duration = 2
    elif choice == 'energy_bar':
        player.status = status_effect.stamina_up
        player.status_duration = 2
    return


def church(game_surface, player):
    from menus import yn_question, message_box, wait_for_input
    from game_enums import colors

    width = game_surface.get_width()
    height = game_surface.get_height()

    # default message
    message_text = 'bless tha LAWD'

    if not player.alive:
        price = player.max_hp * 1.5
        question = 'would you like to revive for %i gold?' % price
        revive = yn_question(game_surface, question, (width / 2, height / 4))

        if revive and player.total_gold >= price:
            player.alive = True
            player.health = player.max_hp
            player.total_gold -= price
            message_text = "bless tha LAWD, you've been revived!"
        elif revive:
            message_text = "you don't have enough money!"

    message, message_rect = message_box(message_text,
                                        (width / 2, height / 4))

    game_surface.fill(colors.offblack.value)
    game_surface.blit(message, message_rect)

    pygame.display.flip()

    wait_for_input()

    return


def castle(game_surface, player):
    from story import chapters
    from menus import message_box, wait_for_input
    from game_enums import colors

    story = chapters[player.story_chapter]

    width = game_surface.get_width()
    height = game_surface.get_height()

    for msg in story:
        message_text = msg
        message, message_rect = message_box(message_text,
                                            (width / 2, height / 4))
        game_surface.fill(colors.offblack.value)
        game_surface.blit(message, message_rect)

        pygame.display.flip()

        wait_for_input()

    return
