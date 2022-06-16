import main

list = []

for i in main.playerData.inventory['charms']:
    list.append(i.displayName)
if('diane' in list):
    main.playerData.buffDefense += main.playerData.armorDefense * 1.5