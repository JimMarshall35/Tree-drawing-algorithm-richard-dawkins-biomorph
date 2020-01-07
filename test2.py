from __future__ import print_function
import librosa

import pygame
import random
import pygame.math
import pygame.time
from biomorph import BioMorph
from biomorph import Node
import biomorph

biomorph.win = win = pygame.display.set_mode((1000,500))
clock = pygame.time.Clock()
pygame.init()


gene1 = [3, 
        random.randrange(-9,9),
        random.randrange(-9,9),
        random.randrange(-9,9),
        random.randrange(-9,9),
        random.randrange(-9,9),
        random.randrange(-9,9)]
gene2 = [2, 
        gene1[1],
        gene1[2],
        gene1[3],
        gene1[4],
        gene1[5],
        gene1[6]]
drawnbiomorph = BioMorph([0,0,0,0,0,0,0])

#print(gene1, gene2)
snapshots = drawnbiomorph.prepareAnimationMorphs(gene1,gene2,250,250,750,250)
win.fill((0,0,0))
snapshots[0].draw((255,0,0))
snapshots[1].draw((0,255,0))
