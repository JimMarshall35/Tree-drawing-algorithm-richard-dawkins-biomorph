# (-9, -6, 8, -2, 4) - butterfly
import pygame
import random
import pygame.math
import pygame.time
from biomorph import BioMorph
from biomorph import Node
import biomorph
import ast
import pygame_textinput
textinput = pygame_textinput.TextInput(text_color = (255,255,255), cursor_color = (255,255,255))
biomorph.win = win = pygame.display.set_mode((1000,500))
clock = pygame.time.Clock()
pygame.init()

treenumber = 5
mybiomorph = None
Color_line = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
run = True  
while(run):
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DELETE:
                textinput.clear_text()
        if event.type == pygame.QUIT:
            exit()

    win.fill((0, 0, 0))
    win.blit(textinput.get_surface(), (10, 10))
    
    if textinput.update(events):
        
        genomeinput = True
        while(genomeinput):
            if(textinput.get_text()[0]== "r"):
                mybiomorph = BioMorph((random.randrange(-9,9), # draw a biomorph - step 1. create a new biomorph object and initialize with genome
                                       random.randrange(-9,9),
                                       random.randrange(-9,9),
                                       random.randrange(-9,9),
                                       random.randrange(-9,9),
                                       random.randrange(-9,9),
                                       random.randrange(-9,9)))
                mybiomorph.create(500,250)          # draw a biomorph - step 2. call create, specifying screen position and colour to grow the tree and populate mybiomorph.nodes
                print(mybiomorph.genome)
                print(len(mybiomorph.nodes))
                textinput.input_string = str(mybiomorph.genome)
                textinput.cursor_position = 0
                Color_line = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)) 
                break

            
            else:
                try:
                    genome = ast.literal_eval(textinput.get_text())
                    genome = tuple(genome)
                except:
                    print("enter a valid tuple or list")
                    break
                if len(genome) != 7:
                    print("length must equal 5")
                    break
                else:
                    okay = True
                    intconvertedgenome = []
                    for gene in genome:
                        try:
                            gene = int(gene)
                            intconvertedgenome.append(gene)
                        except:
                            print("all elements must be ints")
                            okay = False
                            break
                        if gene >=10 or gene <= -10:
                            print("all elements must be between -9 and +9")
                            okay = False
                            break
                    if okay == True:
                        #textinput.clear_text()
                        intconvertedgenome = tuple(intconvertedgenome)
                        print("successful input")
                        print(intconvertedgenome)
                        Color_line = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)) 
                    else:
                        break
            mybiomorph = BioMorph(intconvertedgenome)
            mybiomorph.create(500,250)
            break


    if mybiomorph != None:
        mybiomorph.draw(Color_line) # draw a biomorph - step 3. call create, specifying screen position and colour - this connects the nodes with lines, actually drawing it

    pygame.display.update()
    clock.tick(30)






        

