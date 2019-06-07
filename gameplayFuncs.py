#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 3.6.4


import classes
from difflib import SequenceMatcher
import time
import random
from gameEnums import colors, status_effect, use_items
import pygame
import sys


def battle(game_surface, font, player, all_words, game_time):
    width = game_surface.get_width()
    height = game_surface.get_height()
    fast_mode = False
    poisonMode = False
    if player.status_duration > 0:
        if player.status == status_effect.stamina_up:
            game_time *= 1.5
        elif player.status == status_effect.hp_up:
            oldHP = player.health
            player.health += 0.5 * player.max_hp
            player.max_hp *= 1.5
        elif player.status == status_effect.dmg_up:
            player.dmgMultiplier *= 2
        elif player.status == status_effect.fast:
            fast_mode = True
        elif player.status == status_effect.give_poison:
            poisonMode = True
        player.status_duration -= 1
        if player.status_duration == 0:
            player.status = status_effect.normal
    if fast_mode:
        player.difficulty -= 0.13

    pass_out_text = font.render("you're passed out! you can't battle!",
                                True,
                                colors.offblack.value)
    pass_out_rect = pass_out_text.get_rect()
    pass_out_rect.midtop = (width / 2, height / 30)

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

    background_surface = pygame.Surface((width * 3 / 4 + 10, height - 20))
    background_surface.fill(colors.bgblue.value)
    background_rect = background_surface.get_rect()
    background_rect.midtop = (width / 2, 10)

    background = pygame.Surface((width * 3 / 4, height - 30))
    background.fill(colors.bgyellow.value)
    background_rect2 = background.get_rect()
    background_rect2.midtop = (background_rect.width / 2, 5)

    background_surface.blit(background, background_rect2)

    # 1176x888
    # each is 294x296
    monster_images_locations = [(i, j) for i in [0, 294, 588, 882] for j in [0, 296, 592]]  # noqa
    current_monster_image = (0, 0, 0, 0)

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
    monster_choice = random.choice(monster_images_locations)
    current_monster_image = (monster_choice[0], monster_choice[1], 294, 296)
    monster_rect = pygame._rect(0, 0, 294, 296)
    monster_rect.midtop = (width / 2, height / 10 - 5)

    while True:
        game_surface.fill(colors.offblack.value)
        game_surface.blit(background_surface, background_rect)
        if not player.alive:
            game_surface.blit(pass_out_text, pass_out_rect)
            time.sleep(3)
            break
        elif player.alive:
            if not finished:
                game_surface.blit(instructions_text, instructions_rect)
                if not enemy.alive:
                    player.gain_exp(enemy.exp_yield)
                    player.gain_gold(enemy.gold_yield)

                    dead_text = font.render("ENEMY LEVEL %s KILLED!! 3 EXTRA SECONDS!!" % enemy.level,  # noqa
                                            True,
                                            colors.offblack.value)
                    dead_rect = dead_text.get_rect()
                    dead_rect.midtop = (width / 2, 11 * height / 12)

                    enemy = classes.enemy_word(random.randrange(1, 4))
                    monster_choice = random.choice(monster_images_locations)
                    current_monster_image = (monster_choice[0],
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
                                  current_monster_image)

                typed_text = font.render("".join(typed_word),
                                         True,
                                         colors.offblack.value)
                typed_rect = typed_text.get_rect()
                typed_rect.midtop = (width / 2, height / 2 + 135)

                game_surface.blit(word_text, word_rect)
                game_surface.blit(typed_text, typed_rect)

                if gave_hit and not took_hit:
                    game_surface.blit(hit_text, hit_rect)

                if took_hit and not gave_hit:
                    game_surface.blit(ouch_text, ouch_rect)

                if dead_enemy:
                    game_surface.blit(dead_text, dead_rect)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.unicode not in ['1', '2', '3', '4', '5', '6'] and event.key != pygame.K_RETURN and event.key != pygame.K_BACKSPACE:  # noqa
                            typed_word.append(event.unicode)
                        elif event.key == pygame.K_RETURN:
                            new_word = True
                            dead_enemy = False
                            if score_word(player.difficulty, enemy.word, "".join(typed_word)):  # noqa
                                gave_hit = True
                                took_hit = False
                                player.score_points(1)
                                enemy.take_damage(player.dmgMultiplier)
                                if poisonMode:
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
                            try:
                                del typed_word[len(typed_word) - 1]
                            except IndexError:
                                pass
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

                if time.time() - last_time > 1:
                    last_time = time.time()
                    time_left -= 1
                if time_left == 0:
                    if time.time() - start_time >= game_time or not player.alive:  # noqa
                        finished = True
            elif finished:
                end_text = font.render("your score was %s and you killed %s monsters," % (player.score, player.kills),  # noqa
                                       True,
                                       colors.offblack.value)  # noqa
                end_rect = end_text.get_rect()
                end_rect.midtop = (width / 2, height / 2)

                end_text2 = font.render("earning your level %s character" % player.level,  # noqa
                                        True,
                                        colors.offblack.value)
                end_rect2 = end_text2.get_rect()
                end_rect2.midtop = (width / 2, height / 2 + 45)

                end_text3 = font.render("%s exp and %s gold" % (player.total_exp, player.total_gold),  # noqa
                                        True,
                                        colors.offblack.value)
                end_rect3 = end_text3.get_rect()
                end_rect3.midtop = (width / 2, height / 2 + 90)

                game_surface.blit(end_text, end_rect)
                game_surface.blit(end_text2, end_rect2)
                game_surface.blit(end_text3, end_rect3)
                pygame.display.flip()
                time.sleep(3)
                for event in pygame.event.get():  # clear event queue
                    pass
                while not exit:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            exit = True
                break
        pygame.display.flip()
    if 'oldHP' in locals():
        player.health = player.max_hp * (2 / 3) - (player.max_hp - player.health)  # noqa
        player.max_hp *= (2 / 3)
    if fast_mode:
        player.difficulty += 0.13
    return


def score_word(difficulty, word, user_input):
    return SequenceMatcher(None, word.lower(), user_input.lower()).ratio() >= difficulty  # noqa


def shop(game_surface, font, player):
    print("buy somethin', will ya?\n")
    print("Gold: %s\n" % player.total_gold)
    for item in use_items:
        print(item.value[0], " ", item.name.replace("_", " "), ": $G", item.value[1])  # noqa
    item_to_buy = input()
    item_chosen = list(item for item in use_items if item.value[0] == item_to_buy)[0].name  # noqa
    item_price = int(list(item for item in use_items if item.name == item_chosen)[0].value[1])  # noqa
    item_count = int(input("how many of %s?\n" % item_chosen))
    if player.total_gold >= item_price * item_count:
        player.inventory[item_chosen] += item_count
        player.total_gold -= item_price * item_count
    else:
        print("you don't have enough money for that! now scram!\n")
    return


def inventory(game_surface, font, player):
    print("\n%s's inventory\n" % player.name)
    if sum([item for item in player.inventory.values()]) == 0:
        print("you don't have anything in your inventory!\n")
        return
    for item in player.inventory.keys():
        if player.inventory[item] > 0:
            print(item + ": " + str(player.inventory[item]))
    choice = input("what would you like to use?\n")
    try:
        player.inventory[choice] -= 1
        get_effect(player, choice)
    except KeyError:
        print("item not recognized!\n")
    return


def get_effect(player, choice):
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


def church(game_surface, font, player):
    width = game_surface.get_width()
    height = game_surface.get_height()
    price = player.max_hp * 1.5
    revive_text = font.render("would you like to revive for %s gold? y/n" % price,  # noqa
                              True,
                              colors.offblack.value)
    revive_rect = revive_text.get_rect()
    revive_rect.midtop = (width / 2, height / 4)

    alive_text = font.render("bless tha LAWD",
                             True,
                             colors.offblack.value)
    alive_rect = alive_text.get_rect()
    alive_rect.midtop = (width / 2, height / 4)

    no_money_text = font.render("you don't have enough money!",
                                True,
                                colors.offblack.value)
    no_money_rect = no_money_text.get_rect()
    no_money_rect.midtop = (width / 2, height / 4 + 45)

    background_surface = pygame.Surface((width * 3 / 4, height / 4 - 10))
    background_surface.fill(colors.bgblue.value)
    background_rect = background_surface.get_rect()
    background_rect.midtop = (width / 2, height / 4 - 25)

    background = pygame.Surface((width * 3 / 4 - 10, height / 4 - 20))
    background.fill(colors.bgyellow.value)
    background_rect2 = background.get_rect()
    background_rect2.midtop = (background_rect.width / 2, 5)

    background_surface.blit(background, background_rect2)

    no_money = False

    while True:
        game_surface.fill(colors.offblack.value)
        game_surface.blit(background_surface, background_rect)
        if not player.alive:
            game_surface.blit(revive_text, revive_rect)
            if no_money:
                game_surface.blit(no_money_text, no_money_rect)
        elif player.alive:
            game_surface.blit(alive_text, alive_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y and not player.alive:
                    if player.total_gold >= price:
                        player.alive = True
                        player.health = player.max_hp
                        player.total_gold -= price
                    else:
                        no_money = True
                else:
                    return
        pygame.display.flip()
    return
