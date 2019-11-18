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
    def addNodePair(self, i, biomorph):                  
        normalizedvector = (self.pos - self.parent.pos).normalize()  # the direction the branch that this node forms the tip of is pointing - this will be rotated in
                                                                     # the for loop below and will have its length changed, then be used to generate a new position for a new node
                                                                                            
        LorR = 1                 # LorR == left or right. This is used in conjunction with the for loop to rotate in first a positive then negative direction so that the v shape of new branches is symmetrical
        
        for x in range(2):       # create two new nodes and add to the biomorphs list of nodes
            
            k1 = maxanglechange/9       # a constant - my intention is to make it so that i can give a maximum possible angle of a branch  - 180 degrees
            k2 = (maxlengthchange+1)/9  # same thing again for length - but its maxlength +1 because otherwise you can get a vector of zero length which causes errors (and would just draw nothing)
            
            depthfraction = i/biomorph.genome[0]                  # the current depth over the maximum depth that will be reached
            
            distancefraction = self.pos.distance_to(self.parent.pos)/(2*maxlengthchange + defaultlength)  # the length of the previous previous branch over the maximum possible lenght a branch can be -
                                                                                                          # confusingly this is default length + 2*maxlength change because two genes add to the default length each capable
                                                                                                          # adding a maximum of maxlengthchange to the default length

            # the two equations below dictate how the trees genes alter the default shape 
            # rotationamount = default angle + (gene 1 * k1) + (gene 3 * depth fraction * k1) + (gene 3 * distance fraction * k1)            
            rotationamount = defaultanglemag+biomorph.genome[1]*k1 + biomorph.genome[2]*depthfraction*k1 + biomorph.genome[3]*distancefraction*k1
            # magnitude = default length + (gene 4 * k2) + (gene 5 * depth fraction * k2) + (gene 6 * length fraction * k2)
            magnitude = defaultlength + biomorph.genome[4]*k2 + biomorph.genome[5]*depthfraction*k2 + biomorph.genome[6]*distancefraction*k2
            
            rotatedvector = normalizedvector.rotate(rotationamount*LorR) # calculated rotation and magnitude are applied to the direction vector
            finalvector = rotatedvector* magnitude                       #
            
            newpos = self.pos + finalvector     # and the final vector is added onto this nodes position to generate the a new branches position
            
            newnode = Node(newpos, i, self)     # the node is actually created 
            biomorph.nodes.append(newnode)      # and added to the biomorphs list of nodes
            LorR *= -1            # LorR changes so that the next branch will be rotated in the opposit direction
        
class BioMorph(object):    
    def __init__(self, genome):
        self.genome = genome
        self.nodes = []
        
    def create(self, x, y): # populates list of nodes by repeatedly calling node.addNodePair. pass x and y to specify where you want to draw it
        base = Node(pygame.math.Vector2(x,y),0,None) 
        startnode = Node(pygame.math.Vector2(x,y+self.genome[4]*((maxlengthchange)/9)+1), 0, base) # first create the nodes that form the first line - the trees trunk - ie base and startnode. use genome[4] to chage the
                                                                                                   # length of the trunk - 4 is arbitrary, and a concequence of the order that the addNodePair function is written
                                                                                                   # genome[4] also determines the length of the branches grown using the same formula - see addNodePair
        self.nodes.append(startnode)
        for i in range(1, abs(self.genome[0])):  # genome[0] determines number the number of times a new pair of branches is added to the outer nodes - ie the final "depth" of the biomorphs branching
            for node in self.nodes:              
                if node.depth == i-1             # only make the outer nodes grow branches
                    node.addNodePair(i, self)    # grow branches, passing a reference to self and i - the current "depth"
                

    def draw(self, Color_line):         # connect each node with its parent with a line and then call display.flip() to update the screen and draw the biomorph
        for node in self.nodes:
            if node.parent != None:
                pygame.draw.line(win, Color_line, node.pos, node.parent.pos)

        pygame.display.flip()
                
    
