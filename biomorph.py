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
    
    def __init__(self, pos, depth, parent, biomorph):
        self.pos = pos
        self.depth = depth
        self.parent = parent
        self.biomorph = biomorph
    def addNodePair(self, i):#, biomorph):                  
        normalizedvector = (self.pos - self.parent.pos).normalize()  # the direction the branch that this node forms the tip of is pointing - this will be rotated in
                                                                     # the for loop below and will have its length changed, then be used to generate a new position for a new node
                                                                                            
        LorR = 1                 # LorR == left or right. This is used in conjunction with the for loop to rotate in first a positive then negative direction so that the v shape of new branches is symmetrical
        
        for x in range(2):       # create two new nodes and add to the biomorphs list of nodes
            
            k1 = maxanglechange/9       # a constant - my intention is to make it so that i can give a maximum possible angle of a branch  - 180 degrees
            k2 = (maxlengthchange+1)/9  # same thing again for length - but its maxlength +1 because otherwise you can get a vector of zero length which causes errors (and would just draw nothing)
            
            depthfraction = i/self.biomorph.genome[0]                  # the current depth over the maximum depth that will be reached
            
            distancefraction = self.pos.distance_to(self.parent.pos)/(2*maxlengthchange + defaultlength)  # the length of the previous  branch over the maximum possible lenght a branch can be -
                                                                                                          # confusingly this is default length + 2*maxlength change because two genes add to the default length each capable
                                                                                                          # adding a maximum of maxlengthchange to the default length

            # the two equations below dictate how the trees genes alter the default shape 
            # rotationamount = default angle + (gene 1 * k1) + (gene 3 * depth fraction * k1) + (gene 3 * distance fraction * k1)            
            rotationamount = defaultanglemag+self.biomorph.genome[1]*k1 + self.biomorph.genome[2]*depthfraction*k1 + self.biomorph.genome[3]*distancefraction*k1
            # magnitude = default length + (gene 4 * k2) + (gene 5 * depth fraction * k2) + (gene 6 * length fraction * k2)
            magnitude = defaultlength + self.biomorph.genome[4]*k2 + self.biomorph.genome[5]*depthfraction*k2 + self.biomorph.genome[6]*distancefraction*k2
            
            rotatedvector = normalizedvector.rotate(rotationamount*LorR) # calculated rotation and magnitude are applied to the direction vector
            finalvector = rotatedvector* magnitude                       #
            
            newpos = self.pos + finalvector     # and the final vector is added onto this nodes position to generate the a new branches position
            
            newnode = Node(newpos, i, self, self.biomorph)     # the node is actually created 
            self.biomorph.nodes.append(newnode)      # and added to the biomorphs list of nodes
            LorR *= -1            # LorR changes so that the next branch will be rotated in the opposit direction
            #print("x= " + str(newnode.pos.x))
            #print("y= " + str(newnode.pos.y))
        #print()
            
    def addSamePosNodePair(self,i):
        for x in range(2):
            newnode = Node(self.pos,i,self, self.biomorph)
            self.biomorph.nodes.append(newnode)
            #print("samepos")
            #print("x= " + str(newnode.pos.x))
            #print("y= " + str(newnode.pos.y))
        #print()

    def findAncestorIn(self, b2):
        ancestor = self
        ancestor = ancestor.parent
        if self.biomorph.nodes.index(ancestor) < len(b2.nodes):
            #print()
            #print(len(b2.nodes))
            #print(self.biomorph.nodes.index(ancestor))
            
            return ancestor
        else:
            self.findAncestorIn(b2)
            
class BioMorph(object):    
    def __init__(self, genome):
        self.genome = genome
        self.nodes = []
        
    def create(self, x, y): # populates list of nodes by repeatedly calling node.addNodePair. pass x and y to specify where you want to draw it
        print()
        print("-------create-------")
        print()

        self.nodes = []
        base = Node(pygame.math.Vector2(x,y),0,None, self) 
        startnode = Node(pygame.math.Vector2(x,y+self.genome[4]*((maxlengthchange)/9)+1), -1, base, self) # first create the nodes that form the first line - the trees trunk - ie base and startnode. use genome[4] to chage the
                                                                                                   # length of the trunk - 4 is arbitrary, and a concequence of the order that the addNodePair function is written
                                                                                                   # genome[4] also determines the length of the branches grown using the same formula - see addNodePair
        self.nodes.append(startnode)
        for i in range(abs(self.genome[0])):  # genome[0] determines number the number of times a new pair of branches is added to the outer nodes - ie the final "depth" of the biomorphs branching
            print("-------depth"+str(i)+"-------")
            for node in self.nodes:              
                if node.depth == i-1:             # only make the outer nodes grow branches
                    node.addNodePair(i)    # grow branches, passing a reference to self and i - the current "depth"
        
    def cutOffCreate(self,x,y, extra):
        print()
        print("-------cutoffCreate-------")
        print()
        self.nodes = []
        base = Node(pygame.math.Vector2(x,y),0,None, self) 
        startnode = Node(pygame.math.Vector2(x,y+self.genome[4]*((maxlengthchange)/9)+1), -1, base, self) 
        self.nodes.append(startnode)
        finald = abs(self.genome[0])+extra
        print("final d= " + str(finald))
        print("self.genome[0]= " +str(self.genome[0]))
        for i in range((finald)):
            
            if i > self.genome[0]-1:
                print("-------extra depth"+str(i)+"-------")
                for node in self.nodes:              
                    if node.depth == i-1:             
                        node.addSamePosNodePair(i) 
            else:
                print("-------depth"+str(i)+"-------")
                for node in self.nodes:              
                    if node.depth == i-1:             
                        node.addNodePair(i)
        
    
    def randomChild(self,index,step): # step and index  passed must be between -9 and +9
        possiblestep = self.genome[index] + step
        returnbm = BioMorph(self.genome)
        
        if possiblestep  > 9 or possiblestep < -9:
            returnbm.genome[index] -= step
            
        else:
            returnbm.genome[index] += step
        return returnbm
    def moveTo(self,x,y):
        
        destination = pygame.math.Vector2(x,y)
        movementvec = destination - self.nodes[0].pos
        for node in self.nodes:
            node.pos += movementvec
            
    def prepareAnimationMorphs(self,g1,g2, x1,y1,x2,y2):
        #self.genome[0] = b1.genome[0]
        print()
        print("-------prepareAnimationMorphs-------")
        print("g1: " + str(g1) + " g2: " +str(g2))
        print()
        def helper(greater, lesser):
            returnlist = []
            b1 = BioMorph(greater)
            b1.create(x1,y1)
            returnlist.append(b1)
            
            #lesser[0] = greater[0]
            b2 = BioMorph(lesser)
            extra = abs(greater[0]) - abs(lesser[0])
            
            b2.cutOffCreate(x2,y2,extra)
            returnlist.append(b2)
            b2.genome[0] = greater[0]
            self.genome[0] = greater[0]
            return returnlist
            
        returnlist = []
        if abs(g1[0]) != abs(g2[0]):
            if  abs(g1[0]) > abs(g2[1]):
                morphs = helper(g1,g2)
                returnlist.append(morphs[0])
                returnlist.append(morphs[1])
            else:
                morphs = helper(g2,g1)
                returnlist.append(morphs[1])
                returnlist.append(morphs[0])
                                                 
        else:
            
            self.genome[0] = g1[0]
            b1 = BioMorph(g1)
            b2 = BioMorph(g2)
            b1.create(x1,y1)
            b2.create(x2,y2)
            returnlist.append(b1)
            returnlist.append(b2)            
        self.create(x1,y1)
        
        print("b1 nodes: "+ str(len(returnlist[0].nodes)) + " b2 nodes: " + str(len(returnlist[1].nodes)) + " drawn nodes: " +str(len(self.nodes)))
        print()
        return returnlist

    def lerpBetween(self,b1,b2,t):
        #print("b1 nodes: "+ str(len(b1.nodes)) + " b2 nodes: " + str(len(b2.nodes)) + " drawn nodes: " +str(len(self.nodes)))
        for node in self.nodes:
            node.pos = b1.nodes[self.nodes.index(node)].pos.lerp(b2.nodes[self.nodes.index(node)].pos,t)
            
    
    def draw(self, Color_line):         # connect each node with its parent with a line and then call display.flip() to update the screen and draw the biomorph
        for node in self.nodes:
            if node.parent != None:
                pygame.draw.line(win, Color_line, node.pos, node.parent.pos)

        pygame.display.flip()
                
    
