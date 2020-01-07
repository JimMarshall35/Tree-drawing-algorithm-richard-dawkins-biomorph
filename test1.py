from __future__ import print_function
import librosa

import pygame
import random
import pygame.math
import pygame.time
from biomorph import BioMorph
from biomorph import Node
import biomorph
#1.787936507936508
# in this program three biomorphs are created, two to hold genomes differing by one gene and a third
# to be drawn. this third one has the position of its nodes linearly interpolated (lerped) over time between positions of the corresponding nodes in
# the first two



    
def hilo(a, b, c):
    if c < b: b, c = c, b
    if b < a: a, b = b, a
    if c < b: b, c = c, b
    return a + c

def complement(r, g, b):
    k = hilo(r, g, b)
    return tuple(k - u for u in (r, g, b))
        
def create():
    biomorph1.create(500,250)
    biomorph2.create(500,250)

def randomWalk(start, end, morph):
    index = random.randrange(start,end) # gene 0 remains constant
    x = random.randrange(0,1)
    if x==0:
        step = -1
    elif x== 1:
        step = 1
    
    return morph.randomChild(index,step)

def colourLerp(c1,c2,t):
    v1 = pygame.math.Vector3(c1[0],c1[1],c1[2])
    v2 = pygame.math.Vector3(c2[0],c2[1],c2[2])
    lv = v1.lerp(v2,t)
    return (int(lv.x), int(lv.y), int(lv.z))
    
def transformBiomorph(biomorph1):
    morph2 = BioMorph([random.randrange(-9,9), 
                       random.randrange(-9,9),
                       random.randrange(-9,9),
                       random.randrange(-9,9),
                       random.randrange(-9,9),
                       biomorph1.genome[5],
                       biomorph1.genome[6]])
    return randomWalk(5,6, morph2)

# 1. Get the file path to the included audio example
#filename = "music\Pillock.wav"
# 2. Load the audio as a waveform `y`
#    Store the sampling rate as `sr`
#y, sr = librosa.load(filename)

# 3. Run the default beat tracker
#tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

#print('Estimated tempo: {:.2f} beats per minute'.format(tempo))

# 4. Convert the frame indices of beat events into timestamps
#beat_times = librosa.frames_to_time(beat_frames, sr=sr)

#print(beat_times)        
biomorph.win = win = pygame.display.set_mode((1000,500))
clock = pygame.time.Clock()
pygame.init()

morphtime = 1000#beat_times[0]*1000

elapsed = 0
depth = 8
##gene1 = [random.randrange(-9,9), 
##        random.randrange(-9,9),
##        random.randrange(-9,9),
##        random.randrange(-9,9),
##        random.randrange(-9,9),
##        random.randrange(-9,9),
##        random.randrange(-9,9)]
##gene2 = [random.randrange(-9,9),
##        random.randrange(-9,9),
##        random.randrange(-9,9),
##        random.randrange(-9,9),
##        random.randrange(-9,9),
##        random.randrange(-9,9),
##        random.randrange(-9,9)]
gene1 = [2, 
        random.randrange(-9,9),
        random.randrange(-9,9),
        random.randrange(-9,9),
        random.randrange(-9,9),
        random.randrange(-9,9),
        random.randrange(-9,9)]
gene2 = [4, 
        random.randrange(-9,9),
        random.randrange(-9,9),
        random.randrange(-9,9),
        random.randrange(-9,9),
        random.randrange(-9,9),
        random.randrange(-9,9)]
drawnbiomorph = BioMorph([0,0,0,0,0,0,0])

#print(gene1, gene2)
snapshots = drawnbiomorph.prepareAnimationMorphs(gene1,gene2,500,250,500,250)

Colour1 = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
Colour2 = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))

#create()
Color_line = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))

#run = True
#beatindex = 0
#pygame.mixer.music.load(filename)
#pygame.mixer.music.play()
run = True
while(run):
    t = elapsed/morphtime
    morphRGB = colourLerp(Colour1, Colour2,t)
    backgroundRGB = complement(morphRGB[0], morphRGB[1], morphRGB[2])
    win.fill(backgroundRGB)
    #draw(biomorph1, biomorph2,drawnbiomorph,elapsed,morphtime)
    
    drawnbiomorph.lerpBetween(snapshots[0],snapshots[1],t)
    drawnbiomorph.draw(morphRGB)
    elapsed += clock.get_time()
    if elapsed > morphtime:
        #morphtime = 1000*(beat_times[beatindex+1]-beat_times[beatindex])
        #beatindex +=1
        elapsed = 0
        #biomorph1 = biomorph2
        #biomorph2 = transformBiomorph(biomorph1)
        gene1 = gene2
        gene2 = [random.randrange(-9,9),
                random.randrange(-9,9),
                random.randrange(-9,9),
                random.randrange(-9,9),
                random.randrange(-9,9),
                random.randrange(-9,9),
                random.randrange(-9,9)]
        snapshots = drawnbiomorph.prepareAnimationMorphs(gene1,gene2,500,250,500,250)
        Color_line = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
        Colour1 = Colour2
        Colour2 = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
        #create()
        
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DELETE:
                textinput.clear_text()
        if event.type == pygame.QUIT:
            exit()

    pygame.display.update()
    clock.tick(100)


    
