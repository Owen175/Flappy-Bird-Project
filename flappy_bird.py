import math
import pygame as py
import time
from bird import Bird
from pipe import Pipe
import random
import sys
import soundfile as sf
import soundcard as sc
import threading





def checkKeys():
    global anTime
    global t
    global skipTime
    oldt = t
    for evt in py.event.get():
        if evt.type == py.QUIT:
            quit()
        if evt.type == py.KEYDOWN:
            if evt.key == py.K_SPACE:
                flap.flap()
                anTime = 1
                # for playing note.wav file
                py.mixer.Sound.play(wings)
            if evt.key == py.K_p:
                paused = True
                py.mixer.music.pause()
                while paused:
                    for e in py.event.get():
                        if evt.type == py.QUIT:
                            quit()
                        if e.type == py.KEYDOWN:
                            if e.key == py.K_p:
                                paused = False
                                py.mixer.music.unpause()
                                t = oldt
                                skipTime = time.time() - t
                    py.display.update()


def scrollIm(img, scroll, y, tls):
    i = 0
    while i < tls:
        screen.blit(img, (img.get_width() * i + scroll, y))
        i += 1


def birdPosSet(pos, img):
    screen.blit(img, (pos[0], pos[1]))


def cont(end):
    return flap.pos[1] >= bseHeight + flap.image.get_height() and not end


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
    pPair = []

    for i, p in enumerate(pL):
        if i % 2 == 0:
            pPair.append([p])
        else:
            pPair[(i - 1) // 2].append(p)

    finList = []

    for pr in pPair:
        if pr[0].pipeEndPos >= 0:
            finList.extend(pr)
    return finList


def displayScore(score, coords=[30, 20], count=3):
    global endgame
    if score == 999:
        print('You won with a score of 999. Well done.')
        endgame = True
    score = str(score)
    for _ in range(count - len(score)):
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
        screen.blit(dg, (scoreDist * i + coords[0], coords[1]))

skipTime = 0
def main():
    global flap
    global t
    global bgScroll
    global bseScroll
    global anTime
    global highScore
    global endGame
    global AllTimeHS
    global pipeInterval
    global skipTime
    initialVelocity = 0
    anTime = 0
    pos = startPos
    t = time.time()
    pipeList = []
    pipeTime = time.time()
    flap = Bird(image=bd, gravity=gravity, pos=startPos, mass=30, initVeloc=initialVelocity, an1=an1, an2=an2)
    pipeList = newPipe(pipeList)
    drawPipe(pipeList[0])

    endGame = False
    intScore = 0
    loopCount = 0
    while cont(endGame):
        checkKeys()
        lastTime = t + skipTime
        t = time.time()
        deltaTime = t - lastTime
        anTime -= deltaTime * anSpeed
        if anTime > 0.5:
            anFrame = an2
        elif anTime < 0:
            anFrame = bd
        else:
            anFrame = an1

        if loopCount == 0:
            loopCount += 1
            flap.flap()
            anTime = 1
            # for playing note.wav file
            py.mixer.Sound.play(wings)
        scrollIm(bg, bgScroll, 0, tiles)

        pipeScroll = -speed * deltaTime
        bgScroll -= speed * deltaTime  # keeps the movement speed constant despite FPS changes
        bseScroll -= speed * deltaTime
        if abs(bgScroll) > bg.get_width():
            bgScroll = 0
        if abs(bseScroll) > bse.get_width():
            bseScroll = 0
        if regularPipeIntervals:
            if pipeTime + minPipeInterval < t + skipTime:
                pipeTime = t
                pipeList = newPipe(pipeList)
        else:
            if pipeTime + pipeInterval < t + skipTime:
                pipeList = newPipe(pipeList)
                pipeTime = t
                pipeInterval = minPipeInterval / max(math.sqrt(random.random()), 0.5)


        shiftPipe(pipeList, pipeScroll)
        pipeList = removeOffScreen(pipeList)
        for p in pipeList:
            drawPipe(p)

        pos = (pos[0], FrameHeight - flap.frameChange((deltaTime) * timeMultiplier)[1])
        birdPosSet(pos, anFrame)

        birdEndPos = flap.pos[0] + flap.image.get_width()
        pipePairs = []
        for i, p in enumerate(pipeList):
            if i % 2 == 0:
                pipePairs.append([p])
            else:
                pipePairs[(i - 1) // 2].append(p)

        for pair in pipePairs:
            additionToScore = pair[0].checkForScore(flap.pos[0])
            intScore += additionToScore
            if additionToScore == 1 and soundOnPoint:
                py.mixer.Sound.play(point)
            p1y = pair[0].pipeTop + pipetop.get_height()
            p2y = pair[1].pipeTop
            flapRealPosy = FrameHeight - flap.pos[1]
            if not (flapRealPosy > p1y and flapRealPosy + flap.image.get_height() < p2y):
                birdX = flap.pos[0]
                if birdX + flap.image.get_width() > pair[0].pipeStartPos and birdX < pair[0].pipeEndPos:
                    endGame = True

        scrollIm(bse, bseScroll, FrameHeight - bse.get_height(), tilesBse)
        displayScore(intScore)
        clock.tick(FPS)  # Limits the FPS to the num
        py.display.update()
        skipTime = 0

    screen.blit(gm_over, (FrameWidth // 2 - gm_over.get_width() // 2, FrameHeight // 2 - gm_over.get_height() // 2))
    py.mixer.Sound.play(die)

    if intScore > highScore:
        highScore = intScore
    if highScore > AllTimeHS:
        with open('highScore.txt', 'w') as f:
            f.write(str(highScore))
        AllTimeHS = highScore
        print(f'Congratulations, you beat the all time high score. It is now {highScore}')
    print(f'Current Session High score is {highScore}')
    while True:
        exit = False
        py.display.update()
        for event in py.event.get():
            if event.type == py.QUIT:
                print(f'Session High Score was {highScore}')
                quit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_r:
                    exit = True
        if exit:
            break

with open('highScore.txt', 'r') as f:
    AllTimeHS = int(f.read())
    print(f'The all time High Score is {AllTimeHS}. Good luck!')

py.init()
wings = py.mixer.Sound('audio/wing.wav')
die = py.mixer.Sound('audio/die.wav')
point = py.mixer.Sound('audio/point.wav')
themeTune = py.mixer.music.load('audio/theme_tune.mp3')


clock = py.time.Clock()

FrameHeight = 600
FrameWidth = 900

# PYGAME FRAME WINDOW
py.display.set_caption("Flappy Bird V2")
screen = py.display.set_mode((FrameWidth, FrameHeight))

# IMAGE
tn = py.image.load('sprites/black.png').convert()
pipetop = py.image.load('sprites/pipetop.png').convert()
pipebottom = py.image.load('sprites/pipebottom.png').convert()
bg = py.image.load('sprites/background-night.png').convert()
bse = py.image.load('sprites/ground.png').convert()
bd = py.image.load('sprites/redbird-downflap.png').convert()
an1 = py.image.load('sprites/redbird-midflap.png').convert()
an2 = py.image.load('sprites/redbird-upflap.png').convert()
gm_over = py.image.load('sprites/gameover.png').convert()

# Removing the .convert removes the transparency
zero = py.image.load('sprites/0.png').convert()
one = py.image.load('sprites/1.png').convert()
two = py.image.load('sprites/2.png').convert()
three = py.image.load('sprites/3.png').convert()
four = py.image.load('sprites/4.png').convert()
five = py.image.load('sprites/5.png').convert()
six = py.image.load('sprites/6.png').convert()
seven = py.image.load('sprites/7.png').convert()
eight = py.image.load('sprites/8.png').convert()
nine = py.image.load('sprites/9.png').convert()

bseHeight = bse.get_height()
bgScroll = 0
bseScroll = 0
FPS = 150
gravity = 100
initialVelocity = 0
startPos = (FrameWidth // 4, FrameHeight // 2)
scoreDist = 25
toggleMusic = False
regularPipeIntervals = False
soundOnPoint = False
minPipeInterval = 1  # Seconds. Could be 2 if regularPipeIntervals is true.
speed = 120
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


highScore = 0
if toggleMusic:
    py.mixer.music.play(-1)  # Repeats

pipeInterval = minPipeInterval

while True:
    #    py.mixer.Sound.play(tune)
    # for _ in range(2):
    #     # cursor up one line
    #     sys.stdout.write('\x1b[1A')
    #
    #     # delete last line
    #     sys.stdout.write('\x1b[2K')
    print('Press Space to play.')

    scrollIm(bg, 0, 0, tiles)
    scrollIm(bse, 0, FrameHeight - bse.get_height(), tilesBse)
    birdPosSet(startPos, bd)
    py.display.update()

    contLoop = True
    while contLoop:
        for evt in py.event.get():
            if evt.type == py.QUIT:
                quit()
            if evt.type == py.KEYDOWN:
                if evt.key == py.K_SPACE:
                    contLoop = False
    main()

#Randomise pipe interval