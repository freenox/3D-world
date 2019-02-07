# -*- coding: utf-8 -*-
"""
TEST PYGAME
"""

import pygame, sys
from random import randint

from pygame.locals import *

DIRT=0
GRASS=1
WATER=2
SAND=3
CLOUD=4

WHITE = (255,255,255)
BLACK = (0,0,0)
ressources = [DIRT, GRASS, WATER, SAND]

textures = {
        GRASS : pygame.image.load("grass.png"),
        WATER : pygame.image.load("water.png"),
        SAND : pygame.image.load("sand.png"),
        DIRT: pygame.image.load("dirt.png"),
        CLOUD: pygame.image.load("cloud.png")
        }

inventory= {
        GRASS : 0,
        WATER : 0,
        SAND : 0,
        DIRT: 0
        }


PLAYER=pygame.image.load("player.png")
playerPos=[0,0] #pos en [x,y]


size = 40
width = 20
height = 15

tiles = [[DIRT for w in range(width)] for h in range(height)]

for rw in range(height):
    for cl in range(width):
        x = randint(1,10)
        if x <= 2:
            tile=WATER
        elif x > 2 and x <= 8:
            tile=GRASS
        else:
            tile=SAND
            
        tiles[rw][cl]=tile

cloudx = -200
cloudy = 50

pygame.init()

DISPLAY = pygame.display.set_mode((width*size,height*size+80))
pygame.display.set_caption("First game")

INVFONT = pygame.font.Font("Aldo.ttf",18)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key==K_RIGHT and playerPos[0]<width-1:
                playerPos[0]+=1
            elif event.key == K_LEFT and playerPos[0]>0:
                playerPos[0]-=1
            elif event.key == K_UP and playerPos[1]>0:
                playerPos[1]-=1
            elif event.key == K_DOWN and playerPos[1]<height-1:
                playerPos[1]+=1
            if event.key == K_SPACE:
                currentTile=tiles[playerPos[1]][playerPos[0]]
                inventory[currentTile]+=1
                tiles[playerPos[1]][playerPos[0]] = DIRT
                print(inventory)
            if event.key == K_1:
                currentTile=tiles[playerPos[1]][playerPos[0]]
                if inventory[DIRT]>0:
                    inventory[DIRT]-=1
                    tiles[playerPos[1]][playerPos[0]]=DIRT
                    
        
    
    for row in range(height):
        for column in range(width):
            DISPLAY.blit(textures[tiles[row][column]], (column*size, row*size))
    
    #Player position
    DISPLAY.blit(PLAYER, (playerPos[0]*size, playerPos[1]*size))
    
    DISPLAY.blit(textures[CLOUD], (cloudx,cloudy))
    cloudx+=1
    if cloudx > width*size:
        cloudy=randint(0,height*size)
        cloudx=-200
        
    #Inventory display
    placePos = 10
    for item in ressources:
        #Image
        DISPLAY.blit(textures[item],(placePos, height*size+20))
        placePos+=30
        #Text
        textObj = INVFONT.render(str(inventory[item]), True, WHITE, BLACK)
        DISPLAY.blit(textObj, (placePos, height*size+20))
        placePos+=50
        
    
    
    pygame.display.update()