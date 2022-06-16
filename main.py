"""
Name(s): Ian, Felix
Name of Project: Ascend to Mr. Cheng
"""

import time
import pygame
import random
import os
import json
from renderer import *
#https://asciiart.club/ | The ASCII art generator we use for levels


levels = []
n1 = 0
n2 = 0
n3 = 0

for file_name in os.listdir('levels'):
    levels.append(file_name)

overlays = {}

for lev in levels:
    overlays.update({lev: []})
    for l in open("levels/" + lev):
        if l != '\n':
            l.replace('\n', '')
            overlays[lev].append(l)

class Battle:
    def __init__(self, playerData, enemy, frame):
        playerData.equippedCharm.triggerAbility("onBattleStart")
        self.log = ["", "", "", "", "", "", "", ""]
        self.enemy = enemy
        self.moveQueue = []
        self.playerData = playerData
        self.frame = frame
        playerData.playerMovementEnabled = False
        self.screenBlock = Shape.Rectangle(50, 45, [0,0], ' ')
        self.battleOverlay = Shape.Overlay([camera.anchor[0], camera.anchor[1]], ['@     vs.     '+ self.enemy.displayName[0], "", self.log[0], self.log[1], self.log[2], self.log[3], self.log[4], self.log[5], self.log[6], self.log[7]])
        self.frame.objects.append(self.screenBlock)
        self.frame.objects.append(self.battleOverlay)
        renderer.renderFrame(frame)
        camera.printScreen()
        enemy.battleAIUpdate(self)
            
    def enemyRanAway(self):
        ranAwayText = Shape.Text(camera.anchor[0], camera.anchor[1]+5, "Enemy ran away!")
        ranAwayText2 = Shape.Text(camera.anchor[0], camera.anchor[1]+6, "You were too intimidating.")
        ranAwayText3 = Shape.Text(camera.anchor[0], camera.anchor[1]+7, "Press [Y] to continue.")
        self.frame.objects.append(ranAwayText)
        self.frame.objects.append(ranAwayText2)
        self.frame.objects.append(ranAwayText3)
        frame.objects.append(self.battleOverlay)
        renderer.renderFrame(frame)
        camera.printScreen()
        while True:
            pygame.event.get()
            if pygame.key.get_pressed()[pygame.K_y] == True:
                break
        self.frame.objects.remove(ranAwayText)
        self.frame.objects.remove(ranAwayText2)
        self.frame.objects.remove(ranAwayText3)
        self.end()
    def submitMove(self, id, sender, value, type, speed):
        self.moveQueue.update({id: [sender, value, type, speed]})
    def end(self):
        self.frame.objects.remove(self.screenBlock)
        self.frame.objects.remove(self.battleOverlay)
        frame.objects.append(self.battleOverlay)
        renderer.renderFrame(frame)
        camera.printScreen()
        try:
            self.enemy.die()
        except:
            pass
        self.playerData.playerMovementEnabled = True
        
def Movement(colliders, overlay1, playerData):
    if playerData.playerMovementEnabled == True:
        movement = False
        inventoryOpen = False
        pygame.event.get()
        if pygame.key.get_pressed()[pygame.K_e] == True and inventoryOpen == False:
                playerData.playerMovementEnabled = False
                inventoryOpen = True
                invLocation = "base"
                screenBlock = Shape.Rectangle(50, 45, [0,0], ' ')
                inventoryOverlay = Shape.Overlay([camera.anchor[0], camera.anchor[1]], ["Equipped weapon: " + playerData.equippedWeapon.displayName, "Equipped armor: " + playerData.equippedArmor.displayName, "Equipped charm: " + playerData.equippedCharm.displayName, "0) Weapons", "1) Armor", "2) Charms", "3) Consumables", "Press a number to open the inventory..."])
                frame.objects.append(screenBlock)
                frame.objects.append(inventoryOverlay)
                renderer.renderFrame(frame)
                camera.printScreen()
                while inventoryOpen:
                    pygame.event.get()
                    if(invLocation == "base"):
                        if(pygame.key.get_pressed()[pygame.K_0] == True):
                            num = 0
                            inventoryOverlay.dArray = []
                            inventoryOverlay.update()
                            inventoryOverlay.dArray.append("Weapons:")
                            for item in playerData.inventory["weapon"]:
                                inventoryOverlay.dArray.append(str(num) + ") " + item.displayName + ", dmg: " + str(item.damage) + ", crit dmg: " + str(item.critDamage) + ", dura: " + str(item.durability))
                                num = num + 1
                            invLocation = "weapon"
                            inventoryOverlay.update()
                            renderer.renderFrame(frame)
                            camera.printScreen()
                        elif(pygame.key.get_pressed()[pygame.K_1] == True):
                            num = 0
                            inventoryOverlay.dArray = []
                            inventoryOverlay.update()
                            inventoryOverlay.dArray.append("Armors:")
                            for item in playerData.inventory["armor"]:
                                inventoryOverlay.dArray.append(str(num) + ") " + item.displayName + ", def: " + str(item.defense) + ", speed: " + str(item.speed))
                                num = num + 1
                            invLocation = "armor"
                            inventoryOverlay.update()
                            renderer.renderFrame(frame)
                            camera.printScreen()
                        elif(pygame.key.get_pressed()[pygame.K_2] == True):
                            num = 0
                            inventoryOverlay.dArray = []
                            inventoryOverlay.update()
                            inventoryOverlay.dArray.append("Charms:")
                            for item in playerData.inventory["charm"]:
                                inventoryOverlay.dArray.append(str(num) + ") " + item.displayName + " a magical object; no description")
                                num = num + 1
                            invLocation = "charm"
                            inventoryOverlay.update()
                            renderer.renderFrame(frame)
                            camera.printScreen()
                        elif(pygame.key.get_pressed()[pygame.K_3] == True):
                            num = 0
                            inventoryOverlay.dArray = []
                            inventoryOverlay.update()
                            inventoryOverlay.dArray.append("Consumables:")
                            for item in playerData.inventory["consumable"]:
                                inventoryOverlay.dArray.append(str(num) + ") " + item.displayName + ", health restored: " + str(item.healthRestored))
                                num = num + 1
                            invLocation = "consumable"
                            inventoryOverlay.update()
                            renderer.renderFrame(frame)
                            camera.printScreen()
                        if(invLocation == "weapon" or invLocation == "armor" or invLocation == "charm" or invLocation == "consumable"):
                            try:
                                if(pygame.key.get_pressed()[pygame.K_0] == True):
                                    playerData.inventory[invLocation][0].equipItem(playerData)
                                elif(pygame.key.get_pressed()[pygame.K_1] == True):
                                    playerData.inventory[invLocation][1].equipItem(playerData)
                                elif(pygame.key.get_pressed()[pygame.K_2] == True):
                                    playerData.inventory[invLocation][2].equipItem(playerData)
                                elif(pygame.key.get_pressed()[pygame.K_3] == True):
                                    playerData.inventory[invLocation][3].equipItem(playerData)
                                elif(pygame.key.get_pressed()[pygame.K_4] == True):
                                    playerData.inventory[invLocation][4].equipItem(playerData)
                                elif(pygame.key.get_pressed()[pygame.K_5] == True):
                                    playerData.inventory[invLocation][5].equipItem(playerData)
                                elif(pygame.key.get_pressed()[pygame.K_6] == True):
                                    playerData.inventory[invLocation][6].equipItem(playerData)
                                elif(pygame.key.get_pressed()[pygame.K_7] == True):
                                    playerData.inventory[invLocation][7].equipItem(playerData)
                                elif(pygame.key.get_pressed()[pygame.K_8] == True):
                                    playerData.inventory[invLocation][8].equipItem(playerData)
                                elif(pygame.key.get_pressed()[pygame.K_9] == True):
                                    playerData.inventory[invLocation][9].equipItem(playerData)

                            except:
                                pass

                    if(pygame.key.get_pressed()[pygame.K_e] == True and inventoryOpen == True):
                        frame.objects.remove(screenBlock)
                        frame.objects.remove(inventoryOverlay)
                        renderer.renderFrame(frame)
                        camera.printScreen()
                        inventoryOpen = False
                        playerData.playerMovementEnabled = True
                            

                            
        if pygame.key.get_pressed()[pygame.K_d] == True:
            try:
                if screen.renderedFrame[player.y][player.x + 1] not in colliders:
                    player.x += 1
                    camera.anchor[0] += 1
                    movement = True
            except:
                pass
        elif pygame.key.get_pressed()[pygame.K_w] == True:
            try:
                if screen.renderedFrame[player.y -
                                        1][player.x] not in colliders:
                    player.y -= 1
                    camera.anchor[1] -= 1
                    movement = True
            except:
                pass
        elif pygame.key.get_pressed()[pygame.K_a] == True:
            try:
                if screen.renderedFrame[player.y][player.x -
                                                  1] not in colliders:
                    player.x -= 1
                    camera.anchor[0] -= 1
                    movement = True
            except:
                pass
        elif pygame.key.get_pressed()[pygame.K_s] == True:
            try:
                if screen.renderedFrame[player.y + 1][player.x] not in colliders:
                    player.y += 1
                    camera.anchor[1] += 1
                    movement = True
            except:
                pass

        if movement == True:
            playerData.equippedCharm.triggerAbility("onMovement")
            if camera.anchor[1] < player.y:
                camera.anchor[1] = player.y
            camera.clearEdgeClipping()
            if player.x < 0:
                player.x = 0
            if player.y < 0:
                player.y = 0
            if player.y > screen.screenH - 4:
                player.y = screen.screenH - 4
            overlay1.anchor = [camera.anchor[0], camera.anchor[1] + 17]
            overlay1.update()
            #print(camera.anchor)
            #print(overlay.anchor)
            player.update()
            for i in floorItems:
                i.update()
            for e in enemies:
                e.update()
            overlay1.dArray = [
    '____________________________________________________________',
    'HP: ' + str(playerData.currentHealth), updateStr
    ]    

            renderer.renderFrame(frame)
            hCounter = 0
            wCounter = 0
            camera.printScreen()
            time.sleep(0.1)

class Enemy:
    def __init__(self, displayName, hp, attack, defense, speed, frame, player, playerData, lootTable, x, y):
        self.displayName = displayName
        self.maxHP = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.x = x
        self.y = y
        self.frame = frame
        self.active = True
        self.player = player
        self.playerData = playerData
        self.lootTable = lootTable
        self.point = Shape.Point(self.x, self.y, "x")
        frame.objects.append(self.point)
    def update(self):
        if self.active == True:
            if player.x == self.x and player.y == self.y:
                newBattle = Battle(self.playerData, self, self.frame)
                
    def battleAIUpdate(self, battle):
        if self.hp <= 0:
            self.die(battle)
        if battle.playerData.currentHealth > 0:
            battle.enemyRanAway()
        elif battle.playerData.currentHealth > 5 * self.hp:
            self.guard(battle)
            
    def attackPlayer(self, battle):
        damage = self.attack - battle.playerData.defense 
        if damage <= 0:
            damage = 3
        battle.submitMove(2, "enemy", damage, "attack", self.speed)

    def guard(self, battle):
        battle.submitMove(2, "enemy", self.defense, "defense", self.speed)
            
    def die(self, battle):
        battle.end()
        frame.objects.remove(self.point)
        self.active = False
        
def InitLevel(level):
    levelOverlay = Shape.Overlay([0, 0], overlays[level][0:22][0:50])
    frame.objects.append(levelOverlay)
    player.x = int(overlays[level][23])
    player.y = int(overlays[level][24])
    return level

def indexJSONItems():
    lootTable = json.load(open('items.json'))
    lootIndex = []
    for l in lootTable:
        if lootTable[l]['itemType'] == 'weapon':
            lootIndex.append(Weapon(lootTable[l]['displayName'], lootTable[l]['damage'], lootTable[l]['durability'], lootTable[l]['critDamage']))
        elif lootTable[l]['itemType'] == 'armor':
            lootIndex.append(Armor(lootTable[l]['displayName'], lootTable[l]['defense'], lootTable[l]['speed']))
        elif lootTable[l]['itemType'] == 'consumable':
            lootIndex.append(Consumable(lootTable[l]['displayName'], lootTable[l]['healthRestored']))
        elif lootTable[l]['itemType'] == 'charm':
            lootIndex.append(Charm(lootTable[l]['charmDamage'], lootTable[l]['charmDefense'], lootTable[l]['charmSpeed'], lootTable[l]['charmCritDamage'], lootTable[l]['charmCritChance'], lootTable[l]['charmMaidens'], lootTable[l]['displayName'], open('abilities/'+lootTable[l]['ability']).read(), lootTable[l]['abilityName'], lootTable[l]['trigger'], lootTable[l]['triggerAmt']))
    return lootIndex

def indexJSONEnemies():
    enemyTable = json.load(open('enemies.json'))
    enemyIndex = []
    for e in enemyTable:
        enemyIndex.append(Enemy(enemyTable[e]['displayName'], enemyTable[e]['hp'], enemyTable[e]['attack'], enemyTable[e]['defense'], enemyTable[e]['speed'], frame, player, playerData, enemyTable[e]['lootTable'], 0, 0))
    return enemyIndex

def levelLootGeneration():
    print("Indexing generated loot...")
    print("Indexing generated creatures...")
    lootTable = json.load(open('lootTables/LootTable' + currentLevel + '.json'))
    weightsList = []
    for w in list(lootTable.values()):
        weightsList.append(int(w))
    lootIndex = indexJSONItems()
    enemyIndex = indexJSONEnemies()
    enemyTable = json.load(open('lootTables/EnemyTable' + currentLevel + '.json'))
    enemyWeightsList = []
    for w in list(enemyTable.values()):
        enemyWeightsList.append(int(w))
    nameEnemyDict = {}
    finalEnemyList = []
    for l in enemyTable.keys():
        for e in enemyIndex:
            if e.displayName == l:
                nameEnemyDict.update({l: e})
    nameLootDict = {}
    finalList = []
    for l in lootTable.keys():
        for i in lootIndex:
            if i.displayName == l.lower():
                nameLootDict.update({l: i})
    for h in range(0, len(screen.renderedFrame) - 3):
        for w in range(0, len(screen.renderedFrame[h])):
            if screen.renderedFrame[h][w] not in "⣿⠿⠾⠽⠼⠻⠺⠹⠸⠷⠶⠵⠴⠳⠲⠱⠰⠯⠮⠬⠫⠪⠩⠨⠧⠥⠤⠭⠣⠡⠟⠞⠝⠜⠍⠎⠏⠓⠔⠕⠖⠗⠘⠙⠚⠚⠇⠅⠃":
                choice = random.choices(list(lootTable.keys()), weights = weightsList)[0]
                choice2 = random.choices(list(enemyTable.keys()), weights = enemyWeightsList)[0]
                if choice == 'none':
                    pass
                else:
                    final = FloorItem(w, h, nameLootDict[choice].displayName[0], nameLootDict[choice], playerData)
                    finalList.append(final)
                if choice2 == 'none':
                    pass
                else: 
                    final = Enemy(nameEnemyDict[choice2].displayName, nameEnemyDict[choice2].hp, nameEnemyDict[choice2].attack, nameEnemyDict[choice2].defense, nameEnemyDict[choice2].speed, frame, player, playerData, nameEnemyDict[choice2].lootTable, w, h)
                    finalEnemyList.append(final)
    return [finalList, finalEnemyList]

class Item:
    def giveToPlayer(self, playerData):
        playerData.inventory[self.itemType].append(self)
    def equipItem(self, player):
        if(self.itemType == "weapon"):
            player.equippedWeapon = self
        elif(self.itemType == "armor"):
            player.equippedArmor = self
        elif(self.itemType == "consumable"):
            player.currentHealth += self.healthRestored
            if(player.currentHealth > player.maxHealth):
                player.currentHealth = player.maxHealth
        elif(self.itemType == "charm"):
            player.equippedCharm = self
        player.recalcBaseStats()
        player.recalcStats()
class Weapon(Item):
    def __init__(self, displayName, damage, durability, critDamage):
        self.itemType = "weapon"
        self.displayName = displayName
        self.damage = damage
        self.durability = durability
        self.critDamage = critDamage
class Armor(Item):
    def __init__(self, displayName, defense, speed):
        self.itemType = "armor"
        self.displayName = displayName
        self.defense = defense
        self.speed = speed
class Consumable(Item):
    def __init__(self, displayName, healthRestored):
        self.itemType = "consumable"
        self.displayName = displayName
        self.healthRestored = healthRestored

class PlayerData:
    def __init__(self):
        self.maxHealth = 100
        self.currentHealth = 100
        self.inventory = {
            "weapon": [],
            "armor": [],
            "comsumable": [],
            "charm": []
        }
        self.equippedWeapon = Weapon("fists", 1, 3, 2)
        self.equippedArmor = Armor("band-aid", 1, 2)
        self.weaponDamage = self.equippedWeapon.damage
        self.armorDefense = self.equippedArmor.defense
        self.equippedCharm = Charm(0, 0, 0, 0, 0, 0, "none", "none.py", "gamer moment", "but what if it triggered somehow...", True)
        self.buffDamage = self.equippedCharm.charmDamage
        self.buffDefense = self.equippedCharm.charmDefense
        self.baseCritDamage = 50
        self.buffCritDamage = self.equippedCharm.charmCritDamage
        self.critChance = 25
        self.buffCritChance = self.equippedCharm.charmCritChance
        self.weaponCritDamage = self.equippedWeapon.critDamage
        self.baseSpeed = 10
        self.playerMovementEnabled = True
        self.buffSpeed = self.equippedCharm.charmSpeed
        self.armorSpeed = self.equippedArmor.speed
        self.maidens = self.equippedCharm.charmMaidens
    def update(self):
        self.weaponDamage = self.equippedWeapon.damage
        self.armorDefense = self.equippedArmor.defense
        self.buffDamage = self.equippedCharm.charmDamage
        self.buffDefense = self.equippedCharm.charmDefense
        self.weaponCritDamage = self.equippedWeapon.critDamage
        self.buffCritDamage = self.equippedCharm.charmCritDamage
        self.armorSpeed = self.equippedArmor.speed
        self.buffSpeed = self.equippedCharm.charmSpeed
        self.buffCritChance = self.equippedCharm.charmCritChance
    def die(self):
        playerData = PlayerData()
        self.playerMovementEnabled = False
        frame = Frame([])
        endText = Shape.Text(camera.anchor[0], camera.anchor[1], "You perished...")
        frame.objects.append(endText)
        MainMenu()

        player = Shape.Point(0, 0, '@')
        playerData = PlayerData()

        lootNameDict = {}
        for l in indexJSONItems():
            lootNameDict.update({l.displayName: l})

        enemyNameDict = {}
        for e in indexJSONEnemies():
            enemyNameDict.update({l.displayName: l})

        updateStr = ""
        screen = Screen(50, 25)
        currentLevel = InitLevel(random.choice(['level1.txt', 'level2.txt', 'level3.txt']))
        camera = Camera([player.x, player.y], 40, 20, screen)
        camera.clearEdgeClipping()
        renderer = Renderer(screen, " ")
        overlay = Shape.Overlay([0, 0], [])
        frame.objects.append(player)
        frame.objects.append(overlay)
        playerData.playerMovementEnabled = True
        renderer.renderFrame(frame)
        generatedLoot = levelLootGeneration()
        floorItems = generatedLoot[0]
        enemies = generatedLoot[1]
        camera.printScreen()
        

class FloorItem:
    def __init__(self, x, y, char, item, player):
        self.x = x
        self.y = y
        self.char = char
        self.type = item.itemType
        self.item = item
        self.player = player
        self.claimed = False
        self.point = Shape.Point(self.x, self.y, self.char)
        frame.objects.append(self.point)
    def update(self):
        if (player.x == self.x and player.y == self.y and self.claimed == False):
            self.item.giveToPlayer(self.player)
            self.claimed = True
            frame.objects.remove(self.point)

class Charm(Item):
    def __init__(self, charmDamage, charmDefense, charmSpeed, charmCritDamage, charmCritChance, charmMaidens, displayName, ability, abilityName, trigger, triggerAmt):
        self.itemType = 'charm'
        self.charmDamage = charmDamage
        self.charmDefense = charmDefense
        self.charmSpeed = charmSpeed
        self.charmCritDamage = charmCritDamage
        self.charmCritChance = charmCritChance
        self.charmMaidens = charmMaidens
        self.displayName = displayName
        self.ability = ability
        self.trigger = trigger
        self.abilityName = abilityName
        self.triggerAmt = triggerAmt
    def equip(self):
        if self.trigger == 'onEquip':
            self.triggerAbility('onEquip')
    def triggerAbility(self, trig):
        if self.trigger == trig:
            if self.triggerAmt:
                exec(self.ability)
            elif self.triggerAmt > 0:
                exec(self.ability)
                self.triggerAmt -= 1
pygame.init()
pygame.display.set_mode([3000, 3000])

frame = Frame([])

def MainMenu():
    screen = Screen(50, 45)
    camera = Camera([5, 5], 45, 20, screen)
    renderer = Renderer(screen, " ")
    mainMenu = Shape.Text(5, 10, "CS-9: THE GAME")
    mainMenu2 = Shape.Text(5, 12, "Ascend the throne of the Dark Lord Mannix!")
    mainMenu3 = Shape.Text(5, 14, "(Click the above window for keyboard input)")
    mainMenu4 = Shape.Text(5, 16, "(E to open inventory, WASD to move)")
    mainMenu5 = Shape.Text(5, 18, "Press [Y] to continue.")

    frame = Frame([mainMenu, mainMenu2, mainMenu3, mainMenu4, mainMenu5])
    renderer.renderFrame(frame)
    camera.printScreen()
    while True:
        pygame.event.get()
        if pygame.key.get_pressed()[pygame.K_y] == True:
            break


MainMenu()

player = Shape.Point(0, 0, '@')
playerData = PlayerData()

lootNameDict = {}
for l in indexJSONItems():
    lootNameDict.update({l.displayName: l})

enemyNameDict = {}
for e in indexJSONEnemies():
    enemyNameDict.update({l.displayName: l})

updateStr = ""
screen = Screen(50, 25)
currentLevel = InitLevel(random.choice(['level1.txt', 'level2.txt', 'level3.txt']))
camera = Camera([player.x, player.y], 40, 20, screen)
camera.clearEdgeClipping()
renderer = Renderer(screen, " ")
overlay = Shape.Overlay([0, 0], [])
frame.objects.append(player)
frame.objects.append(overlay)
playerData.playerMovementEnabled = True
renderer.renderFrame(frame)
generatedLoot = levelLootGeneration()
floorItems = generatedLoot[0]
enemies = generatedLoot[1]
camera.printScreen()

while True:
    Movement("⣿⠿⠾⠽⠼⠻⠺⠹⠸⠷⠶⠵⠴⠳⠲⠱⠰⠯⠮⠬⠫⠪⠩⠨⠧⠥⠤⠭⠣⠡⠟⠞⠝⠜⠍⠎⠏⠓⠔⠕⠖⠗⠘⠙⠚⠚⠇⠅⠃", overlay, playerData)
