import main

if(main.playerData.currentHealth < main.playerData.maxHealth / 4):
    main.playerData.buffDefense += main.playerData.armorDefense
    main.playerData.buffCritDamage += main.playerData.armorSpeed / 4
#did you see my wonderful discord message