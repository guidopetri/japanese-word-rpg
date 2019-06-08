#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 3.6.4

import gameplay_funcs
import backend
import pyglet
import pyglet.gl


def main_menu():
    all_words = backend.load_words()
    (player_data, current_player) = backend.load_player()

    width, height = 800, 600
    window = pyglet.window.Window(width=width,
                                  height=height,
                                  caption='Word RPG')
    # window.push_handlers(pyglet.window.event.WindowEventLogger())

    main_batch = pyglet.graphics.Batch()
    text_edo = pyglet.text.Label("welcome to Edo",  # noqa
                                 font_name='Arial',
                                 font_size=36,
                                 x=width / 2,
                                 y=height / 2 + 135,
                                 anchor_x='center',
                                 anchor_y='center',
                                 align='center',
                                 color=(0, 0, 0, 255),
                                 batch=main_batch)
    text_battle = pyglet.text.Label("1: battle",  # noqa
                                    font_name='Arial',
                                    font_size=36,
                                    x=width / 2,
                                    y=height / 2 + 90,
                                    anchor_x='center',
                                    anchor_y='center',
                                    align='center',
                                    color=(0, 0, 0, 255),
                                    batch=main_batch)
    text_shop = pyglet.text.Label("2: shop",  # noqa
                                  font_name='Arial',
                                  font_size=36,
                                  x=width / 2,
                                  y=height / 2 + 45,
                                  anchor_x='center',
                                  anchor_y='center',
                                  align='center',
                                  color=(0, 0, 0, 255),
                                  batch=main_batch)
    text_inventory = pyglet.text.Label("3: inventory",  # noqa
                                       font_name='Arial',
                                       font_size=36,
                                       x=width / 2,
                                       y=height / 2,
                                       anchor_x='center',
                                       anchor_y='center',
                                       align='center',
                                       color=(0, 0, 0, 255),
                                       batch=main_batch)
    text_church = pyglet.text.Label("4: church",  # noqa
                                    font_name='Arial',
                                    font_size=36,
                                    x=width / 2,
                                    y=height / 2 - 45,
                                    anchor_x='center',
                                    anchor_y='center',
                                    align='center',
                                    color=(0, 0, 0, 255),
                                    batch=main_batch)
    text_quit = pyglet.text.Label("0: quit",  # noqa
                                  font_name='Arial',
                                  font_size=36,
                                  x=width / 2,
                                  y=height / 2 - 90,
                                  anchor_x='center',
                                  anchor_y='center',
                                  align='center',
                                  color=(0, 0, 0, 255),
                                  batch=main_batch)

    print("in the main function")

    @window.event
    def on_draw():
        window.clear()
        pyglet.graphics.draw(4,
                             pyglet.gl.GL_QUADS,
                             ('v2f',
                              (width / 4 - 5,
                               height / 4 + 5,
                               width * 3 / 4 + 5,
                               height / 4 + 5,
                               width * 3 / 4 + 5,
                               height * 3 / 4 + 15,
                               width / 4 - 5,
                               height * 3 / 4 + 15
                               )
                              ),
                             ('c3B',
                              (131, 131, 252) * 4)
                             )
        pyglet.graphics.draw(4,
                             pyglet.gl.GL_QUADS,
                             ('v2f',
                              (width / 4,
                               height / 4 + 10,
                               width * 3 / 4,
                               height / 4 + 10,
                               width * 3 / 4,
                               height * 3 / 4 + 10,
                               width / 4,
                               height * 3 / 4 + 10
                               )
                              ),
                             ('c3B',
                              (252, 232, 131) * 4))
        main_batch.draw()

    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == pyglet.window.key._1:
            gameplay_funcs.battle(window, current_player, all_words, 60)
        elif symbol == pyglet.window.key._2:
            gameplay_funcs.shop(current_player)
        elif symbol == pyglet.window.key._3:
            gameplay_funcs.inventory(current_player)
        elif symbol == pyglet.window.key._4:
            gameplay_funcs.church(window, current_player)
        elif symbol == pyglet.window.key._0:
            backend.save_player(player_data, current_player)
            pyglet.app.exit()

    pyglet.app.run()
    return
