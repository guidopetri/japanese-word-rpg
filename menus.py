#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python 3.6.4

import gameplayFuncs
import backend

def mainMenu():
	allWords = backend.loadWords()
	(playerData,currentPlayer) = backend.loadPlayer()
	while True:
		print("    welcome to Edo")
		print("1: battle")
		print("2: shop")
		print("3: inventory")
		print("4: church")
		print("0: quit")
		choice = input("where would you like to go?\n")
		if choice == '1':
			gameplayFuncs.battle(currentPlayer,allWords,60)
		elif choice == '2':
			gameplayFuncs.shop(currentPlayer)
		elif choice == '3':
			gameplayFuncs.inventory(currentPlayer)
		elif choice == '3':
			gameplayFuncs.church(currentPlayer)
		elif choice == '0':
			backend.savePlayer(playerData,currentPlayer)
			break
	return