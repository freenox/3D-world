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
pygame.display.set_caption("Tilemap Generator")


selectedTile=DIRT

while True:

    for event in pygame.event.get():
        pressed = pygame.mouse.get_pressed()
        if pressed[0]:
            (x,y) = pygame.mouse.get_pos()
            if x >0 and x < size*width and y < height*size and y>0:
                tiles[int(y/size)][int(x/size)]=selectedTile
            
            if y> height*size and x<(width-1)*size:
                selectedTile=ressources[int(x/size)]
                print(selectedTile)
            
            #SAVE BUTTON
            if y> height*size and x>(width-1)*size:
                save =  open('save.txt', 'w')
                for tile in tiles:
                    save.write("%s\n" % tile)
                save.close()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()                   
        
    
    for row in range(height):
        for column in range(width):
            DISPLAY.blit(textures[tiles[row][column]], (column*size, row*size))
            
    placePos = 0
    for item in ressources:
        #Image
        DISPLAY.blit(textures[item],(placePos, height*size))
        placePos+=size
    
    posSauv = ((width-1)*size,(height-1)*size)
    pygame.draw.rect(DISPLAY, (0,255,255), ((width-1)*size,
                     (height)*size,(width)*size,(height-1)*size))
    
    pygame.display.update()

