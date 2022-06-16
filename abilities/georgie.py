import main
import math

main.playerData.totalDamage = main.playerData.totalDamage + ((main.playerData.totalDefense) + math.sqrt((main.playerData.totalDefense ** 2) - (-4 * main.playerData.charmDamage * main.playerData.charmDefense))) / (2 * (main.playerData.charmDamage / 3))