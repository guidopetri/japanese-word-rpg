#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# python 3.6.4

import menus


# random.seed(1)

def sort_words_len(all_words):
    import json
    from collections import defaultdict

    words_lengths = defaultdict(list)

    for word in all_words:
        words_lengths[len(word)].append(word)

    with open('wordsLen.ini', 'w') as file:
        json.dump(words_lengths, file)

    return


menus.mainMenu()
