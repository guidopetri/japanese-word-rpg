#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python 3.6.4

import gameplayFuncs
import backend

def mainMenu():
	allWords = backend.loadWords()
	(playerData,currentPlayer) = backend.loadPlayer()
	gameplayFuncs.battle(currentPlayer,allWords,60)
	backend.savePlayer(playerData,currentPlayer)
	return