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
from aubio import source, tempo
from numpy import median, diff

def get_file_bpm(path, params=None):
    """ Calculate the beats per minute (bpm) of a given file.
        path: path to the file
        param: dictionary of parameters
    """
    if params is None:
        params = {}
    # default:
    samplerate, win_s, hop_s = 44100, 1024, 512
    if 'mode' in params:
        if params.mode in ['super-fast']:
            # super fast
            samplerate, win_s, hop_s = 4000, 128, 64
        elif params.mode in ['fast']:
            # fast
            samplerate, win_s, hop_s = 8000, 512, 128
        elif params.mode in ['default']:
            pass
        else:
            raise ValueError("unknown mode {:s}".format(params.mode))
    # manual settings
    if 'samplerate' in params:
        samplerate = params.samplerate
    if 'win_s' in params:
        win_s = params.win_s
    if 'hop_s' in params:
        hop_s = params.hop_s

    s = source(path, samplerate, hop_s)
    samplerate = s.samplerate
    o = tempo("specdiff", win_s, hop_s, samplerate)
    # List of beats, in samples
    beats = []
    # Total number of frames read
    total_frames = 0
    onlyonce = True
    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat and onlyonce:
            firstbeatlocation = total_frames*(1/samplerate) #first beat location in seconds
            print(firstbeatlocation)
            onlyonce = False
        if is_beat:
            this_beat = o.get_last_s()
            beats.append(this_beat)
            #if o.get_confidence() > .2 and len(beats) > 2.:
            #    break
        total_frames += read
        if read < hop_s:
            break

    def beats_to_bpm(beats, path):
        # if enough beats are found, convert to periods then to bpm
        if len(beats) > 1:
            if len(beats) < 4:
                print("few beats found in {:s}".format(path))
            bpms = 60./diff(beats)
            return median(bpms)
        else:
            print("not enough beats found in {:s}".format(path))
            return 0

    return {"bpm":beats_to_bpm(beats, path), "first":firstbeatlocation}

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode',
            help="mode [default|fast|super-fast]",
            dest="mode", default='default')
    parser.add_argument('sources',
            nargs='+',
            help="input_files")
    args = parser.parse_args()
    for f in args.sources:
        path = f
        info = get_file_bpm(f, params = args)
    print("bpm: "+str(info["bpm"]), "first beat: " + str(info["first"]))
    
def draw(b1,b2,drawbm, elapsed, morphtime):
    t = elapsed / morphtime
    for node in drawbm.nodes:
        node.pos = b1.nodes[drawbm.nodes.index(node)].pos.lerp(b2.nodes[drawbm.nodes.index(node)].pos,t)
    
    drawbm.draw(Color_line)
        
def create():
    biomorph1.create(500,250)
    biomorph2.create(500,250)

textinput = pygame_textinput.TextInput(text_color = (255,255,255), cursor_color = (255,255,255))
biomorph.win = win = pygame.display.set_mode((1000,500))
clock = pygame.time.Clock()
pygame.init()

morphtime = ((60/info["bpm"])*1000)*2#1500
print("morphtime: " + str(morphtime))
elapsed = 0
depth = 8
biomorph1 = BioMorph([depth, # draw a biomorph - step 1. create a new biomorph object and initialize with genome
                       random.randrange(-9,9),
                       random.randrange(-9,9),
                       random.randrange(-9,9),
                       random.randrange(-9,9),
                       random.randrange(-9,9),
                       random.randrange(-9,9)])
biomorph2 = BioMorph([depth, # draw a biomorph - step 1. create a new biomorph object and initialize with genome
                       random.randrange(-9,9),
                       random.randrange(-9,9),
                       random.randrange(-9,9),
                       random.randrange(-9,9),
                       random.randrange(-9,9),
                       random.randrange(-9,9)])
print("B2 Genome: " + str(biomorph2.genome))
print()
Color_line = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))

drawnbiomorph = BioMorph((depth,0,0,0,0,0,0))
drawnbiomorph.create(500,250)
create()
Color_line = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
print(path)
#path = path.rstrip(".wav")
#path += ".ogg"
print(path)
pygame.mixer.music.load(path)
try:
    pygame.mixer.music.set_pos(info["first"])
except:
    print("unsupported filetype for setposition")
pygame.mixer.music.play()
wait = True
waittime = 0
run = False
while(wait):
    waittime += clock.get_time()
    if waittime >= info["first"]*1000:
        wait = False
        run = True
    clock.tick(60)
        
while(run):
    win.fill((0, 0, 0))
    draw(biomorph1, biomorph2,drawnbiomorph,elapsed,morphtime)
    
    elapsed += clock.get_time()
    if elapsed > morphtime:
        elapsed = 0
        biomorph1 = biomorph2
        biomorph2 = BioMorph([depth, # draw a biomorph - step 1. create a new biomorph object and initialize with genome
                       random.randrange(-9,9),
                       random.randrange(-9,9),
                       random.randrange(-9,9),
                       random.randrange(-9,9),
                       random.randrange(-9,9),
                       random.randrange(-9,9)])
        Color_line = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
        create()
        print("B2 Genome: " + str(biomorph2.genome))
        print()
        
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DELETE:
                textinput.clear_text()
        if event.type == pygame.QUIT:
            exit()

    pygame.display.update()
    clock.tick(60)


    
