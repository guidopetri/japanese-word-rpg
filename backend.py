#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python 3.6.4

import json
import classes

def loadWords():
	with open('wordsLen.ini','r') as file:
		allWords = json.loads(file.read())
	return allWords

def loadPlayer():
	try:
		with open('player.ini','r') as file:
			playerData = json.loads(file.read())

		print([x for x in playerData.keys()],sep=' ',end='\n')
		playerName = input("who are you?\n")
		try:
			player = classes.PlayerCharacter(playerDict=playerData[playerName])
		except KeyError:
			print("player doesn't exist")
			playerName = input("what's your name?\n")
			playerClass = input("what's your class?\n")
			player = classes.PlayerCharacter(playerName=playerName,playerClass=playerClass)
	except FileNotFoundError:
		playerData = {}
		playerName = input("what's your name?\n")
		player = classes.PlayerCharacter(playerName=playerName)
	return playerData,player

def savePlayer(playerData,player):
	playerData[player.name] = player.toJSON()

	with open('player.ini','w') as file:
		json.dump(playerData,file)
	return