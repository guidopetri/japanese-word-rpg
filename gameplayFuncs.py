#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python 3.6.4

import classes
import difflib
import time
import random
import gameEnums

def battle(player,allWords,gameTime):
	if not player.alive:
		print("you're passed out! you can't battle!\n")
		return
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
	print("type it out! you have %s seconds!"%gameTime)
	print(player.health)
	timeLimit = gameTime
	startTime = time.time()
	finished = False
	while not finished:
		enemy = classes.enemyWord(random.randrange(1,4))
		while enemy.alive:
			enemy.pickWord(allWords)
			enemy.printWord() #print it out
			userInput = input() #wait for user to type something then press Enter
			if scoreWord(player.difficulty,enemy.word,userInput):
				print(" HIT!! %s"%enemy.health)
				player.scorePoints(1)
				enemy.takeDamage(player.dmgMultiplier)
				if poisonMode:
					enemy.takeDamage(1)
			else:
				print(" OUCH!!")
				player.takeDamage(1)
			if (time.time()-startTime >= timeLimit) or (not player.alive): #after 60 seconds
				finished = True #it's done
				break;
		timeLimit+=3
		player.gainEXP(enemy.expYield)
		player.gainGold(enemy.goldYield)
		if finished == True: #it's done
				break;
		print(" ENEMY LEVEL %s KILLED!! 3 EXTRA SECONDS!! %s TIME LEFT!!" % (enemy.level,int(timeLimit-time.time()+startTime)))
		player.kills +=1

	if 'oldHP' in locals():
		player.health = player.maxHP*(2/3)-(player.maxHP-player.health)
		player.maxHP *= (2/3)
	if fastMode:
		player.difficulty +=0.13
	print("your score was %s and you killed %s monsters, earning your level %s character %s exp and %s gold"%(player.score,player.kills,player.level,player.totalEXP,player.totalGold))
	return

def scoreWord(difficulty,word,userInput):
	return difflib.SequenceMatcher(None,word.lower(),userInput.lower()).ratio() >= difficulty

def shop(player):
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

def inventory(player):
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
