import pygame
import random
import pygame.math
import pygame.time
win = pygame.display.set_mode((1000,500))
pygame.init()
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
    def addNodePair(self, i, biomorph):
        # this term is -1 the second iteration of the for loop - so that the two branches have reflectional symmetry in y axis
        LorR = 1 
        # get normalized vector from this node to its parent.
        # this will be used to generate child node positions by rotating it, changing its magnitude and then adding to the nodes position.
        normalizedvector = (self.pos - self.parent.pos).normalize()
        #generate two child nodes and draw line from this node to each one - rotating by equal amount in first positive then negative direction
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
            pygame.draw.line(win, Color_line, (self.pos), (newnode.pos))
            LorR *= -1
            
        pygame.display.flip() # update screen to show drawn lines   
class BioMorph(object):    
    def __init__(self, genome):
        self.genome = genome
        self.nodes = []
    def draw(self, x, y): # draws the biomorph at the x and y coordinates passed
        base = Node(pygame.math.Vector2(x,y),0,None)
        startnode = Node(pygame.math.Vector2(x,y+biomorph.genome[3]*((maxlengthchange)/9)+1), 0, base)
        pygame.draw.line(win,Color_line, base.pos, startnode.pos)
        pygame.display.flip()
        self.nodes.append(startnode)
        for i in range(1, abs(self.genome[0])):  
            for node in self.nodes:
                if node.depth == i-1:
                    node.addNodePair(i, self)
    
treenumber = 5
run = True  # placeholder main loop - generate 15 biomorphs in a row over and over again
while(run):
    for x in range(treenumber): # draws 15 trees
        #nodes = []
        biomorph = BioMorph((
                             random.randrange(-9,9),
                             random.randrange(-9,9),
                             random.randrange(-9,9),
                             random.randrange(-9,9),
                             random.randrange(-9,9)
                            ))
        print(biomorph.genome)
        Color_line = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)) 

        x= x*(1000/treenumber) + 0.5*(1000/treenumber)
        y= 300
        biomorph.draw(x,y)
    pygame.time.wait(1000)
    win.fill((0,0,0))
    
