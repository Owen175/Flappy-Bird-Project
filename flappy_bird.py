import math
import pygame as py
import time
from bird import Bird
from pipe import Pipe
import random


def checkKeys():
    global anTime
    for event in py.event.get():
        if event.type == py.QUIT:
            quit()
        if event.type == py.KEYDOWN:
            if event.key == py.K_SPACE:
                flap.flap()
                anTime = 1
                # for playing note.wav file
                py.mixer.Sound.play(wings)


def scrollIm(img, scroll, y, tiles):
    i = 0
    while i < tiles:
        screen.blit(img, (img.get_width() * i
                          + scroll, y))
        i += 1


def birdPosSet(pos, img):
    screen.blit(img, (pos[0], pos[1]))


def cont(end):
    return flap.pos[1] >= bseHeight + flap.image.get_height() and not(end)


def newPipe(pL):
    pipeGap = random.randint(100, 250)
    bottomPipeStart = random.randint(400 - pipeGap, FrameHeight - bseHeight - 20)
    topPipeStart = bottomPipeStart - pipeGap - pipetop.get_height()
    pL.append(Pipe((FrameWidth, topPipeStart), pipetop.get_width(), pipetop.get_height(), pipetop))
    pL.append(Pipe((FrameWidth, bottomPipeStart), pipebottom.get_width(), pipebottom.get_height(), pipebottom))
    return pL


def drawPipe(pipe):
    screen.blit(pipe.img, (pipe.pipeStartPos, pipe.pipeTop))


def shiftPipe(pL, scroll):
    for i in range(len(pL)):
        pL[i].nextFrame(scroll)


def removeOffScreen(pL):
    pipePairs = []

    for i, p in enumerate(pL):
        if i%2 == 0:
            pipePairs.append([p])
        else:
            pipePairs[(i-1)//2].append(p)

    finList = []

    for pair in pipePairs:
        if pair[0].pipeEndPos >= 0:
            finList.extend(pair)
    return finList

def displayScore(score):
    score = str(score)
    for _ in range(3-len(score)):
        score = '0' + score

    digitList = []
    for char in score:
        match int(char):
            case 0:
                digitList.append(zero)
            case 1:
                digitList.append(one)
            case 2:
                digitList.append(two)
            case 3:
                digitList.append(three)
            case 4:
                digitList.append(four)
            case 5:
                digitList.append(five)
            case 6:
                digitList.append(six)
            case 7:
                digitList.append(seven)
            case 8:
                digitList.append(eight)
            case 9:
                digitList.append(nine)

    for i, dg in enumerate(digitList):
        screen.blit(dg, (20*i+30, 20))


py.init()
wings = py.mixer.Sound("audio/wing.wav")
die = py.mixer.Sound("audio/die.wav")
# NEED TO DO OTHER SOUNDS
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

zero = py.image.load('sprites/0.png')
one = py.image.load('sprites/1.png')
two = py.image.load('sprites/2.png')
three = py.image.load('sprites/3.png')
four = py.image.load('sprites/4.png')
five = py.image.load('sprites/5.png')
six = py.image.load('sprites/6.png')
seven = py.image.load('sprites/7.png')
eight = py.image.load('sprites/8.png')
nine = py.image.load('sprites/9.png')


bseHeight = bse.get_height()
bgScroll = 0
bseScroll = 0
speed = 90
FPS = 150
gravity = 100
initialVelocity = 0
startPos = (FrameWidth // 4, FrameHeight // 2)
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
pipeTime = time.time()
pipeInterval = 2  # Seconds

anTime = 0

pipeList = []

flap = Bird(image=bd, gravity=gravity, pos=startPos, mass=30, initVeloc=initialVelocity, an1=an1, an2=an2)
pipeList = newPipe(pipeList)
drawPipe(pipeList[0])

endGame = False

intScore = 0
while cont(endGame):
    lastTime = t
    t = time.time()
    deltaTime = t - lastTime
    anTime -= deltaTime * anSpeed
    if anTime > 0.5:
        anFrame = an2
    elif anTime < 0:
        anFrame = bd
    else:
        anFrame = an1

    checkKeys()

    scrollIm(bg, bgScroll, 0, tiles)


    pipeScroll = -speed * deltaTime
    bgScroll -= speed * deltaTime  # keeps the movement speed constant despite FPS changes
    bseScroll -= speed * deltaTime
    if abs(bgScroll) > bg.get_width():
        bgScroll = 0
    if abs(bseScroll) > bse.get_width():
        bseScroll = 0

    if pipeTime + pipeInterval < t:
        pipeList = newPipe(pipeList)
        pipeTime = t

    shiftPipe(pipeList, pipeScroll)
    pipeList = removeOffScreen(pipeList)
    for p in pipeList:
        drawPipe(p)

    pos = (pos[0], FrameHeight - flap.frameChange(deltaTime * timeMultiplier)[1])
    birdPosSet(pos, anFrame)

    birdEndPos = flap.pos[0] + flap.image.get_width()
    pipePairs = []
    for i, p in enumerate(pipeList):
        if i % 2 == 0:
            pipePairs.append([p])
        else:
            pipePairs[(i-1)//2].append(p)

    for pair in pipePairs:
        intScore += pair[0].checkForScore(flap.pos[0])
        p1y = pair[0].pipeTop + pipetop.get_height()
        p2y = pair[1].pipeTop
        flapRealPosy = FrameHeight - flap.pos[1]
        if not(flapRealPosy > p1y and flapRealPosy + flap.image.get_height() < p2y):
            birdX = flap.pos[0]
            if birdX + flap.image.get_width() > pair[0].pipeStartPos and birdX < pair[0].pipeEndPos:
                endGame = True

    scrollIm(bse, bseScroll, FrameHeight - bse.get_height(), tilesBse)
    displayScore(intScore)
    clock.tick(FPS)  # Limits the FPS to the num
    py.display.update()

screen.blit(gm_over, (FrameWidth // 2 - gm_over.get_width() // 2, FrameHeight // 2 - gm_over.get_height() // 2))
py.mixer.Sound.play(die)
while True:
    py.display.update()
    for event in py.event.get():
        if event.type == py.QUIT:
            quit()

# Need -
# Score - use digits given in sprites
