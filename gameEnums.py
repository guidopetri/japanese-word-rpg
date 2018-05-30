#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python 3.6.4

from enum import Enum

class StatusEffect(Enum):
	normal=1
	berserk=2
	slow=3

class playerClasses(Enum):
	fighter='fighter'
	rogue='rogue'
	wizard='wizard'
	