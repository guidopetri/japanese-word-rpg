#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# python 3.6.4

import random
import json
import pygame
import OpenGL
import sys
import time
from enum import Enum

#random.seed(1)

difficulty = 0.75

class StatusEffect(Enum):
	normal=1
	berserk=2
	slow=3

class enemyWord():
	def __init__(self,health):
		self.health = health
		self.maxHP = health
		self.status = StatusEffect.normal
		return

	def pickWord(self,wordsDict):
		allWords = [x for y in wordsDict.values() for x in y]
		longWords = [x for y in wordsDict.values() for x in y if len(x) > 10]
		shortWords = [x for y in wordsDict.values() for x in y if len(x) < 6]
		if self.status == StatusEffect.normal:
			self.word = random.choice(allWords)
		elif self.status == StatusEffect.berserk:
			print("BERSERK!!")
			self.word = random.choice(longWords)
		elif self.status == StatusEffect.slow:
			print("..... slow .....")
			self.word = random.choice(shortWords)
		return

	def takeDamage(self,amount):
		self.health -= amount
		if (self.health < self.maxHP/2) and (self.health > self.maxHP/4):
			self.status = StatusEffect.berserk
		if self.health < self.maxHP/4:
			self.status = StatusEffect.slow
		return

	def printWord(self):
		print(self.word)
		return

def scoreWord(word,userInput):
	score = 0
	index = 0
	for character in list(word): #for each character in the goal-word
		if userInput[index:index+1].lower() == character.lower(): #if the user's input on the same spot matches that character
			score +=1 #add one to the score
		index+=1 #next index
	if (score/len(word)) >= difficulty:
		return True
	else:
		return False

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

print("type it out! you have 60 seconds!")
startTime = time.time()
score = 0
finished = False
enemy = enemyWord(random.randrange(10,21))
originalHealth = enemy.health
while not finished:
	enemy.pickWord(allWords)
	enemy.printWord() #print it out
	userInput = input() #wait for user to type something then press Enter
	if scoreWord(enemy.word,userInput):
		score +=1
		enemy.takeDamage(1)
	if (time.time()-startTime >= 60) or enemy.health <= 0: #after 60 seconds
		finished = True #it's done

print("your score was %s out of %s"%(score,originalHealth))
sys.exit()