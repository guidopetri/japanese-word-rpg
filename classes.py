#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python 3.6.4

import random
import gameEnums

class enemyWord():
	def __init__(self,level):
		self.level = level
		self.expYield = self.level*random.randrange(5,11)
		self.goldYield = self.level*random.randrange(1,4)
		self.health = self.level*random.randrange(2,5)
		self.maxHP = self.health
		self.status = gameEnums.StatusEffect.normal
		self.alive = True
		return

	def pickWord(self,wordsDict):
		allWords = [x for y in wordsDict.values() for x in y]
		longWords = [x for y in wordsDict.values() for x in y if len(x) > 10]
		shortWords = [x for y in wordsDict.values() for x in y if len(x) < 6]
		if self.status == gameEnums.StatusEffect.normal:
			self.word = random.choice(allWords)
		elif self.status == gameEnums.StatusEffect.berserk:
			self.word = random.choice(longWords)
		elif self.status == gameEnums.StatusEffect.slow:
			self.word = random.choice(shortWords)
		return

	def takeDamage(self,amount):
		self.health -= amount
		if self.health <= 0:
			self.alive = False
			return
		if (self.health < self.maxHP/2) and (self.health > self.maxHP/4) and (self.status == gameEnums.StatusEffect.normal):
			print(" BERSERK!!")
			self.status = gameEnums.StatusEffect.berserk
		if (self.health < self.maxHP/4) and (self.status == gameEnums.StatusEffect.berserk):
			self.status = gameEnums.StatusEffect.slow
			print(" ..... slow .....")
		return

	def printWord(self):
		print(self.word)
		return

class PlayerCharacter():
	def __init__(self,playerName=None,playerClass=None,playerDict=None):
		if playerDict == None and playerName != None:
			self.name = playerName
			self.charClass = playerClass
			self.health = 10
			self.maxHP = 10
			self.level = 1
			self.kills = 0
			self.score = 0
			self.totalEXP = 0
			self.alive = True
			self.totalGold = 0
			self.goldMultiplier = 1.0
			self.dmgMultiplier = 1.0
			self.calculateClassBonuses()
		elif playerDict != None and playerName == None:
			self.name = playerDict['name']
			self.charClass = playerDict['charClass']
			self.health = playerDict['health']
			self.maxHP = playerDict['maxHP']
			self.level = playerDict['level']
			self.kills = playerDict['kills']
			self.score = playerDict['score']
			self.totalEXP = playerDict['totalEXP']
			self.alive = playerDict['alive']
			self.totalGold = playerDict['totalGold']
			self.goldMultiplier = playerDict['goldMultiplier']
			self.dmgMultiplier = playerDict['dmgMultiplier']
		self.calculateScoreMultiplier()
		self.calculateLevelThreshold()
		return

	def calculateClassBonuses(self):
		if self.charClass == gameEnums.playerClasses.fighter:
			self.maxHP = int(self.health*1.1)
			self.health = int(self.health*1.1)
			self.dmgMultiplier *= 1.1
		elif self.charClass == gameEnums.playerClasses.rogue:
			self.goldMultiplier *= 1.2
		elif self.charClass == gameEnums.playerClasses.wizard:
			self.dmgMultiplier *= 1.3
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

	def gainGold(self,amount):
		self.totalGold += int(amount*self.goldMultiplier)
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
		returnDict = {'name':self.name,
						'charClass':self.charClass,
						'health':self.health,
						'maxHP':self.maxHP,
						'level':self.level,
						'kills':self.kills,
						'score':self.score,
						'totalEXP':self.totalEXP,
						'alive':self.alive,
						'totalGold':self.totalGold,
						'goldMultiplier':self.goldMultiplier,
						'dmgMultiplier':self.dmgMultiplier
						}
		return returnDict
