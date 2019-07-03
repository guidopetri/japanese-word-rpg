#! /usr/bin/env python

from classes import LocationType
from collections import OrderedDict

location_types = OrderedDict([('grass', LocationType(name='grass',
                                                     level=0,
                                                     )),
                              ('city', LocationType(name='city',
                                                    level=-1)),
                              ('mountain', LocationType(name='mountain',
                                                        block_mv=True,
                                                        level=1)),
                              ('river', LocationType(name='river',
                                                     ship_mv=True,
                                                     level=1)),
                              ])
