# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 17:45:41 2019

@author: Freenox
"""
from IPython import get_ipython

get_ipython().magic('reset -f')

import wireframe as wf
import pygame, sys
import numpy as np
 
key_to_function = {
    97: (lambda x: x.translateAll([-10, 0, 0])),
    100:(lambda x: x.translateAll([ 10, 0, 0])),
    273: (lambda x: x.translateAll([0,  10, 0])),
    274:   (lambda x: x.translateAll([0, -10, 0])),
    119: (lambda x: x.scaleAll([1.1, 1.1, 1.1])),
    115:  (lambda x: x.scaleAll([.9,.9,.9])),
#    pygame.K_q: (lambda x: x.rotateAll('X',  0.1)),
#    pygame.K_w: (lambda x: x.rotateAll('X', -0.1)),
#    pygame.K_a: (lambda x: x.rotateAll('Y',  0.1)),
#    pygame.K_s: (lambda x: x.rotateAll('Y', -0.1)),
#    pygame.K_z: (lambda x: x.rotateAll('Z',  0.1)),
#    pygame.K_x: (lambda x: x.rotateAll('Z', -0.1))
}


class ProjectionViewer:
    """Displays 3D on pygame screen"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Wireframe Viewer")
        self.background = (10,10,50)
        self.wireframes = {}
        self.displayNodes = False
        self.displayEdges = True
        self.nodeColor = (255,255,255)
        self.edgeColor = (200,200,200)
        self.nodeRadius = 4
        
    def display(self):
        self.screen.fill(self.background)
        for wireframe in self.wireframes.values():
            if self.displayEdges:
                for n1, n2 in wireframe.edges:
                    pygame.draw.aaline(self.screen, self.edgeColor, 
                                       wireframe.nodes[n1][:2], 
                                       wireframe.nodes[n2][:2],
                                       1)
            if self.displayNodes:
                for node in wireframe.nodes:
                    pygame.draw.circle(self.screen, self.nodeColor,
                                       (int(node[0]), int(node[1])),
                                       self.nodeRadius, 0)
    def translateAll(self, vector):        
        for wireframe in self.wireframes.values():
            wireframe.transform(wf.translationMatrix(vector[0], vector[1], vector[2]))
            
    def scaleAll(self, vector):
        for wireframe in self.wireframes.values():
            wireframe.transform(wf.scaleMatrix(vector[0], vector[1], vector[2]))
            
    def rotateAll(self, axis, theta):
        rotateFunction = "rotate" + axis + "Matrix"
        for wireframe in self.wireframes.values():
            wireframe.transform(getattr(wireframe, rotateFunction)(theta))
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    print(event.key)
                    if event.key in key_to_function:
                        key_to_function[event.key](self)
            self.display()
            pygame.display.flip()
            
    def addWireframe(self, name, wireframe):
        self.wireframes[name] = wireframe


"""------ FUNCTIONS ------"""
def cubeNodes(size, coords):
    x0, y0, z0 = coords
    return [(x,y,z) for x in (x0,x0+size) 
            for y in (y0,y0+size) 
            for z in (z0,z0+size)]


cubeEdges = [(n,n+4) for n in range(0,4)]+[(n,n+1) 
for n in range(0,8,2)]+[(n,n+2) 
for n in (0,1,4,5)]

def chunk(depth, height, width, size, coords):
    cubes = []
    x0, y0, z0 = coords
    for d in range(depth):
        for w in range(width):
            for h in range(height):
                cube = wf.Wireframe()
                cubes.append(cube)
                coords = (x0+w*size,y0+h*size,z0+d*size)
                cube.addNodes(np.array(cubeNodes(size,coords)))
                cube.addEdges(cubeEdges)
    return cubes


"""------ PROGRAM ------"""
if __name__ == "__main__":
    
    cubes = chunk(1,10,1,50,(100,100,100))
    
    pv = ProjectionViewer(800, 600)
    i=0
    for cube in cubes:
        pv.addWireframe("cube"+str(i),cube)
        i+=1

    pv.run()
    