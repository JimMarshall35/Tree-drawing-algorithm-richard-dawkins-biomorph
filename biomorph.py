import pygame
import random
import pygame.math
import pygame.time
defaultanglemag = 30
defaultlength = 20
defaultdepth = 10
maxlengthchange = 28
maxanglechange = 180
class Node(object):
    
    def __init__(self, pos, depth, parent):
        self.pos = pos
        self.depth = depth
        self.parent = parent        
    def addNodePair(self, i, biomorph, Color_line):
        LorR = 1 
        normalizedvector = (self.pos - self.parent.pos).normalize()
        for x in range(2):
            k1 = maxanglechange/9
            k2 = (maxlengthchange+1)/9
            fraction = i/biomorph.genome[0]
            
            rotationamount = defaultanglemag+biomorph.genome[1]*k1 + biomorph.genome[2]*fraction*k1
            magnitude = defaultlength + biomorph.genome[3]*k2 + biomorph.genome[4]*fraction*k2
            
            rotatedvector = normalizedvector.rotate(rotationamount*LorR)
            newpos = self.pos + rotatedvector* magnitude
            
            newnode = Node(newpos, i, self)
            biomorph.nodes.append(newnode)
            LorR *= -1            
        
class BioMorph(object):    
    def __init__(self, genome):
        self.genome = genome
        self.nodes = []
        
    def create(self, x, y, Color_line): 
        self.Color_line = Color_line
        base = Node(pygame.math.Vector2(x,y),0,None)
        startnode = Node(pygame.math.Vector2(x,y+self.genome[3]*((maxlengthchange)/9)+1), 0, base)
        self.nodes.append(startnode)
        for i in range(1, abs(self.genome[0])):  
            for node in self.nodes:
                if node.depth == i-1:
                    node.addNodePair(i, self, Color_line)
                

    def draw(self):
        for node in self.nodes:
            if node.parent != None:
                pygame.draw.line(win, self.Color_line, node.pos, node.parent.pos)

        pygame.display.flip()
                
    
