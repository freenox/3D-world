# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 17:45:41 2019

@author: Freenox
"""
from IPython import get_ipython

get_ipython().magic('reset -f')

import wireframe as wf
import pygame, sys, time
import numpy as np

"""--- FIXED VALUES ---"""
SPEED = 2
ROTATION = 0.1
SCALE = 0.05

"""--------------------"""
key_to_function = {
    97 :(lambda x: x.translateAll([-SPEED, 0, 0])),
    100:(lambda x: x.translateAll([ SPEED, 0, 0])),
    115:(lambda x: x.translateAll([0,  SPEED, 0])),
    119:(lambda x: x.translateAll([0, -SPEED, 0])),
    270:(lambda x: x.scaleAll([1+SCALE, 1+SCALE, 1+SCALE])),
    269:(lambda x: x.scaleAll([1-SCALE,1-SCALE,1-SCALE])),
    273:(lambda x: x.rotateAll('X',  0.1)),
    274:(lambda x: x.rotateAll('X', -0.1)),
    275:(lambda x: x.rotateAll('Y',  0.1)),
    276:(lambda x: x.rotateAll('Y', -0.1)),
    101:(lambda x: x.rotateAll('Z',  0.1)),
    113:(lambda x: x.rotateAll('Z', -0.1))
}


colors = [(255,255,255), (255,0,0), (0,255,0),(0,0,255),(255,255,0),(0,255,255)]

def itemgetter(liste):
    return liste[1]


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
        self.displayEdges = False
        self.displayFaces = True
        self.nodeColor = (255,255,255)
        self.edgeColor = (200,200,200)
        self.nodeRadius = 1
        
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
            
            #calculate average depth per face
            avg_z=[]
            for i, face in enumerate(wireframe.faces):
                avg_z.append([i,(wireframe.nodes[face[0]][2] + 
                              wireframe.nodes[face[1]][2] +
                              wireframe.nodes[face[2]][2] +
                              wireframe.nodes[face[3]][2]/4.0)])
           
            sort_face = [face[0] for face in sorted(avg_z, key=itemgetter,reverse=True)]
            #display faces from furthest to closest
            if self.displayFaces:
                for i, fs in enumerate(sort_face):
                    face = wireframe.faces[fs]
                    pygame.draw.polygon(self.screen, colors[fs],
                                        [wireframe.nodes[it][:2] for it in face])
                
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
            pressed = pygame.key.get_pressed()
            for key in key_to_function:
                if pressed[key]:
                    key_to_function[key](self)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                        
                    
#                (x,y) = pygame.mouse.get_rel()
#                self.rotateAll('X', x*SENSITIVITY)
#                self.rotateAll('Y', y*SENSITIVITY)
#                self.rotateAll('Z', (x-y)*SENSITIVITY)
                
            self.display()
            pygame.display.flip()
#            time.sleep(0.1)
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

cubeFaces = [(0,1,3,2),
             (1,3,7,5),
             (4,5,7,6),
             (0,4,6,2),
             (0,4,5,1),
             (3,2,6,7)]

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
                cube.addFaces(cubeFaces)

    return cubes


"""------ PROGRAM ------"""
if __name__ == "__main__":
    
    cubes = chunk(1,1,1,250,(300,300,300))
    pv = ProjectionViewer(1200, 800)
    i=0
    for cube in cubes:
        pv.addWireframe("cube"+str(i),cube)
        i+=1

    pv.run()