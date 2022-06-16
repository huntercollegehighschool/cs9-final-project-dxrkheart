import main

if(main.n == 1):
    main.playerData.maxHealth = main.playerData.maxHealth * 2
    main.playerData.currentHealth = main.playerData.currentHealth * 2
elif(main.n == 2):
    main.playerData.maxHealth = main.playerData.maxHealth - (main.playerData.weaponDamage / 3)
    main.playerData.currentHealth = main.playerData.currentHealth - (main.playerData.weaponDamage / 3)
elif(main.n == 3):
    main.playerData.buffCritDamage += main.playerData.WeaponDamage - (main.playerData.armorDefense / 2)
elif(main.n == 4):
    main.playerData.buffDefense += main.playerData.weaponDamage / (main.playerData.weaponCritDamage / 2)
elif(main.n == 5):
    main.playerData.buffCritDamage += main.playerData.buffCritChance * main.playerData.buffDefense
elif(main.n == 6):
    main.playerData.buffSpeed = main.playerData.maxHealth / 8
elif(main.n == 7):
    main.playerData.buffDamage += main.playerData.buffCritDamage * 3
if(main.n == 7 and main.n1 == 7 and main.n2 == 7):
    main.playerData.buffSpeed = 777
    main.playerData.buffCritDamage = 777
    main.playerData.buffCritChance = 777
    main.playerData.buffDamage = 777
if(main.n == 6 and main.n1 == 6 and main.n2 == 6):
    main.playerData.buffDamage = -(main.playerData.weaponDamage) + 6
    main.playerData.buffDefense = -(main.playerData.armorDefense) + 6
    main.playerData.maxHealth = main.playerData.maxHealth / 6
    main.playerData.currentHealth = main.playerData.currentHealth / 6