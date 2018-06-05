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
	welcomeText = sysFont.render("welcome to Edo",True,gameEnums.gameColors.offblack.value)
	welcomeRect = welcomeText.get_rect()
	welcomeRect.midtop=(width/2,height/2-135)

	battleText = sysFont.render("1: battle",True,gameEnums.gameColors.offblack.value)
	battleRect = battleText.get_rect()
	battleRect.midtop=(width/2,height/2-90)

	shopText = sysFont.render("2: shop",True,gameEnums.gameColors.offblack.value)
	shopRect = shopText.get_rect()
	shopRect.midtop=(width/2,height/2-45)

	inventoryText = sysFont.render("3: inventory",True,gameEnums.gameColors.offblack.value)
	inventoryRect = inventoryText.get_rect()
	inventoryRect.midtop=(width/2,height/2)

	churchText = sysFont.render("4: church",True,gameEnums.gameColors.offblack.value)
	churchRect = churchText.get_rect()
	churchRect.midtop=(width/2,height/2+45)

	quitText = sysFont.render("0: quit",True,gameEnums.gameColors.offblack.value)
	quitRect = quitText.get_rect()
	quitRect.midtop=(width/2,height/2+90)

	backgroundSurface = pygame.Surface((welcomeRect.width+100,305))
	backgroundSurface.fill(gameEnums.gameColors.bgblue.value)
	backgroundRect = backgroundSurface.get_rect()
	backgroundRect.midtop = (width/2,height/2-157)

	background = pygame.Surface((welcomeRect.width+90,295))
	background.fill(gameEnums.gameColors.bgyellow.value)
	backgroundRect2 = background.get_rect()
	backgroundRect2.midtop = (backgroundRect.width/2,5)

	backgroundSurface.blit(background,backgroundRect2)
	
	while True:
		playSurface.fill(gameEnums.gameColors.offblack.value)
		playSurface.blit(backgroundSurface,backgroundRect)
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
					gameplayFuncs.battle(playSurface,sysFont,currentPlayer,allWords,20)
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