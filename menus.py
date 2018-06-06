#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python 3.6.4

import gameplayFuncs
import backend
import pyglet

def mainMenu():
	allWords = backend.loadWords()
	(playerData,currentPlayer) = backend.loadPlayer()
	width,height=(800,600)
	window = pyglet.window.Window(width=width,height=height,caption='Word RPG')
	window.push_handlers(pyglet.window.event.WindowEventLogger())

	mainBatch = pyglet.graphics.Batch()
	textEdo = pyglet.text.Label("welcome to Edo",font_name='Arial',font_size=36,x=width/2,y=height/2+135,anchor_x='center',anchor_y='center',align='center',batch=mainBatch)
	textBattle = pyglet.text.Label("1: battle",font_name='Arial',font_size=36,x=width/2,y=height/2+90,anchor_x='center',anchor_y='center',align='center',batch=mainBatch)
	textShop = pyglet.text.Label("2: shop",font_name='Arial',font_size=36,x=width/2,y=height/2+45,anchor_x='center',anchor_y='center',align='center',batch=mainBatch)
	textInventory = pyglet.text.Label("3: inventory",font_name='Arial',font_size=36,x=width/2,y=height/2,anchor_x='center',anchor_y='center',align='center',batch=mainBatch)
	textChurch = pyglet.text.Label("4: church",font_name='Arial',font_size=36,x=width/2,y=height/2-45,anchor_x='center',anchor_y='center',align='center',batch=mainBatch)
	textQuit = pyglet.text.Label("0: quit",font_name='Arial',font_size=36,x=width/2,y=height/2-90,anchor_x='center',anchor_y='center',align='center',batch=mainBatch)

	@window.event
	def on_draw():
		window.clear()
		mainBatch.draw()

	@window.event
	def on_key_press(symbol,modifiers):
		if symbol == pyglet.window.key._1:
			gameplayFuncs.battle(currentPlayer,allWords,60)
		elif symbol == pyglet.window.key._2:
			gameplayFuncs.shop(currentPlayer)
		elif symbol == pyglet.window.key._3:
			gameplayFuncs.inventory(currentPlayer)
		elif symbol == pyglet.window.key._4:
			gameplayFuncs.church(currentPlayer)
		elif symbol == pyglet.window.key._0:
			backend.savePlayer(playerData,currentPlayer)
			pyglet.app.exit()

	pyglet.app.run()
	return