#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# python 3.6.4

#import pygame
#import OpenGL
#import kivy
import sys
import menus

#random.seed(1)

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

menus.mainMenu()

sys.exit()