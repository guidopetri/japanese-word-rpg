#!/usr/bin/env python3

from os.path import expanduser
from sys import platform as _platform

fontname = 'Arial'
fontsize = 32
width = 800
height = 600
player = None

if _platform == 'linux':
    savepath = '~/Edo/'
elif _platform == 'win32':
    savepath = '~/AppData/Roaming/Edo/'

savepath = expanduser(savepath)
