#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python 3.6.4

import classes
import difflib
import time
import random

difficulty = 0.93

def battle(player,allWords,gameTime):
	print("type it out! you have %s seconds!"%gameTime)
	timeLimit = gameTime
	startTime = time.time()
	finished = False
	while not finished:
		enemy = classes.enemyWord(random.randrange(1,4))
		while enemy.alive:
			enemy.pickWord(allWords)
			enemy.printWord() #print it out
			userInput = input() #wait for user to type something then press Enter
			if scoreWord(enemy.word,userInput):
				print(" HIT!!")
				player.scorePoints(1)
				enemy.takeDamage(player.dmgMultiplier)
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

	print("your score was %s and you killed %s monsters, earning your level %s character %s exp and %s gold"%(player.score,player.kills,player.level,player.totalEXP,player.totalGold))
	return

def scoreWord(word,userInput):
	return difflib.SequenceMatcher(None,word.lower(),userInput.lower()).ratio() >= difficulty
