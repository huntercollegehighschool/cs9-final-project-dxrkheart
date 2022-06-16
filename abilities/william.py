import main
import random

myList = ["brown", "gray", "purple", "green", "yellow", "cyan", "white", "orange", "pink", "lime", "blue", "red"]
main.n = random.choice(myList)
susValue = myList.index(main.n)
main.playerData.buffCritDamage += round(main.playerData.buffCritDamage * (1 + (0.01 * (susValue + 1) * 2)))