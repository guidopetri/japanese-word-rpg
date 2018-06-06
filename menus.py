#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python 3.6.4

import gameplayFuncs
import gameEnums
import backend
import pygame
import sys

def mainMenu():
	allWords = backend.loadWords()
	(playerData,currentPlayer) = backend.loadPlayer()

	initStatus = pygame.init()
	print(initStatus)
	if initStatus[1] > 0:
		print("had {0} initializing errors, exiting".format(initStatus[1]))
		sys.exit()
	print("pygame initialized successfully")

	width,height = 800,600
	playSurface = pygame.display.set_mode((width,height))
	pygame.display.set_caption("Word RPG")
	sysFont = pygame.font.SysFont('Arial',32)
	welcomeText = sysFont.render("welcome to Edo",True,gameEnums.gameColors.offwhite.value)
	welcomeRect = welcomeText.get_rect()
	welcomeRect.midtop=(350,100)

	battleText = sysFont.render("1: battle",True,gameEnums.gameColors.offwhite.value)
	battleRect = battleText.get_rect()
	battleRect.midtop=(350,145)

	shopText = sysFont.render("2: shop",True,gameEnums.gameColors.offwhite.value)
	shopRect = shopText.get_rect()
	shopRect.midtop=(350,190)

	inventoryText = sysFont.render("3: inventory",True,gameEnums.gameColors.offwhite.value)
	inventoryRect = inventoryText.get_rect()
	inventoryRect.midtop=(350,235)

	churchText = sysFont.render("4: church",True,gameEnums.gameColors.offwhite.value)
	churchRect = churchText.get_rect()
	churchRect.midtop=(350,280)

	quitText = sysFont.render("0: quit",True,gameEnums.gameColors.offwhite.value)
	quitRect = quitText.get_rect()
	quitRect.midtop=(350,325)

	while True:
		playSurface.fill(gameEnums.gameColors.offblack.value)
		playSurface.blit(welcomeText,welcomeRect)
		playSurface.blit(battleText,battleRect)
		playSurface.blit(shopText,shopRect)
		playSurface.blit(inventoryText,inventoryRect)
		playSurface.blit(churchText,churchRect)
		playSurface.blit(quitText,quitRect)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					gameplayFuncs.battle(playSurface,sysFont,currentPlayer,allWords,60)
				elif event.key == pygame.K_2:
					gameplayFuncs.shop(playSurface,sysFont,currentPlayer)
				elif event.key == pygame.K_3:
					gameplayFuncs.inventory(playSurface,sysFont,currentPlayer)
				elif event.key == pygame.K_4:
					gameplayFuncs.church(playSurface,sysFont,currentPlayer)
				elif event.key == pygame.K_0:
					backend.savePlayer(playerData,currentPlayer)
					pygame.event.post(pygame.event.Event(pygame.QUIT))
		pygame.display.flip()
	return