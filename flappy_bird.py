import math
import pygame as py
import time
from bird import Bird

def checkKeys():
    global anTime
    for event in py.event.get():
        if event.type == py.QUIT:
            quit()
        if event.type == py.KEYDOWN:
            if event.key == py.K_SPACE:
                flap.flap()
                anTime = 1

def scrollIm(img, scroll, y, tiles):
    i = 0
    while i < tiles:
        screen.blit(img, (img.get_width() * i
                         + scroll, y))
        i += 1

def birdPosSet(pos, img):
    screen.blit(img, (pos[0], pos[1]))

py.init()

clock = py.time.Clock()

FrameHeight = 600
FrameWidth = 900

# PYGAME FRAME WINDOW
py.display.set_caption("Flappy Bird V2")
screen = py.display.set_mode((FrameWidth,
                              FrameHeight))

# IMAGE

pipetop = py.image.load('sprites/pipetop.png').convert()
pipebottom = py.image.load('sprites/pipebottom.png').convert()
bg = py.image.load('sprites/background-night.png').convert()
bse = py.image.load('sprites/ground.png').convert()
bd = py.image.load('sprites/redbird-downflap.png').convert()
an1 = py.image.load('sprites/redbird-midflap.png').convert()
an2 = py.image.load('sprites/redbird-upflap.png').convert()
gm_over = py.image.load('sprites/gameover.png').convert()

bseHeight = bse.get_height()
bgScroll = 0
bseScroll = 0
speed = 90
FPS = 150
gravity = 100
initialVelocity = 0
startPos = (FrameWidth//4, FrameHeight//2)
pos = startPos
mass = 70
timeMultiplier = 3.5
anSpeed = 6

# CHANGE THE BELOW 1 TO UPPER NUMBER IF
# BUFFERING OF THE IMAGE
# HERE 1 IS THE CONSTANT FOR REMOVING BUFFERING
tiles = math.ceil(FrameWidth / bg.get_width()) + 1
tilesBse = math.ceil(FrameWidth / bse.get_width()) + 1
t = time.time()
clock.tick(33)

anTime = 0

flap = Bird(image=bd, gravity=gravity, pos=startPos, mass=30, initVeloc=initialVelocity, an1=an1, an2=an2)

while flap.pos[1] >= bseHeight:
    lastTime = t
    t = time.time()
    deltaTime = t-lastTime
    anTime -= deltaTime * anSpeed
    if anTime > 0.5:
        anFrame = an2
    elif anTime < 0:
        anFrame = bd
    else:
        anFrame = an1

    checkKeys()

    scrollIm(bg, bgScroll, 0, tiles)
    scrollIm(bse, bseScroll, FrameHeight-bse.get_height(), tilesBse)

    bgScroll -= speed * deltaTime  # keeps the movement speed constant despite FPS changes
    bseScroll -= speed * deltaTime
    if abs(bgScroll) > bg.get_width():
        bgScroll = 0
    if abs(bseScroll) > bse.get_width():
        bseScroll = 0


    pos = (pos[0], FrameHeight - flap.frameChange(deltaTime*timeMultiplier)[1])
    birdPosSet(pos, anFrame)

    clock.tick(FPS) # Limits the FPS to the num
    py.display.update()

screen.blit(gm_over, (FrameWidth//2 - gm_over.get_width()//2, FrameHeight//2-gm_over.get_height()//2))
while True:
    py.display.update()
    for event in py.event.get():
        if event.type == py.QUIT:
            quit()


# Need -
# Add posts - Got them in the code - random widths, but not too high/low + random heights.
# Score - use digits given in sprites