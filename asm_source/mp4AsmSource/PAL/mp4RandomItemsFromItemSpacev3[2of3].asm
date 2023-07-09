#To be inserted at 80082ED4
#patch text
#r27 holds string id to print
#817FFFF0 s32 holds chosen item id from earlier code

bl afterAsciiTable
.balign 4
itemAsciiTable:
.ascii "\x0BYou\x10got\x10"
	.asciz "a\x10\x1E\x05Mini\x10Mushroom\x1E\x08\x85\xFF"
.ascii "\x0BYou\x10got\x10"
	.asciz "a\x10\x1E\x05Mega\x10Mushroom\x1E\x08\x85\xFF"
.ascii "\x0BYou\x10got\x10"
	.asciz "a\x10\x1E\x05Super\x10Mini\x10Mushroom\x1E\x08\x85\xFF"
.ascii "\x0BYou\x10got\x10"
	.asciz "a\x10\x1E\x05Super\x10Mega\x10Mushroom\x1E\x08\x85\xFF"
.ascii "\x0BYou\x10got\x10"
	.asciz "a\x10\x1E\x05Mini\x10Mega\x10Hammer\x1E\x08\x85\xFF"
.ascii "\x0BYou\x10got\x10"
	.asciz "a\x10\x1E\x05Warp\x10Pipe\x1E\x08\x85\xFF"
.ascii "\x0BYou\x10got\x10"
	.ascii "a\x10\x1E\x05Swap\x10"
	.asciz "Card\x1E\x08\x85\xFF"
.ascii "\x0BYou\x10got\x10"
	.asciz "a\x10\x1E\x05Sparky\x10Sticker\x1E\x08\x85\xFF"
.ascii "\x0BYou\x10got\x10"
	.asciz "a\x10\x1E\x05Gaddlight\x1E\x08\x85\xFF"
.ascii "\x0BYou\x10got\x10"
	.ascii "a\x10\x1E\x05"
	.ascii "Chomp\x10"
	.asciz "Call\x1E\x08\x85\xFF"
.ascii "\x0BYou\x10got\x10"
	.ascii "a\x10\x1E\x05"
	.asciz "Bowser\x10Suit\x1E\x08\x85\xFF"
.ascii "\x0BYou\x10got\x10"
	.ascii "a\x10\x1E\x04"
	.ascii "Crystal\x10"
	.asciz "Ball\x1E\x08\x85\xFF"
.ascii "\x0BYou\x10got\x10"
	.asciz "a\x10\x1E\x07Magic\x10Lamp\x1E\x08\x85\xFF"
.balign 4
afterAsciiTable:
mflr r3 #pointer to ascii table
#parse ascii table and find pointer to item
lis r4, 0x817F
ori r4, r4, 0xFFF0
lwz r4, 0 (r4) #load chosen item id

asciiTableLoop:
#init loop
li r5, 0 #loop counter
li r6, 0 #found strings
	Loop:
	lbzx r7, r5, r3 #load char
	cmpwi r7, 0 #compare char to 0
	bne+ notZero
	#is zero
	cmpw r6, r4 #does item id == inner loop count
	beq- itemFound
	add r3, r3, r5
	addi r3, r3, 1 #point to next string
	addi r6, r6, 1 #increment string counter
	li r5, 0 #reset loop counter
	b Loop
	
	notZero:
	addi r5, r5, 1
	b Loop

itemFound:
mr r4, r3 #move ptr to string to r4
li r3, 0







