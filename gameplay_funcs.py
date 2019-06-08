#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 3.6.4


import classes
from difflib import SequenceMatcher
import time
import random
from game_enums import status_effect  # , use_items
import pyglet.gl
import pyglet


def battle(window, player, all_words, game_time):
    if not player.alive:
        print("you're passed out! you can't battle!\n")
        return
    fast_mode = False
    poison_mode = False
    if player.status_duration > 0:
        if player.status == status_effect.stamina_up:
            game_time *= 1.5
        elif player.status == status_effect.hp_up:
            oldHP = player.health
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

    print("type it out! you have %s seconds!" % game_time)
    print(player.health)
    time_limit = game_time
    start_time = time.time()
    finished = False
    while not finished:
        enemy = classes.enemy_word(random.randrange(1, 4))
        while enemy.alive:
            enemy.pick_word(all_words)
            enemy.print_word()
            user_input = input()
            if score_word(player.difficulty, enemy.word, user_input):
                print(" HIT!! %s" % enemy.health)
                player.score_points(1)
                enemy.take_damage(player.dmg_multiplier)
                if poison_mode:
                    enemy.take_damage(1)
            else:
                print(" OUCH!!")
                player.take_damage(1)
            if (time.time() - start_time >= time_limit) or (not player.alive):
                finished = True
                break
        time_limit += 3
        player.gain_exp(enemy.exp_yield)
        player.gain_gold(enemy.gold_yield)
        if finished:
            break
        print(" ENEMY LEVEL %s KILLED!! 3 EXTRA SECONDS!! %s TIME LEFT!!"
              % (enemy.level, int(time_limit - time.time() + start_time)))
        player.kills += 1

    if 'oldHP' in locals():
        player.health = (player.max_hp
                         * (2 / 3)
                         - (player.max_hp - player.health)
                         )
        player.max_hp *= (2 / 3)
    if fast_mode:
        player.difficulty += 0.13
    print("your score was %s and you killed %s monsters,"
          " earning your level %s character %s exp and %s gold"
          % (player.score,
             player.kills,
             player.level,
             player.total_exp,
             player.total_gold))
    return


def score_word(difficulty, word, user_input):
    return SequenceMatcher(None, word.lower(), user_input.lower()).ratio() >= difficulty  # noqa


def shop(game_surface, font, player):
    raise NotImplementedError
    # width = game_surface.get_width()
    # height = game_surface.get_height()

    # background_surface = pygame.Surface((width * 3 / 4 + 10,
    #                                      height * 3 / 4 - 10))
    # background_surface.fill(colors.bgblue.value)
    # background_rect = background_surface.get_rect()
    # background_rect.midtop = (width / 2, height / 6 - 25)

    # background = pygame.Surface((width * 3 / 4, height * 3 / 4 - 20))
    # background.fill(colors.bgyellow.value)
    # background_rect2 = background.get_rect()
    # background_rect2.midtop = (background_rect.width / 2, 5)

    # background_surface.blit(background, background_rect2)

    # buy_text = font.render("buy somethin', will ya?",
    #                        True,
    #                        colors.offblack.value)
    # buy_rect = buy_text.get_rect()
    # buy_rect.midtop = (width / 2, height / 6)

    # gold_amount_text = font.render("Gold: {}".format(player.total_gold),
    #                                True,
    #                                colors.offblack.value)
    # gold_amount_rect = gold_amount_text.get_rect()
    # gold_amount_rect.midtop = (width / 2, height / 6 + 45)

    # no_money_text = font.render("You don't have enough money for that!"
    #                             " Now scram!",
    #                             True,
    #                             colors.offblack.value)
    # no_money_rect = no_money_text.get_rect()
    # no_money_rect.midtop = (width / 2, height / 6 + 90)

    # item_texts = {}

    # i = 90
    # for item in use_items:
    #     i += 45

    #     key = item.value[0]
    #     price = item.value[1]
    #     item_str = key + ': ' + item.name.replace('_', ' ') + ': $G' + price

    #     item_text = font.render(item_str,
    #                             True,
    #                             colors.offblack.value)
    #     item_rect = item_text.get_rect()
    #     item_rect.midtop = (width / 2, height / 6 + i)

    #     item_texts[item_text] = item_rect

    # no_money = False

    # while True:
    #     game_surface.fill(colors.offblack.value)
    #     game_surface.blit(background_surface, background_rect)
    #     game_surface.blit(buy_text, buy_rect)
    #     game_surface.blit(gold_amount_text, gold_amount_rect)
    #     for text, rect in item_texts.items():
    #         game_surface.blit(text, rect)
    #     if no_money:
    #         game_surface.blit(no_money_text, no_money_rect)

    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()
    #         elif event.type == pygame.KEYDOWN:
    #             if no_money:
    #                 return
    #             for item in use_items:
    #                 key = item.value[0]
    #                 price = int(item.value[1])
    #                 if event.unicode == key:
    #                     if player.total_gold >= price:
    #                         player.total_gold -= price
    #                         player.inventory[item.name] += 1
    #                         return
    #                     else:
    #                         no_money = True
    #     pygame.display.flip()
    # return


def inventory(game_surface, font, player):
    raise NotImplementedError
    # width = game_surface.get_width()
    # height = game_surface.get_height()

    # background_surface = pygame.Surface((width * 3 / 4 + 10,
    #                                      height * 3 / 4 - 10))
    # background_surface.fill(colors.bgblue.value)
    # background_rect = background_surface.get_rect()
    # background_rect.midtop = (width / 2, height / 6 - 25)

    # background = pygame.Surface((width * 3 / 4, height * 3 / 4 - 20))
    # background.fill(colors.bgyellow.value)
    # background_rect2 = background.get_rect()
    # background_rect2.midtop = (background_rect.width / 2, 5)

    # background_surface.blit(background, background_rect2)

    # player_name_text = font.render("{}'s inventory".format(player.name),
    #                                True,
    #                                colors.offblack.value)
    # player_name_rect = player_name_text.get_rect()
    # player_name_rect.midtop = (width / 2, height / 6)

    # gold_amount_text = font.render("Gold: {}".format(player.total_gold),
    #                                True,
    #                                colors.offblack.value)
    # gold_amount_rect = gold_amount_text.get_rect()
    # gold_amount_rect.midtop = (width / 2, height / 6 + 45)

    # item_texts = {}

    # i = 90
    # if sum([item for item in player.inventory.values()]) == 0:
    #     item_text = font.render("You don't have anything in your inventory!",
    #                             True,
    #                             colors.offblack.value)
    #     item_rect = item_text.get_rect()
    #     item_rect.midtop = (width / 2, height / 6 + i)
    #     item_texts[item_text] = item_rect
    # else:
    #     for item in use_items:
    #         if player.inventory[item.name] > 0:
    #             i += 45

    #             key = item.value[0]
    #             item_str = key + ': ' + item.name.replace('_', ' ')

    #             item_text = font.render(item_str,
    #                                     True,
    #                                     colors.offblack.value)
    #             item_rect = item_text.get_rect()
    #             item_rect.midtop = (width / 2, height / 6 + i)

    #             item_texts[item_text] = item_rect

    # while True:
    #     game_surface.fill(colors.offblack.value)
    #     game_surface.blit(background_surface, background_rect)
    #     game_surface.blit(player_name_text, player_name_rect)
    #     game_surface.blit(gold_amount_text, gold_amount_rect)
    #     for text, rect in item_texts.items():
    #         game_surface.blit(text, rect)

    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()
    #         elif event.type == pygame.KEYDOWN:
    #             for item in use_items:
    #                 key = item.value[0]
    #                 if event.unicode == key:
    #                     if player.inventory[item.name] >= 1:
    #                         player.inventory[item.name] -= 1
    #                         get_effect(player, item.name)
    #                         return
    #             return

    #     pygame.display.flip()
    # return


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


def church(window, player):
    width, height = window.get_size()

    price = player.max_hp * 1.5
    not_enough_money = False

    revive_q = pyglet.text.Label("would you like to revive for %s gold?"
                                 % price,
                                 font_name='Arial',
                                 font_size=32,
                                 x=width / 2,
                                 y=height / 2,
                                 anchor_x='center',
                                 anchor_y='center',
                                 align='center',
                                 color=(255, 0, 0, 255)
                                 )
    no_money = pyglet.text.Label("you don't have enough money!",
                                 font_name='Arial',
                                 font_size=32,
                                 x=width / 2,
                                 y=height / 2 - 45,
                                 anchor_x='center',
                                 anchor_y='center',
                                 align='center',
                                 color=(255, 0, 0, 255)
                                 )
    lawd_bless = pyglet.text.Label("bless tha LAWD",
                                   font_name='Arial',
                                   font_size=32,
                                   x=width / 2,
                                   y=height / 2,
                                   anchor_x='center',
                                   anchor_y='center',
                                   align='center',
                                   color=(255, 0, 0, 255)
                                   )

    print("in the church function")

    @window.event
    def on_draw():
        window.clear()

        if not player.alive:
            revive_q.draw()
            if not_enough_money:
                no_money.draw()
        else:
            lawd_bless.draw()

    @window.event
    def on_key_press(symbol, modifiers):
        not_enough_money = False
        if symbol == pyglet.window.key.Y and not not_enough_money:
            if player.total_gold >= price:
                player.alive = True
                player.health = player.max_hp
                player.total_gold -= price
                return
            else:
                not_enough_money = True
        else:
            return
    return
