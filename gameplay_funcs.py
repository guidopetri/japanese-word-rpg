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
    message_text = "you're passed out! you can't battle!"
    message, message_rect = message_box(message_text,
                                        (width / 2, height / 4))
    if not player.alive:
        game_surface.fill(colors.offblack.value)
        game_surface.blit(message, message_rect)

        pygame.display.flip()

        wait_for_input()
        return

    poison_mode = False

    if player.status == status_effect.stamina_up:
        game_time *= 1.5
    elif player.status == status_effect.hp_up:
        player.health += int(0.5 * player.max_hp)  # 8 / 10 -> 13 / 15
        player.max_hp = int(player.max_hp * 1.5)
    elif player.status == status_effect.dmg_up:
        player.dmg_multiplier *= 2
    elif player.status == status_effect.fast:
        player.difficulty -= 0.13
    elif player.status == status_effect.give_poison:
        poison_mode = True

    font = pygame.font.SysFont('Arial', 32)

    bg, bg_rect = message_bg((width * 3 / 4 + 10, height - 20),
                             (width / 2, 10))

    instructions_text = font.render("type it out!",
                                    True,
                                    colors.offblack.value)
    instructions_rect = instructions_text.get_rect()
    instructions_rect.midtop = (bg_rect.width / 2, 10)
    bg.blit(instructions_text, instructions_rect)

    health_text = font.render("HP: %s" % player.health,
                              True,
                              colors.offblack.value)
    health_rect = health_text.get_rect()
    health_rect.midtop = (width / 4, height / 30)

    # 1176x888
    # each is 294x296
    img_coords = [(i, j) for i in range(0, 883, 294) for j in [0, 296, 592]]
    current_img = (0, 0, 0, 0)

    monster_images = pygame.image.load('media/monsters.png')
    monster_pixel_array = pygame.PixelArray(monster_images)
    monster_pixel_array.replace(colors.magenta.value,
                                pygame.Color(131, 232, 252), 0.4)  # wat
    del monster_pixel_array  # what the heck is this

    game_surface.fill(colors.offblack.value)
    start_time = time.time()
    typed_words = [' ' for i in range(15)]

    enemy = classes.enemy_word(random.randrange(1, 4))

    for i in range(enemy.max_hp):
        enemy.pick_word(all_words)

    monster_choice = random.choice(img_coords)
    current_img = (*monster_choice, 294, 296)
    monster_rect = pygame.Rect(0, 0, 294, 296)
    monster_rect.midtop = (width / 2, height / 10 - 5)

    i = 15
    last_word_index = 15
    correct = 0
    while enemy.alive and player.alive:
        game_surface.blit(bg, bg_rect)

        # this still needs to align properly
        word_text = font.render(''.join(enemy.words[i - 15:i + 15]),
                                True,
                                colors.offblack.value)
        word_rect = word_text.get_rect()
        word_rect.midtop = (width / 2, height / 2 + 90)

        game_surface.blit(health_text, health_rect)

        game_surface.blit(monster_images,
                          monster_rect,
                          current_img)

        typed_text = font.render(''.join(typed_words[i - 15:]),
                                 True,
                                 colors.offblack.value)
        typed_rect = typed_text.get_rect()
        typed_rect.topright = (width / 2, height / 2 + 135)

        game_surface.blit(word_text, word_rect)
        game_surface.blit(typed_text, typed_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # i need a better way of comparing words...
                    last_word = ''.join(typed_words[last_word_index:])
                    enemy_word = ''.join(enemy.words[last_word_index:i])
                    last_word_index = i + 1
                    if score_word(player.difficulty, enemy_word, last_word):
                        correct += 1
                        enemy.take_damage(int(player.dmg_multiplier))
                        if poison_mode:
                            enemy.take_damage(1)
                    else:
                        enemy.pick_word(all_words)
                        player.take_damage(1)
                        health_text = font.render("HP: %s" % player.health,
                                                  True,
                                                  colors.offblack.value)
                        health_rect = health_text.get_rect()
                        health_rect.midtop = (width / 4, height / 30)
                    typed_words.append(' ')
                elif event.key == pygame.K_BACKSPACE:
                    # stop backspacing past a space
                    if typed_words[-1] != ' ':
                        typed_words = typed_words[:-1]
                        i -= 1
                    continue
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
                elif event.key == pygame.K_RETURN:
                    pass
                else:
                    typed_words.append(event.unicode)
                i += 1

        pygame.display.flip()

    if not enemy.alive:
        end_time = time.time()
        score = round(correct / enemy.word_count, 2)
        cpm = round(60 * (len(typed_words) - 15) / (end_time - start_time))
        wpm = cpm / 5

        player.gain_exp(int(enemy.exp_yield * score))
        player.gain_gold(int(enemy.gold_yield * score))

        player.kills += 1

        texts = ["ENEMY LEVEL %s KILLED!!" % enemy.level,
                 "your accuracy was %s" % score,
                 "with a speed of %s cpm (%s wpm)," % (cpm, wpm),
                 "earning your level %s character" % player.level,
                 "%s exp and %s gold." % (player.total_exp, player.total_gold)]

        message, message_rect = multiple_message_box(texts,
                                                     (width / 2, height / 4))

    game_surface.fill(colors.offblack.value)
    game_surface.blit(message, message_rect)
    pygame.display.flip()

    time.sleep(1)

    # clear event queue
    pygame.event.clear()

    wait_for_input()

    if player.status_duration > 0:
        if player.status == status_effect.fast:
            player.difficulty += 0.13
        elif player.status == status_effect.hp_up:
            player.health = int(player.max_hp * (2 / 3)  # 13 / 15 -> 8 / 10
                                - (player.max_hp - player.health))
            player.max_hp = int(player.max_hp * (2 / 3))
        elif player.status == status_effect.dmg_up:
            player.dmg_multiplier /= 2
        player.status_duration -= 1
        if player.status_duration == 0:
            player.status = status_effect.normal
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
        game_surface.fill(colors.offblack.value)
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
