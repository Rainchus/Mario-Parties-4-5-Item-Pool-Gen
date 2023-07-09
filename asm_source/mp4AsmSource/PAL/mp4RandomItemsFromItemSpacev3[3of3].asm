#To be inserted at 80083B9C
lis r4, 0x817f
ori r4, r4, 0xfff0
lwz r4, 0 (r4) #load new item to give player
