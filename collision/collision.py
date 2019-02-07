# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 10:26:32 2019

@author: Freenox
"""

import tkinter as tk
from math import sqrt
import numpy as np

wd = tk.Tk()
canvas = tk.Canvas(wd, width = 400., height = 300.)

canvas.pack()

def distance(obj1, obj2):
    L1=canvas.coords(obj1.part)
    L2=canvas.coords(obj2.part)
    
    x = (L1[2]+L1[0])/2 - (L2[2]+L2[0])/2
    y = (L1[3]+L1[1])/2 - (L2[3]+L2[1])/2
    
    return sqrt(x**2 + y**2)-obj1.r-obj2.r

def collisionAngle(obj1, obj2):
    """Return angle of collision in rad"""
    vec1 = obj1.vec
    vec2 = obj2.vec
    n1 = np.linalg.norm(vec1)
    n2 = np.linalg.norm(vec2)
    return abs(np.cross(vec1,vec2)/(n1*n2))

def collision(obj1, obj2):
    vec1 = obj1.vec
    vec2 = obj2.vec
    vec = vec1
    if distance(obj1, obj2) <=0:
        obj1.vec=-vec1
        obj2.vec=-vec2
        
    
    
class Particle:
    def __init__(self, canvas, x, y, r, col,dx,dy,dt):
        self.x = x
        self.y = y
        self.r = r
        self.vec = np.array([dx,dy])
        self.dt = dt
        self.canvas = canvas
        self.color = col
        self.part = canvas.create_oval(self.x-r,self.y-r,self.x+r,self.y+r,fill=self.color)
        
    def move(self):
        self.dx = self.vec[0]
        self.dy = self.vec[1]
        self.canvas.move(self.part, self.dx, self.dy)
        self.canvas.after(self.dt)
        self.collisionB()
        self.canvas.update()
    
    def collisionB(self):
        L = self.canvas.coords(self.part)
        xL= float(self.canvas.cget("width"))
        yL= float(self.canvas.cget("height"))
        if L[1]>=yL or L[3]>=yL or L[1]<=0 or L[3]<=0:
            self.vec = self.vec*[1,-1]
            
        if L[0]>=xL or L[2]>=xL or L[0]<=0 or L[2]<=0:
            self.vec = self.vec*[-1,1]
    


ball1 = Particle(canvas, 100, 100, 50,'blue', 0.5, -0.8, 1)
ball2 = Particle(canvas, 200, 100, 50,'red', -0.6,0.7, 1)
print(distance(ball1,ball2))
print(canvas.coords(ball1.part))
print(canvas.coords(ball2.part))

for i in range(2000):
    collision(ball1, ball2)
    ball1.move()
    ball2.move()
    print(distance(ball1,ball2))
#    print(ball1.vec)
#    print(ball2.vec)
wd.mainloop()
