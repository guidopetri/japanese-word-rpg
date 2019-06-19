#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 3.6.4

import classes
from difflib import SequenceMatcher
import time
import random
import pygame
import sys
import config


def battle(game_surface, all_words):
    from menus import message_box, wait_for_input, message_bg
    from menus import multiple_message_box
    from game_enums import colors, status_effect

    player = config.player
    width = config.width
    height = config.height

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
        # not sure what to do for an effect yet
        raise NotImplementedError
    elif player.status == status_effect.hp_up:
        player.health += int(0.5 * player.max_hp)  # 8 / 10 -> 13 / 15
        player.max_hp = int(player.max_hp * 1.5)
    elif player.status == status_effect.dmg_up:
        player.dmg_multiplier *= 2
    elif player.status == status_effect.fast:
        player.difficulty -= 0.13
    elif player.status == status_effect.give_poison:
        poison_mode = True

    font = pygame.font.SysFont(config.fontname, config.fontsize)

    bg, bg_rect = message_bg((width * 3 / 4 + 10, height - 20),
                             (width / 2, 10))

    instructions_text = font.render("type it out!",
                                    True,
                                    colors.offblack.value)
    instructions_rect = instructions_text.get_rect(midtop=(bg_rect.width / 2,
                                                           10))
    bg.blit(instructions_text, instructions_rect)

    # 1176x888
    # each is 294x296
    img_coords = [(i, j) for i in range(0, 883, 294) for j in [0, 296, 592]]
    current_img = (0, 0, 0, 0)

    # images need to be cleaned up a little
    monster_images = pygame.image.load('media/monsters.png').convert()
    monster_images.set_colorkey(colors.magenta.value)

    bg_gradient = pygame.Surface((width / 2, font.get_linesize()),
                                 pygame.SRCALPHA)
    bg_gradient.fill(colors.bgyellow.value)
    make_bg_gradient(bg_gradient)

    game_surface.fill(colors.offblack.value)
    typed_words = []

    enemy = classes.enemy_word(random.randrange(1, 4))

    for i in range(enemy.max_hp):
        enemy.pick_word(all_words)

    monster_choice = random.choice(img_coords)
    current_img = (*monster_choice, 294, 296)
    monster_rect = pygame.Rect(0, 0, 294, 296)
    monster_rect.midtop = (bg_rect.width / 2, 45)

    bg.blit(monster_images,
            monster_rect,
            current_img)

    i = 0
    correct = 0
    last_atk = time.time()
    while enemy.alive:
        game_surface.blit(bg, bg_rect)

        hp_text = font.render("HP: %s" % player.health,
                              True,
                              colors.offblack.value)
        hp_rect = hp_text.get_rect(midtop=(width / 4, height / 30))

        word_text = font.render(''.join(enemy.words),
                                True,
                                colors.offblue.value)
        typed_text = font.render(''.join(typed_words),
                                 True,
                                 colors.offred.value,
                                 colors.bgyellow.value)

        dest = (width / 4, height / 2 + 90)
        template_dest = (width / 2, height / 2 + 90)

        move_by = sum([x[4] for x in font.metrics(''.join(enemy.words[:i]))])
        word_area = pygame.Rect(move_by,  # left
                                0,  # top
                                width / 4,  # width
                                font.get_linesize()  # height
                                )
        move_typed = sum([x[4] for x in font.metrics(''.join(typed_words))])
        type_area = pygame.Rect(- width / 4 + move_typed,  # left
                                0,  # top
                                width / 2,  # width
                                font.get_linesize()  # height
                                )

        if time.time() - last_atk >= enemy.atk_ivl:
            last_atk = time.time()
            player.take_damage(1)
        if not player.alive:
            break

        game_surface.blit(word_text, template_dest, word_area)
        game_surface.blit(typed_text, dest, type_area)
        game_surface.blit(bg_gradient, dest)

        game_surface.blit(hp_text, hp_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # start counting towards cpm timer on first keypress
                if i == 0:
                    start_time = time.time()
                if event.key == pygame.K_SPACE:
                    word, typed = get_words(enemy.words, typed_words)
                    if score_word(player.difficulty, word, typed):
                        correct += 1
                        enemy.take_damage(int(player.dmg_multiplier))
                        if poison_mode:
                            enemy.take_damage(1)
                    else:
                        enemy.pick_word(all_words)
                        player.take_damage(1)
                    try:
                        # move i to next space in enemy.words, if not on space
                        i += enemy.words[i:].index(' ')
                    except ValueError:
                        pass
                    typed_words.append(' ')
                elif event.key == pygame.K_BACKSPACE:
                    # stop backspacing past a space
                    if typed_words and typed_words[-1] != ' ':
                        typed_words = typed_words[:-1]
                        word, typed = get_words(enemy.words, typed_words)
                        if enemy.words[i] != ' ' or len(word) > len(typed):
                            i -= 1
                    continue
                elif event.key in (pygame.K_1,
                                   pygame.K_2,
                                   pygame.K_3,
                                   pygame.K_4,
                                   pygame.K_5,
                                   pygame.K_6):
                    # for item usage during battle
                    held_idx = int(event.unicode) - 1
                    use_item = player.held_items[held_idx]
                    if player.inventory[use_item] > 0:
                        get_effect(use_item)
                        player.inventory[use_item] -= 1
                    continue
                elif event.key == pygame.K_RETURN:
                    continue
                else:
                    typed_words.append(event.unicode)
                    # don't add to i if currently space on enemy.words
                    if len(enemy.words) <= i or enemy.words[i] == ' ':
                        continue
                i += 1
        pygame.display.flip()
    else:
        # if the enemy died, not the player
        end_time = time.time()
        score = round(100 * correct / enemy.word_count)
        cpm = round(60 * len(typed_words) / (end_time - start_time))
        wpm = cpm / 5
        gained_exp = int(enemy.exp_yield * score / 100)
        gained_gold = int(enemy.gold_yield * score / 100)

        player.gain_exp(gained_exp)
        player.gain_gold(gained_gold)

        player.kills += 1

        texts = ["ENEMY LEVEL %s KILLED!!" % enemy.level,
                 "your accuracy was %s%%" % score,
                 "with a speed of %s cpm (%s wpm)," % (cpm, wpm),
                 "earning your level %s character" % player.level,
                 "%i exp and %i gold." % (gained_exp, gained_gold)]

        message, message_rect = multiple_message_box(texts,
                                                     (width / 2, height / 4))

    game_surface.fill(colors.offblack.value)
    game_surface.blit(message, message_rect)
    pygame.display.flip()

    time.sleep(0.5)

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

    if player.level_pending:
        stats_delta = player.level_up()

        tups = [(name, stat - stats_delta[name], stat)
                for name, stat in player.stats
                if name in stats_delta]

        texts = ["LEVEL UP!!"]
        # unpack into formatting text
        texts.extend(["{}: {} -> {}".format(*tup)
                     for tup in tups])

        message, message_rect = multiple_message_box(texts,
                                                     (width / 2, height / 4))

        game_surface.fill(colors.offblack.value)
        game_surface.blit(message, message_rect)
        pygame.display.flip()
        wait_for_input()

    return


def get_words(enemy_words, typed_words):
    typed_wordlist = ''.join(typed_words).split(' ')
    idx = len(typed_wordlist) - 1
    last_enemy_word = ''.join(enemy_words).split(' ')[idx]
    last_typed_word = typed_wordlist[-1]
    return last_enemy_word, last_typed_word


def make_bg_gradient(surface):
    from pygame.surfarray import pixels_alpha
    from numpy import full, linspace, concatenate, flip

    # manipulate alpha values with numpy
    grad_width = surface.get_width() // 3
    grad_height = surface.get_height()
    alpha_array = pixels_alpha(surface)

    all_fill = full(grad_height,  # single dimension
                    255)
    all_empty = full(grad_height,
                     0)
    left_half = linspace(all_empty,
                         all_fill,
                         num=grad_width,
                         dtype='uint8')
    right_half = flip(left_half, axis=0)  # mirrored
    center = full((surface.get_width() - 2 * grad_width, grad_height),
                  255,  # fill value
                  dtype='uint8')

    # operates in place, since we used pixels_alpha and not array_alpha
    alpha_array -= concatenate([left_half, center, right_half],
                               axis=0)
    return


def score_word(difficulty, word, user_input):
    return SequenceMatcher(None, word, user_input).ratio() >= difficulty


def shop(game_surface):
    from game_enums import colors
    from menus import choose_from_options, message_box, wait_for_input
    from items import items

    player = config.player
    width = config.width
    height = config.height

    options = [(name, item.print_price())
               for name, item in items.items()
               if item.unlock_chapter <= config.player.story_chapter
               and not item.is_special]

    gold_text = "Gold: $G{}".format(player.total_gold)
    gold, gold_rect = message_box(gold_text,
                                  (width * 5 / 6, height / 6))

    game_surface.fill(colors.offblack.value)
    game_surface.blit(gold, gold_rect)

    selected = choose_from_options(game_surface,
                                   "buy somethin', will ya?",
                                   [opt[1] for opt in options],
                                   (width / 2, height / 6))

    if selected == -1:
        return

    name = options[selected][0]
    selected_item = items[name]
    price = selected_item.price
    if player.total_gold >= price:
        player.total_gold -= price
        player.inventory[name] += 1
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


def inventory(game_surface):
    from game_enums import colors
    from menus import choose_from_options, message_box, item_options
    from menus import multiple_message_box, wait_for_input, yn_question
    from items import items

    player = config.player
    width = config.width
    height = config.height

    if sum([item for item in player.inventory.values()]) == 0:
        message_text = "you don't have anything in your inventory!"

    else:
        options = []
        for name, item in items.items():
            amount = player.inventory[name]
            if amount <= 0:
                continue
            if isinstance(amount, bool):
                item_str = name
            else:
                item_str = '{}x {}'.format(amount, name)
            options.append((name, item_str))

        gold_text = "Gold: $G{}".format(player.total_gold)
        gold, gold_rect = message_box(gold_text,
                                      (width * 5 / 6, height / 6))

        current_equipment = ["{}: {}".format(slot, item or 'empty')
                             for slot, item in player.equipment.items()]

        equips, equips_rect = multiple_message_box(current_equipment,
                                                   (width * 5 / 6,
                                                    height * 2 / 6))

        current_held = ['{}: {}'.format(i + 1, x or 'empty')
                        for i, x in enumerate(player.held_items)]

        held, held_rect = multiple_message_box(current_held,
                                               (width / 6,
                                                height * 2 / 6))

        game_surface.fill(colors.offblack.value)
        game_surface.blit(gold, gold_rect)
        game_surface.blit(equips, equips_rect)
        game_surface.blit(held, held_rect)

        selected = choose_from_options(game_surface,
                                       "{}'s inventory".format(player.name),
                                       [opt[1] for opt in options],
                                       (width / 2, height / 6))

        if selected == -1:
            return

        name = options[selected][0]
        action = item_options(game_surface, name)
        if action == 'use':
            if items[name].is_use:
                player.inventory[name] -= 1
                get_effect(name)
                message_text = "you used {}!"
            else:
                message_text = "you can't use {}!"
        elif action == 'hold':
            if items[name].is_use:
                # choose slot
                selected = choose_from_options(game_surface,
                                               'which slot?',
                                               [str(x) for x in range(1, 7)],
                                               (width / 2, height / 3))
                if name in player.held_items:
                    idx = player.held_items.index(name)
                    player.held_items[idx] = None
                player.held_items[selected] = name
                message_text = "you held onto {}!"
            else:
                message_text = "you can't hold onto {}!"
        elif action == 'equip':
            if items[name].is_equip:
                player.equipment[items[name].equip_type] = name
                player.inventory[name] -= 1
                message_text = "you equipped {}!"
            else:
                message_text = "you can't equip {}!"
        elif action == 'discard':
            if not items[name].is_special:
                # are you sure?
                sure = yn_question(game_surface,
                                   'are you sure?',
                                   (width / 2, height / 2))
                if sure:
                    player.inventory[name] -= 1
                    message_text = "you threw away {}."
                else:
                    return
            else:
                message_text = "you can't throw {} away! it's too valuable!"

        message_text = message_text.format(name)

    message, message_rect = message_box(message_text,
                                        (width / 2, height / 4))

    game_surface.fill(colors.offblack.value)
    game_surface.blit(message, message_rect)

    pygame.display.flip()

    wait_for_input()

    game_surface.fill(colors.offblack.value)

    return


def get_effect(choice):
    from game_enums import status_effect

    player = config.player

    if choice == 'potion':
        player.health = min(player.health + 10, player.max_hp)
    elif choice == 'coffee':
        player.status = status_effect.fast
        player.status_duration = 5
    elif choice == 'poison flask':
        player.status = status_effect.give_poison
        player.status_duration = 10
    elif choice == 'protein shake':
        player.status = status_effect.hp_up
        player.status_duration = 2
    elif choice == 'sharpening oil':
        player.status = status_effect.dmg_up
        player.status_duration = 2
    elif choice == 'energy bar':
        player.status = status_effect.stamina_up
        player.status_duration = 2
    return


def church(game_surface):
    from menus import yn_question, conversation_box, wait_for_input
    from game_enums import colors

    player = config.player
    width = config.width
    height = config.height

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

    message, message_rect = conversation_box('priest',
                                             message_text)

    game_surface.fill(colors.offblack.value)
    game_surface.blit(message, message_rect)

    pygame.display.flip()

    wait_for_input()

    return


def castle(game_surface):
    from story import king_story, king_items_given
    from menus import conversation_box, message_box, wait_for_input
    from game_enums import colors
    from items import items

    player = config.player
    width = config.width
    height = config.height

    # this is all needed just for the king positioning...
    font = pygame.font.SysFont(config.fontname, config.fontsize)
    line_size = font.get_linesize()

    box_height = 2 * line_size + 10

    story = king_story[player.story_chapter]
    added_items = king_items_given[player.story_chapter]

    king_img = pygame.image.load('media/edo-king.png').convert()
    king_img.set_colorkey(colors.magenta.value)
    king_img = pygame.transform.scale(king_img,
                                      (height // 2,  # width
                                       height // 2)  # height
                                      )
    king_rect = king_img.get_rect(bottomright=(width,
                                               height - box_height))

    for i, msg in enumerate(story + added_items):
        if msg in story:
            message, message_rect = conversation_box('king', msg)
        if msg in items:
            if items[msg].is_special:
                player.inventory[msg] = True
            else:
                player.inventory[msg] += 1
            message, message_rect = message_box("you got {}".format(msg),
                                                (width / 2, height / 4))

        game_surface.fill(colors.offblack.value)
        game_surface.blit(message, message_rect)
        game_surface.blit(king_img, king_rect)

        pygame.display.flip()

        wait_for_input()

    return
