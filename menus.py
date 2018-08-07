#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python 3.6.4

import gameplayFuncs
import backend
import pyglet
import pyglet.gl

def mainMenu():
	allWords = backend.loadWords()
	(playerData,currentPlayer) = backend.loadPlayer()
	width,height=(800,600)
	window = pyglet.window.Window(width=width,height=height,caption='Word RPG')
	#window.push_handlers(pyglet.window.event.WindowEventLogger())

	mainBatch = pyglet.graphics.Batch()
	textEdo = pyglet.text.Label("welcome to Edo",font_name='Arial',font_size=36,x=width/2,y=height/2+135,anchor_x='center',anchor_y='center',align='center',color=(0,0,0,255),batch=mainBatch)
	textBattle = pyglet.text.Label("1: battle",font_name='Arial',font_size=36,x=width/2,y=height/2+90,anchor_x='center',anchor_y='center',align='center',color=(0,0,0,255),batch=mainBatch)
	textShop = pyglet.text.Label("2: shop",font_name='Arial',font_size=36,x=width/2,y=height/2+45,anchor_x='center',anchor_y='center',align='center',color=(0,0,0,255),batch=mainBatch)
	textInventory = pyglet.text.Label("3: inventory",font_name='Arial',font_size=36,x=width/2,y=height/2,anchor_x='center',anchor_y='center',align='center',color=(0,0,0,255),batch=mainBatch)
	textChurch = pyglet.text.Label("4: church",font_name='Arial',font_size=36,x=width/2,y=height/2-45,anchor_x='center',anchor_y='center',align='center',color=(0,0,0,255),batch=mainBatch)
	textQuit = pyglet.text.Label("0: quit",font_name='Arial',font_size=36,x=width/2,y=height/2-90,anchor_x='center',anchor_y='center',align='center',color=(0,0,0,255),batch=mainBatch)

	print("in the main function")

	@window.event
	def on_draw():
		window.clear()
		pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f',(width/4-5,height/4+5,width*3/4+5,height/4+5,width*3/4+5,height*3/4+15,width/4-5,height*3/4+15)),('c3B', (131,131,252)*4))
		pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f',(width/4,height/4+10,width*3/4,height/4+10,width*3/4,height*3/4+10,width/4,height*3/4+10)),('c3B', (252,232,131)*4))
		mainBatch.draw()
		

	@window.event
	def on_key_press(symbol,modifiers):
		if symbol == pyglet.window.key._1:
			gameplayFuncs.battle(window,currentPlayer,allWords,60)
		elif symbol == pyglet.window.key._2:
			gameplayFuncs.shop(currentPlayer)
		elif symbol == pyglet.window.key._3:
			gameplayFuncs.inventory(currentPlayer)
		elif symbol == pyglet.window.key._4:
			gameplayFuncs.church(window,currentPlayer)
		elif symbol == pyglet.window.key._0:
			backend.savePlayer(playerData,currentPlayer)
			pyglet.app.exit()

	pyglet.app.run()
	return