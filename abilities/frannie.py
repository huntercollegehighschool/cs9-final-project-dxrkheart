import main
itemNames = []
for i in main.playerData.inventory['charms']:
    itemNames.append(i.displayName)
if ('shinae' and 'morgan' and 'michelle a' in itemNames):  
    main.playerData.buffDefense = main.playerData.armorDefense * 4
    main.playerData.buffDamage = main.playerData.weaponDamage * 4