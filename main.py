#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# python 3.6.4

import random
import json
import pygame
import OpenGL
import sys
import time

#random.seed(1)

class enemyWord():
	def __init__(self,word):
		self.word = word
		return

	def printWord(self):
		print(self.word)
		return

with open('words.ini','r') as file:
	allWords = json.loads(file.read())

print("type it out! you have 60 seconds!")
startTime = time.time()
score = 0
finished = False
while not finished:
	enemy = enemyWord(random.choice(allWords))
	enemy.printWord()
	userInput = input()
	index = 0
	for character in list(enemy.word):
		if userInput[index:index+1] == character:
			score +=1
		index+=1
	if time.time()-startTime >= 60:
		finished = True

print("your score was %s"%score)
sys.exit()