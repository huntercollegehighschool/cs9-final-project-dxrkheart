import main
list = []

for i in main.playerData.inventory['charms']:
    list.append(i.displayName)
if('david' in list):
    main.playerData.buffDamage = main.playerData.weaponDamage * 1.5