# -*- coding: utf-8 -*-

import pygame, sys

DIRT=0
GRASS=1
WATER=2
SAND=3
CLOUD=4

WHITE = (255,255,255)
BLACK = (0,0,0)

textures = {
        GRASS : pygame.image.load("grass.png"),
        WATER : pygame.image.load("water.png"),
        SAND : pygame.image.load("sand.png"),
        DIRT: pygame.image.load("dirt.png")
        }

size = 40

width = 20
height = 15

tiles = [[DIRT for w in range(width)] for h in range(height)]
ressources = [DIRT, GRASS, WATER, SAND]

#INIT GRAPHICS
pygame.init()
DISPLAY = pygame.display.set_mode((width*size,height*size+80))
pygame.display.set_caption("First game")

INVFONT = pygame.font.Font("Aldo.ttf",18)

selectedTile=DIRT

while True:

    for event in pygame.event.get():
        pressed = pygame.mouse.get_pressed()
        if pressed[0]:
            (x,y) = pygame.mouse.get_pos()
            if x >0 and x < size*width and y < height*size and y>0:
                tiles[int(y/size)][int(x/size)]=selectedTile
            
            if y> height*size:
                selectedTile=ressources[int(x/size)]
                print(selectedTile)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            print(event.key)
#            if event.key==K_RIGHT and playerPos[0]<width-1:
#                playerPos[0]+=1
#            elif event.key == K_LEFT and playerPos[0]>0:
#                playerPos[0]-=1
#            elif event.key == K_UP and playerPos[1]>0:
#                playerPos[1]-=1
#            elif event.key == K_DOWN and playerPos[1]<height-1:
#                playerPos[1]+=1
#            if event.key == K_SPACE:
#                currentTile=tiles[playerPos[1]][playerPos[0]]
#                inventory[currentTile]+=1
#                tiles[playerPos[1]][playerPos[0]] = DIRT
#                print(inventory)
#            if event.key == K_1:
#                currentTile=tiles[playerPos[1]][playerPos[0]]
#                if inventory[DIRT]>0:
#                    inventory[DIRT]-=1
#                    tiles[playerPos[1]][playerPos[0]]=DIRT
                    
        
    
    for row in range(height):
        for column in range(width):
            DISPLAY.blit(textures[tiles[row][column]], (column*size, row*size))
            
    placePos = 0
    for item in ressources:
        #Image
        DISPLAY.blit(textures[item],(placePos, height*size))
        placePos+=size
    
    pygame.display.update()

