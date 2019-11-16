import pygame
import random
import pygame.math
win = pygame.display.set_mode((1000,500))
pygame.init()

class Node(object):
    
    def __init__(self, pos, depth, parent):
        self.set_pos(pos)
        self.depth = depth
        self.parent = parent
    def set_pos(self,pos):
        self._pos = pos
    def get_pos(self):
        return self._pos
    
def addNodePair(i, node, length, anglemagnitude):
    LorR = 1
    for x in range(2):
        vector = node.get_pos() - node.parent.get_pos()
        normalizedvector = vector.normalize()
        rotatedvector = normalizedvector.rotate(anglemagnitude*LorR)
        newpos = node.get_pos() + rotatedvector*length
        newnode = Node(newpos, i, node)
        pygame.draw.line(win, Color_line, (node.get_pos()), (newnode.get_pos()))
        LorR *= -1
        pygame.display.flip()
        nodes.append(newnode)

for x in range(15):
    nodes = []
    Color_line = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
    anglemagnitude = random.randrange(10,120)
    length = random.randrange(2,30)
    x= 500 + random.randrange(-500, 500)
    y= 500
    base = Node(pygame.math.Vector2(x,y),0,None)
    startnode = Node(pygame.math.Vector2(x,y-20), 0, base)
    pygame.draw.line(win,Color_line, base.get_pos(), startnode.get_pos())
    pygame.display.flip()
    nodes.append(startnode)
    for i in range(1,6):
        for node in nodes:
            if node.depth == i-1:
                addNodePair(i, node, length,anglemagnitude)
            
    