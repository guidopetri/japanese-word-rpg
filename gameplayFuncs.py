#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 3.6.4


import classes
import difflib
import time
import random
import gameEnums
import pygame
import sys


def battle(gameSurface, font, player, allWords, gameTime):
    width = gameSurface.get_width()
    height = gameSurface.get_height()
    fastMode = False
    poisonMode = False
    if player.statusDuration > 0:
        if player.status == gameEnums.StatusEffect.staminaUp:
            gameTime *= 1.5
        elif player.status == gameEnums.StatusEffect.hpUp:
            oldHP = player.health
            player.health += 0.5 * player.maxHP
            player.maxHP *= 1.5
        elif player.status == gameEnums.StatusEffect.dmgUp:
            player.dmgMultiplier *= 2
        elif player.status == gameEnums.StatusEffect.fast:
            fastMode = True
        elif player.status == gameEnums.StatusEffect.givePoison:
            poisonMode = True
        player.statusDuration -= 1
        if player.statusDuration == 0:
            player.status = gameEnums.StatusEffect.normal
    if fastMode:
        player.difficulty -= 0.13

    passOutText = font.render("you're passed out! you can't battle!",
                              True,
                              gameEnums.gameColors.offblack.value)
    passOutRect = passOutText.get_rect()
    passOutRect.midtop = (width / 2, height / 30)

    instructionsText = font.render("type it out!",
                                   True,
                                   gameEnums.gameColors.offblack.value)
    instructionsRect = instructionsText.get_rect()
    instructionsRect.midtop = (width / 2, height / 30)

    healthText = font.render("HP: %s" % player.health,
                             True,
                             gameEnums.gameColors.offblack.value)
    healthRect = healthText.get_rect()
    healthRect.midtop = (width / 4, height / 30)

    hitText = font.render("HIT!!",
                          True,
                          gameEnums.gameColors.offblue.value)
    hitRect = hitText.get_rect()
    hitRect.midtop = (width / 2, height / 2 + 45)

    ouchText = font.render("OUCH!!",
                           True,
                           gameEnums.gameColors.offred.value)
    ouchRect = ouchText.get_rect()
    ouchRect.midtop = (width / 2, height / 2 + 45)

    backgroundSurface = pygame.Surface((width * 3 / 4 + 10, height - 20))
    backgroundSurface.fill(gameEnums.gameColors.bgblue.value)
    backgroundRect = backgroundSurface.get_rect()
    backgroundRect.midtop = (width / 2, 10)

    background = pygame.Surface((width * 3 / 4, height - 30))
    background.fill(gameEnums.gameColors.bgyellow.value)
    backgroundRect2 = background.get_rect()
    backgroundRect2.midtop = (backgroundRect.width / 2, 5)

    backgroundSurface.blit(background, backgroundRect2)

    # 1176x888
    # each is 294x296
    monsterImagesLocations = [(i, j) for i in [0, 294, 588, 882] for j in [0, 296, 592]]  # noqa
    currentMonsterImage = (0, 0, 0, 0)

    monsterImages = pygame.image.load('media/monsters.png')
    monsterPixelArray = pygame.PixelArray(monsterImages)
    monsterPixelArray.replace(gameEnums.gameColors.magenta.value,
                              pygame.Color(131, 232, 252), 0.4)  # wat
    del monsterPixelArray  # what the heck is this

    startTime = time.time()
    lastTime = startTime
    timeLeft = gameTime
    newWord = True
    typedWord = []
    gaveHit = False
    tookHit = False
    deadEnemy = False
    finished = False
    exit = False
    enemy = classes.enemyWord(random.randrange(1, 4))
    monsterChoice = random.choice(monsterImagesLocations)
    currentMonsterImage = (monsterChoice[0], monsterChoice[1], 294, 296)
    monsterRect = pygame.Rect(0, 0, 294, 296)
    monsterRect.midtop = (width / 2, height / 10 - 5)

    while True:
        gameSurface.fill(gameEnums.gameColors.offblack.value)
        gameSurface.blit(backgroundSurface, backgroundRect)
        if not player.alive:
            gameSurface.blit(passOutText, passOutRect)
            time.sleep(3)
            break
        elif player.alive:
            if not finished:
                gameSurface.blit(instructionsText, instructionsRect)
                if not enemy.alive:
                    player.gainEXP(enemy.expYield)
                    player.gainGold(enemy.goldYield)

                    deadText = font.render("ENEMY LEVEL %s KILLED!! 3 EXTRA SECONDS!!" % enemy.level,  # noqa
                                           True,
                                           gameEnums.gameColors.offblack.value)
                    deadRect = deadText.get_rect()
                    deadRect.midtop = (width / 2, 11 * height / 12)

                    enemy = classes.enemyWord(random.randrange(1, 4))
                    monsterChoice = random.choice(monsterImagesLocations)
                    currentMonsterImage = (monsterChoice[0],
                                           monsterChoice[1],
                                           294,
                                           296)
                    timeLeft += 3
                    player.kills += 1
                    deadEnemy = True
                if newWord:
                    enemy.pickWord(allWords)
                    wordText = font.render("%s" % enemy.word,
                                           True,
                                           gameEnums.gameColors.offblack.value)
                    wordRect = wordText.get_rect()
                    wordRect.midtop = (width / 2, height / 2 + 90)
                    newWord = False
                    typedWord = []
                timeLeftText = font.render("%ss left" % timeLeft,
                                           True,
                                           gameEnums.gameColors.offblack.value)
                timeLeftRect = timeLeftText.get_rect()
                timeLeftRect.midtop = (3 * width / 4, height / 30)

                gameSurface.blit(timeLeftText, timeLeftRect)
                gameSurface.blit(healthText, healthRect)

                gameSurface.blit(monsterImages,
                                 monsterRect,
                                 currentMonsterImage)

                typedText = font.render("".join(typedWord),
                                        True,
                                        gameEnums.gameColors.offblack.value)
                typedRect = typedText.get_rect()
                typedRect.midtop = (width / 2, height / 2 + 135)

                gameSurface.blit(wordText, wordRect)
                gameSurface.blit(typedText, typedRect)

                if gaveHit and not tookHit:
                    gameSurface.blit(hitText, hitRect)

                if tookHit and not gaveHit:
                    gameSurface.blit(ouchText, ouchRect)

                if deadEnemy:
                    gameSurface.blit(deadText, deadRect)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.unicode not in ['1', '2', '3', '4', '5', '6'] and event.key != pygame.K_RETURN and event.key != pygame.K_BACKSPACE:  # noqa
                            typedWord.append(event.unicode)
                        elif event.key == pygame.K_RETURN:
                            newWord = True
                            deadEnemy = False
                            if scoreWord(player.difficulty, enemy.word, "".join(typedWord)):  # noqa
                                gaveHit = True
                                tookHit = False
                                player.scorePoints(1)
                                enemy.takeDamage(player.dmgMultiplier)
                                if poisonMode:
                                    enemy.takeDamage(1)
                            else:
                                tookHit = True
                                gaveHit = False
                                player.takeDamage(1)
                                healthText = font.render("HP: %s" % player.health,  # noqa
                                                         True,
                                                         gameEnums.gameColors.offblack.value)  # noqa
                                healthRect = healthText.get_rect()
                                healthRect.midtop = (width / 4, height / 30)
                        elif event.key == pygame.K_BACKSPACE:
                            try:
                                del typedWord[len(typedWord) - 1]
                            except IndexError:
                                pass
                        elif event.key == pygame.K_1:
                            # for item usage during battle
                            pass
                        elif event.key == pygame.K_2:
                            pass
                        elif event.key == pygame.K_3:
                            pass
                        elif event.key == pygame.K_4:
                            pass
                        elif event.key == pygame.K_5:
                            pass
                        elif event.key == pygame.K_6:
                            pass

                if time.time() - lastTime > 1:
                    lastTime = time.time()
                    timeLeft -= 1
                if timeLeft == 0:
                    if time.time() - startTime >= gameTime or not player.alive:
                        finished = True
            elif finished:
                endText = font.render("your score was %s and you killed %s monsters," % (player.score, player.kills),  # noqa
                                      True,
                                      gameEnums.gameColors.offblack.value)  # noqa
                endRect = endText.get_rect()
                endRect.midtop = (width / 2, height / 2)

                endText2 = font.render("earning your level %s character" % player.level,  # noqa
                                       True,
                                       gameEnums.gameColors.offblack.value)
                endRect2 = endText2.get_rect()
                endRect2.midtop = (width / 2, height / 2 + 45)

                endText3 = font.render("%s exp and %s gold" % (player.totalEXP, player.totalGold),  # noqa
                                       True,
                                       gameEnums.gameColors.offblack.value)
                endRect3 = endText3.get_rect()
                endRect3.midtop = (width / 2, height / 2 + 90)

                gameSurface.blit(endText, endRect)
                gameSurface.blit(endText2, endRect2)
                gameSurface.blit(endText3, endRect3)
                pygame.display.flip()
                time.sleep(3)
                for event in pygame.event.get():  # clear event queue
                    pass
                while not exit:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            exit = True
                break
        pygame.display.flip()
    if 'oldHP' in locals():
        player.health = player.maxHP * (2 / 3) - (player.maxHP - player.health)
        player.maxHP *= (2 / 3)
    if fastMode:
        player.difficulty += 0.13
    return


def scoreWord(difficulty, word, userInput):
    return difflib.SequenceMatcher(None, word.lower(), userInput.lower()).ratio() >= difficulty  # noqa


def shop(gameSurface, font, player):
    print("buy somethin', will ya?\n")
    print("Gold: %s\n" % player.totalGold)
    for item in gameEnums.useItems:
        print(item.value[0], " ", item.name.replace("_", " "), ": $G", item.value[1])  # noqa
    itemToBuy = input()
    itemChosen = list(item for item in gameEnums.useItems if item.value[0] == itemToBuy)[0].name  # noqa
    itemPrice = int(list(item for item in gameEnums.useItems if item.name == itemChosen)[0].value[1])  # noqa
    itemCount = int(input("how many of %s?\n" % itemChosen))
    if player.totalGold >= itemPrice * itemCount:
        player.inventory[itemChosen] += itemCount
        player.totalGold -= itemPrice * itemCount
    else:
        print("you don't have enough money for that! now scram!\n")
    return


def inventory(gameSurface, font, player):
    print("\n%s's inventory\n" % player.name)
    if sum([item for item in player.inventory.values()]) == 0:
        print("you don't have anything in your inventory!\n")
        return
    for item in player.inventory.keys():
        if player.inventory[item] > 0:
            print(item + ": " + str(player.inventory[item]))
    choice = input("what would you like to use?\n")
    try:
        player.inventory[choice] -= 1
        getEffect(player, choice)
    except KeyError:
        print("item not recognized!\n")
    return


def getEffect(player, choice):
    if choice == 'potion':
        player.health += 10
        if player.health > player.maxHP:
            player.health = player.maxHP
    elif choice == 'coffee':
        player.status = gameEnums.StatusEffect.fast
        player.statusDuration = 5
    elif choice == 'poison_flask':
        player.status = gameEnums.StatusEffect.givePoison
        player.statusDuration = 10
    elif choice == 'protein_shake':
        player.status = gameEnums.StatusEffect.hpUp
        player.statusDuration = 2
    elif choice == 'sharpening_oil':
        player.status = gameEnums.StatusEffect.dmgUp
        player.statusDuration = 2
    elif choice == 'energy_bar':
        player.status = gameEnums.StatusEffect.staminaUp
        player.statusDuration = 2
    return


def church(gameSurface, font, player):
    width = gameSurface.get_width()
    height = gameSurface.get_height()
    price = player.maxHP * 1.5
    reviveText = font.render("would you like to revive for %s gold? y/n" % price,  # noqa
                             True,
                             gameEnums.gameColors.offblack.value)
    reviveRect = reviveText.get_rect()
    reviveRect.midtop = (width / 2, height / 4)

    aliveText = font.render("bless tha LAWD",
                            True,
                            gameEnums.gameColors.offblack.value)
    aliveRect = aliveText.get_rect()
    aliveRect.midtop = (width / 2, height / 4)

    noMoneyText = font.render("you don't have enough money!",
                              True,
                              gameEnums.gameColors.offblack.value)
    noMoneyRect = noMoneyText.get_rect()
    noMoneyRect.midtop = (width / 2, height / 4 + 45)

    backgroundSurface = pygame.Surface((width * 3 / 4, height / 4 - 10))
    backgroundSurface.fill(gameEnums.gameColors.bgblue.value)
    backgroundRect = backgroundSurface.get_rect()
    backgroundRect.midtop = (width / 2, height / 4 - 25)

    background = pygame.Surface((width * 3 / 4 - 10, height / 4 - 20))
    background.fill(gameEnums.gameColors.bgyellow.value)
    backgroundRect2 = background.get_rect()
    backgroundRect2.midtop = (backgroundRect.width / 2, 5)

    backgroundSurface.blit(background, backgroundRect2)

    noMoney = False

    while True:
        gameSurface.fill(gameEnums.gameColors.offblack.value)
        gameSurface.blit(backgroundSurface, backgroundRect)
        if not player.alive:
            gameSurface.blit(reviveText, reviveRect)
            if noMoney:
                gameSurface.blit(noMoneyText, noMoneyRect)
        elif player.alive:
            gameSurface.blit(aliveText, aliveRect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y and not player.alive:
                    if player.totalGold >= price:
                        player.alive = True
                        player.health = player.maxHP
                        player.totalGold -= price
                    else:
                        noMoney = True
                else:
                    return
        pygame.display.flip()
    return
