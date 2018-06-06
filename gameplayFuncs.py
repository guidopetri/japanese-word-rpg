#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python 3.6.4

import classes
import difflib
import time
import random
import gameEnums
import pygame
import sys

def battle(gameSurface,font,player,allWords,gameTime):
	fastMode = False
	poisonMode = False
	if player.statusDuration > 0:
		if player.status == gameEnums.StatusEffect.staminaUp:
			gameTime *= 1.5
		elif player.status == gameEnums.StatusEffect.hpUp:
			oldHP = player.health
			player.health += 0.5*player.maxHP
			player.maxHP *= 1.5
		elif player.status == gameEnums.StatusEffect.dmgUp:
			player.dmgMultiplier *= 2
		elif player.status == gameEnums.StatusEffect.fast:
			fastMode = True
		elif player.status == gameEnums.StatusEffect.givePoison:
			poisonMode = True
		player.statusDuration -=1
		if player.statusDuration == 0:
			player.status = gameEnums.StatusEffect.normal
	if fastMode:
		player.difficulty -=0.13

	passOutText = font.render("you're passed out! you can't battle!",True,gameEnums.gameColors.offwhite.value)
	passOutRect = passOutText.get_rect()
	passOutRect.midtop = (350,145)

	instructionsText = font.render("type it out!",True,gameEnums.gameColors.offwhite.value)
	instructionsRect = instructionsText.get_rect()
	instructionsRect.midtop = (350,145)

	healthText = font.render("%s"%player.health,True,gameEnums.gameColors.offwhite.value)
	healthRect = healthText.get_rect()
	healthRect.midtop = (150,145)

	hitText = font.render("HIT!!",True,gameEnums.gameColors.offwhite.value)
	hitRect = hitText.get_rect()
	hitRect.midtop = (50,400)

	ouchText = font.render("OUCH!!",True,gameEnums.gameColors.offwhite.value)
	ouchRect = ouchText.get_rect()
	ouchRect.midtop = (750,400)

	startTime = time.time()
	lastTime = startTime
	timeLeft = gameTime
	newWord = True
	typedWord = []
	gaveHit = False
	tookHit = False
	deadEnemy = False
	finished = False
	enemy = classes.enemyWord(random.randrange(1,4))

	while True:
		gameSurface.fill(gameEnums.gameColors.offblack.value)
		if not player.alive:
			gameSurface.blit(passOutText,passOutRect)
			time.sleep(3)
			break
		elif player.alive:
			gameSurface.blit(instructionsText,instructionsRect)
			if not finished:
				if not enemy.alive:
					player.gainEXP(enemy.expYield)
					player.gainGold(enemy.goldYield)

					deadText = font.render("ENEMY LEVEL %s KILLED!! 3 EXTRA SECONDS!!"%enemy.level,True,gameEnums.gameColors.offwhite.value)
					deadRect = deadText.get_rect()
					deadRect = (600,450)
					
					enemy = classes.enemyWord(random.randrange(1,4))
					timeLeft += 3
					player.kills +=1
					deadEnemy = True
				if newWord:
					enemy.pickWord(allWords)
					wordText = font.render("%s"%enemy.word,True,gameEnums.gameColors.offwhite.value)
					wordRect = wordText.get_rect()
					wordRect.midtop = (450,250)
					newWord = False
					typedWord = []
				timeLeftText = font.render("%s"%timeLeft,True,gameEnums.gameColors.offwhite.value)
				timeLeftRect = timeLeftText.get_rect()
				timeLeftRect.midtop = (450,145)

				gameSurface.blit(timeLeftText,timeLeftRect)
				gameSurface.blit(healthText,healthRect)

				typedText = font.render("".join(typedWord),True,gameEnums.gameColors.offwhite.value)
				typedRect = typedText.get_rect()
				typedRect.midtop = (450,285)

				gameSurface.blit(wordText,wordRect)
				gameSurface.blit(typedText,typedRect)

				if gaveHit and not tookHit:
					gameSurface.blit(hitText,hitRect)

				if tookHit and not gaveHit:
					gameSurface.blit(ouchText,ouchRect)

				if deadEnemy:
					gameSurface.blit(deadText,deadRect)

				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					elif event.type == pygame.KEYDOWN:
						if event.unicode not in ['1','2','3','4','5','6'] and event.key != pygame.K_RETURN:
							typedWord.append(event.unicode)
						elif event.key == pygame.K_RETURN:
							newWord = True
							deadEnemy = False
							if scoreWord(player.difficulty,enemy.word,"".join(typedWord)):
								gaveHit = True
								tookHit = False
								player.scorePoints(1)
								enemy.takeDamage(player.dmgMultiplier)
								if poisonMode:
									enemy.takeDamage(1)
							else:
								tookHit = True
								gaveHit = False
								player.takeDamage(1)
								healthText = font.render("%s"%player.health,True,gameEnums.gameColors.offwhite.value)
								healthRect = healthText.get_rect()
								healthRect.midtop = (150,145)
						elif event.key == pygame.K_1: #for item usage during battle
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

				if time.time()-lastTime > 1:
					lastTime = time.time()
					timeLeft -=1
				if timeLeft == 0:
					if time.time()-startTime >= gameTime or not player.alive:
						finished = True
			elif finished:
				endText = font.render("your score was %s and you killed %s monsters, earning your level %s character %s exp and %s gold"%(player.score,player.kills,player.level,player.totalEXP,player.totalGold),True,gameEnums.gameColors.offwhite.value)
				endRect = endText.get_rect()
				endRect.midtop = (50,300)

				gameSurface.blit(endText,endRect)
				pygame.display.flip()
				time.sleep(3)
				break
		pygame.display.flip()
	if 'oldHP' in locals():
		player.health = player.maxHP*(2/3)-(player.maxHP-player.health)
		player.maxHP *= (2/3)
	if fastMode:
		player.difficulty +=0.13
	return

def scoreWord(difficulty,word,userInput):
	return difflib.SequenceMatcher(None,word.lower(),userInput.lower()).ratio() >= difficulty

def shop(gameSurface,font,player):
	print("buy somethin', will ya?\n")
	print("Gold: %s\n"%player.totalGold)
	for item in gameEnums.useItems:
		print(item.value[0]," ",item.name.replace("_"," "),": $G",item.value[1])
	itemToBuy = input()
	itemChosen = list(item for item in gameEnums.useItems if item.value[0] == itemToBuy)[0].name
	itemPrice = int(list(item for item in gameEnums.useItems if item.name == itemChosen)[0].value[1])
	itemCount = int(input("how many of %s?\n"%itemChosen))
	if player.totalGold >= itemPrice*itemCount:
		player.inventory[itemChosen] +=itemCount
		player.totalGold -= itemPrice*itemCount
	else:
		print("you don't have enough money for that! now scram!\n")
	return

def inventory(gameSurface,font,player):
	print("\n%s's inventory\n"%player.name)
	if sum([item for item in player.inventory.values()]) == 0:
		print("you don't have anything in your inventory!\n")
		return
	for item in player.inventory.keys():
		if player.inventory[item] > 0:
			print(item+": "+str(player.inventory[item]))
	choice = input("what would you like to use?\n")
	try:
		player.inventory[choice] -=1
		getEffect(player,choice)
	except KeyError:
		print("item not recognized!\n")
	return

def getEffect(player,choice):
	if choice == 'potion':
		player.health += 10
		if player.health > player.maxHP:
			player.health = player.maxHP
	elif choice == 'coffee':
		player.status = gameEnums.StatusEffect.fast
		player.statusDuration = 5
	elif choice == 'poison_flask':
		player.status = gameEnums.StatusEffect.givePoison
		player.statusDuration = 10
	elif choice == 'protein_shake':
		player.status = gameEnums.StatusEffect.hpUp
		player.statusDuration = 2
	elif choice == 'sharpening_oil':
		player.status = gameEnums.StatusEffect.dmgUp
		player.statusDuration = 2
	elif choice == 'energy_bar':
		player.status = gameEnums.StatusEffect.staminaUp
		player.statusDuration = 2
	return

def church(gameSurface,font,player):
	price = player.maxHP*1.5
	reviveText = font.render("would you like to revive for %s gold? y/n"%price,True,gameEnums.gameColors.offwhite.value)
	reviveRect = reviveText.get_rect()
	reviveRect.midtop = (400,100)

	aliveText = font.render("bless tha LAWD",True,gameEnums.gameColors.offwhite.value)
	aliveRect = aliveText.get_rect()
	aliveRect.midtop = (400,100)

	noMoneyText = font.render("you don't have enough money!",True,gameEnums.gameColors.offwhite.value)
	noMoneyRect = noMoneyText.get_rect()
	noMoneyRect.midtop = (400,145)

	noMoney = False

	while True:
		gameSurface.fill(gameEnums.gameColors.offblack.value)
		if not player.alive:
			gameSurface.blit(reviveText,reviveRect)
			if noMoney:
				gameSurface.blit(noMoneyText,noMoneyRect)
		elif player.alive:
			gameSurface.blit(aliveText,aliveRect)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_y and not player.alive:
					if player.totalGold >= price:
						player.alive = True
						player.health = player.maxHP
						player.totalGold -= price
					else:
						noMoney = True
				else:
					return
		pygame.display.flip()
	return
