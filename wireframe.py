# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 17:27:35 2019

@author: Freenox
"""
import numpy as np

def translationMatrix(dx=0, dy=0, dz=0):
    return np.array([[1,0,0,0],
                     [0,1,0,0],
                     [0,0,1,0],
                     [dx,dy,dz,1]])

def scaleMatrix(sx=0, sy=0, sz=0):
    return np.array([[sx,0,0,0],
                     [0,sy,0,0],
                     [0,0,sz,0],
                     [0,0,0,1]])


class Wireframe:
    def __init__(self):
        self.nodes = np.zeros((0,4))
        self.edges = []
        self.faces = []
    
    def addNodes(self, node_array):
        ones_col = np.ones((len(node_array),1))
        ones_add = np.hstack((node_array, ones_col))
        self.nodes = np.vstack((self.nodes, ones_add))
    
    def addEdges(self, edgeList):
        """Create edge between given nodes indices"""
        self.edges += edgeList
    
    def addFaces(self, faceList):
        self.faces += faceList
        
    def outputNodes(self):
        print("\n ---Nodes---")
        for i, (x,y,z,_) in enumerate(self.nodes):
            print("%d: (%.2f,%.2f,%.2f)" % (i, x, y, z))
    
    def outputEdges(self):
        print("\n --- Edges --- ")
        for i, (node1, node2) in enumerate(self.edges):
            print(" %d: %d -> %d" % (i, node1, node2))

    def outputFaces(self):
        print("\n--- Faces ---")
        for i, (a,b,c,d) in enumerate(self.faces):
            print(" %d: (%d, %d, %d, %d)" % (i, a,b,c,d))

    def transform(self, matrix):
        self.nodes = np.dot(self.nodes, matrix)        
    
    
    def findCentre(self):
        num_nodes = len(self.nodes)
        
        meanX = sum([node.x for node in self.nodes])/num_nodes
        meanY = sum([node.y for node in self.nodes])/num_nodes
        meanZ = sum([node.z for node in self.nodes])/num_nodes

        return (meanX, meanY, meanZ)
    
    def rotateXMatrix(self, radians):
        c = np.cos(radians)
        s = np.sin(radians)
        
        return np.array([[1,0,0,0],
                         [0,c,-s,0],
                         [0,s,c,0],
                         [0,0,0,1]])

    def rotateYMatrix(self, radians):
        c = np.cos(radians)
        s = np.sin(radians)
        
        return np.array([[c,0,s,0],
                         [0,1,0,0],
                         [-s,0,c,0],
                         [0,0,0,1]])
    
    def rotateZMatrix(self, radians):
        c = np.cos(radians)
        s = np.sin(radians)
        
        return np.array([[c,-s,0,0],
                         [s,c,0,0],
                         [0,0,1,0],
                         [0,0,0,1]])
    
    
if __name__ == "__main__":
    cube_nodes = [(x,y,z) for x in (0,1) for y in (0,1) for z in (0,1)]

    cube = Wireframe()
    cube.addNodes(np.array(cube_nodes))
    cube.addEdges([(n, n+4) for n in range(0,4)])
    cube.addEdges([(n, n+1) for n in range(0,8,2)])
    cube.addEdges([(n, n+2) for n in (0,1,4,5)])
    cube.addFaces([(0,1,2,3),(1,5,3,7),(4,5,6,7),(0,4,2,6),(0,4,5,1),(3,2,6,7)])
    
    
    cube.outputNodes()
    cube.outputEdges()
    cube.outputFaces()
    
    for face in cube.faces:
        points = [cube.nodes[i][:3] for i in face]
        
    #my_wireframe = Wireframe()
    #my_wireframe.addNodes([(0,0,0), (1,2,3),(3,2,1)])
    #my_wireframe.addEdges([(1,2)])
    #
    #my_wireframe.outputEdges()
    #my_wireframe.outputNodes()