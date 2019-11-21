import pygame
import random
import pygame.math
import pygame.time
from biomorph import BioMorph
from biomorph import Node
import biomorph
import pygame_textinput

# in this program three biomorphs are created, two to hold genomes differing by one gene and a third
# to be drawn. this third one has the position of its nodes linearly interpolated (lerped) over time between positions of the corresponding nodes in
# the first two

def draw(b1,b2,drawbm, elapsed, morphtime):
    t = elapsed / morphtime
    for node in drawbm.nodes:
        node.pos = b1.nodes[drawbm.nodes.index(node)].pos.lerp(b2.nodes[drawbm.nodes.index(node)].pos,t)
    
    drawbm.draw(Color_line)
        
def create():
    biomorph1.create(500,250)
    biomorph2.create(500,250)
def randomWalk():
    index = random.randrange(1,6) # gene 0 remains constant
    x = random.randrange(0,1)
    if x==0:
        step = -1
    elif x== 1:
        step = 1
    
    return biomorph1.randomChild(index,step)

textinput = pygame_textinput.TextInput(text_color = (255,255,255), cursor_color = (255,255,255))
biomorph.win = win = pygame.display.set_mode((1000,500))
clock = pygame.time.Clock()
pygame.init()

morphtime = 1500
elapsed = 0
biomorph1 = BioMorph([9, # draw a biomorph - step 1. create a new biomorph object and initialize with genome
                       random.randrange(-9,9),
                       random.randrange(-9,9),
                       random.randrange(-9,9),
                       random.randrange(-9,9),
                       random.randrange(-9,9),
                       random.randrange(-9,9 )])
biomorph2 = randomWalk()
print("B1 Genome: " + str(biomorph1.genome))
print("B2 Genome: " + str(biomorph2.genome))
print()
Color_line = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))

drawnbiomorph = BioMorph((9,0,0,0,0,0,0))
drawnbiomorph.create(500,250)
create()
Color_line = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
run = True
while(run):
    elapsed += clock.get_time()
    if elapsed > morphtime:
        elapsed = 0
        biomorph1 = biomorph2
        biomorph2 = randomWalk()
        Color_line = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
        create()
        print("B1 Genome: " + str(biomorph1.genome))
        print("B2 Genome: " + str(biomorph2.genome))
        print()
        
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DELETE:
                textinput.clear_text()
        if event.type == pygame.QUIT:
            exit()

    win.fill((0, 0, 0))
    draw(biomorph1, biomorph2,drawnbiomorph,elapsed,morphtime)
    pygame.display.update()
    clock.tick(60)


    
