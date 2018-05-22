#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# python 3.6.4

import random
import json
#import pygame
#import OpenGL
import sys
import time
from enum import Enum
import difflib

#random.seed(1)

difficulty = 0.93

class StatusEffect(Enum):
	normal=1
	berserk=2
	slow=3

class enemyWord():
	def __init__(self,level):
		self.level = level
		self.expYield = self.level*random.randrange(5,11)
		self.goldYield = self.level*random.randrange(1,4)
		self.health = self.level*random.randrange(2,5)
		self.maxHP = self.health
		self.status = StatusEffect.normal
		self.alive = True
		return

	def pickWord(self,wordsDict):
		allWords = [x for y in wordsDict.values() for x in y]
		longWords = [x for y in wordsDict.values() for x in y if len(x) > 10]
		shortWords = [x for y in wordsDict.values() for x in y if len(x) < 6]
		if self.status == StatusEffect.normal:
			self.word = random.choice(allWords)
		elif self.status == StatusEffect.berserk:
			self.word = random.choice(longWords)
		elif self.status == StatusEffect.slow:
			self.word = random.choice(shortWords)
		return

	def takeDamage(self,amount):
		self.health -= amount
		if self.health <= 0:
			self.alive = False
			return
		if (self.health < self.maxHP/2) and (self.health > self.maxHP/4) and (self.status == StatusEffect.normal):
			print(" BERSERK!!")
			self.status = StatusEffect.berserk
		if (self.health < self.maxHP/4) and (self.status == StatusEffect.berserk):
			self.status = StatusEffect.slow
			print(" ..... slow .....")
		return

	def printWord(self):
		print(self.word)
		return

class PlayerCharacter():
	def __init__(self,playerName='Player1',health=10,maxHP=10,level=1,kills=0,score=0,totalEXP=0,alive=True,totalGold=0):
		self.name = playerName
		self.health = health
		self.maxHP = maxHP
		self.level = level
		self.kills = kills
		self.score = score
		self.calculateScoreMultiplier()
		self.totalEXP = totalEXP
		self.alive = alive
		self.totalGold = totalGold
		self.calculateLevelThreshold()
		return

	def takeDamage(self,amount):
		self.health -= amount
		if self.health <= 0:
			self.alive = False
		return

	def gainEXP(self,amount):
		self.totalEXP += amount
		if self.EXPThreshold-self.totalEXP <= 0:
			self.levelUp()
		return

	def levelUp(self):
		print(" LEVEL UP!!")
		self.level += 1
		self.health = self.maxHP
		self.calculateLevelThreshold()
		print(" NEXT LEVEL AT %s!!"%self.EXPThreshold)
		self.calculateScoreMultiplier()
		return

	def calculateScoreMultiplier(self):
		self.scoreMultiplier = 1.0*(self.level**1.3)
		return

	def calculateLevelThreshold(self):
		self.EXPThreshold = 43.65*((self.level+1)**3)
		return

	def scorePoints(self,amount):
		self.score += int(amount*self.scoreMultiplier)
		return

	def toJSON(self):
		returnDict = {'name':self.name,'health':self.health,'maxHP':self.maxHP,'level':self.level,'kills':self.kills,'score':self.score,'totalEXP':self.totalEXP,'alive':self.alive,'totalGold':self.totalGold}
		return returnDict

def scoreWord(word,userInput):
	return difflib.SequenceMatcher(None,word.lower(),userInput.lower()).ratio() >= difficulty

def sortWordsByLength(allWords):
	wordsLenDict = {}
	for word in allWords:
		try:
			wordsLenDict[len(word)].append(word)
		except KeyError:
			wordsLenDict[len(word)] = [word]
	with open('wordsLen.ini','w') as file:
		json.dump(wordsLenDict,file)
	return

with open('wordsLen.ini','r') as file:
	allWords = json.loads(file.read())

try:
	with open('player.ini','r') as file:
		playerData = json.loads(file.read())

	print([x for x in playerData.keys()],sep=' ',end='\n')
	playerName = input("who are you?\n")
	try:
		player = PlayerCharacter(playerData[playerName]['name'],playerData[playerName]['health'],playerData[playerName]['maxHP'],playerData[playerName]['level'],playerData[playerName]['kills'],playerData[playerName]['score'],playerData[playerName]['totalEXP'],playerData[playerName]['alive'],playerData[playerName]['totalGold'])
	except KeyError:
		print("player doesn't exist")
		playerName = input("what's your name?\n")
		player = PlayerCharacter(playerName=playerName)
except FileNotFoundError:
	playerData = {}
	playerName = input("what's your name?\n")
	player = PlayerCharacter(playerName=playerName)

print("type it out! you have 60 seconds!")
timeLimit = 60
startTime = time.time()
finished = False
while not finished:
	enemy = enemyWord(random.randrange(1,4))
	while enemy.alive:
		enemy.pickWord(allWords)
		enemy.printWord() #print it out
		userInput = input() #wait for user to type something then press Enter
		if scoreWord(enemy.word,userInput):
			print(" HIT!!")
			player.scorePoints(1)
			enemy.takeDamage(1)
		else:
			print(" OUCH!!")
			player.takeDamage(1)
		if (time.time()-startTime >= timeLimit) or (not player.alive): #after 60 seconds
			finished = True #it's done
			break;
	timeLimit+=3
	player.gainEXP(enemy.expYield)
	player.totalGold += enemy.goldYield
	if finished == True: #it's done
			break;
	print(" ENEMY LEVEL %s KILLED!! 3 EXTRA SECONDS!! %s TIME LEFT!!" % (enemy.level,int(timeLimit-time.time()+startTime)))
	player.kills +=1

print("your score was %s and you killed %s monsters, earning your level %s character %s exp and %s gold"%(player.score,player.kills,player.level,player.totalEXP,player.totalGold))

playerData[player.name] = player.toJSON()

with open('player.ini','w') as file:
	json.dump(playerData,file)

sys.exit()