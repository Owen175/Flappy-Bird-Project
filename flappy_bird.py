# import pygame as py
import time
from bird import Bird
from pipe import Pipe
import random
from config import *


def checkKeys(brd, anTime, t, skipTime):
    oldt = t
    for evt in py.event.get():
        if evt.type == py.QUIT:
            quit()
        if evt.type == py.KEYDOWN:
            if evt.key == py.K_SPACE:
                brd.flap()
                anTime = 1
                # for playing note.wav file
                py.mixer.Sound.play(wings)
            if evt.key == py.K_q:
                quit()
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
                                skipTime = time.time() - oldt
                            if e.key == py.K_q:
                                quit()
                    py.display.update()
    return anTime, skipTime


def scrollIm(img, scroll, y, tls):
    i = 0
    while i < tls:
        screen.blit(img, (img.get_width() * i + scroll, y))
        i += 1


def birdPosSet(pos, img):
    screen.blit(img, (pos[0], pos[1]))


def cont(end, brd):
    return brd.pos[1] >= bseHeight + brd.image.get_height() and not end


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


def displayScore(score, endG, coords=[30, 20], count=3):
    if score == 999:
        print('You won with a score of 999. Well done.')
        endG = True
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
    return endG


skipTime = 0


def main(bgScroll, bseScroll, highScore, AllTimeHS, pipeInterval, pointWhenPassed):
    initialVelocity = 0
    anTime = 0
    skipTime = 0
    pos = startPos
    t = time.time()
    pipeList = []
    pipeTime = time.time()
    flap = Bird(image=bd, gravity=gravity, pos=startPos, mass=30, initVeloc=initialVelocity, an1=an1, an2=an2)
    pipeList = newPipe(pipeList)
    drawPipe(pipeList[0])
    lastTime = time.time()
    deltaTime = 0.00001

    endGame = False
    intScore = 0
    loopCount = 0
    cumulativeSkipTime = 0
    while cont(endGame, flap):
        anTime, skipTime = checkKeys(flap, anTime, t, skipTime)
        lastTime = t
        t = time.time()
        deltaTime = t - lastTime - skipTime
        anTime -= deltaTime * anSpeed
        cumulativeSkipTime += skipTime
        if anTime > 0.5:
            anFrame = an1
        elif anTime > 0:
            anFrame = an2
        elif anTime > -0.5:
            anFrame = an1
        else:
            anFrame = bd

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
            if pipeTime + cumulativeSkipTime + minPipeInterval < time.time():
                pipeTime = t
                pipeList = newPipe(pipeList)
        else:
            if time.time() > pipeInterval + cumulativeSkipTime + pipeTime:
                pipeList = newPipe(pipeList)
                pipeTime = time.time()
                pipeInterval = minPipeInterval / max(math.sqrt(random.random()), 0.5)

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
                pipePairs[(i - 1) // 2].append(p)

        for pair in pipePairs:
            additionToScore = pair[0].checkForScore(flap.pos[0], pointWhenPassed)
            intScore += additionToScore
            if additionToScore == 1 and soundOnPoint:
                py.mixer.Sound.play(point)

            p1y = pair[0].pipeTop + pipetop.get_height()
            p2y = pair[1].pipeTop
            # flap.pos = (flap.pos[0], FrameHeight-p2y)

            for row in [flap.shape[0], flap.shape[2], flap.shape[4], flap.shape[6], flap.shape[12], flap.shape[14],
                        flap.shape[16], flap.shape[20], flap.shape[23]]:
                start = row[0]
                start = [start[0] + flap.pos[0], start[1] + FrameHeight - flap.pos[1]]

                flapRealPosy = start[1]  # FrameHeight-start[1]
                if not (p1y < flapRealPosy < p2y):
                    end = row[1]
                    end = end[0] + flap.pos[0]

                    if end > pair[0].pipeStartPos and start[0] < pair[0].pipeEndPos:
                        endGame = True

        scrollIm(bse, bseScroll, FrameHeight - bse.get_height(), tilesBse)
        endGame = displayScore(intScore, endGame)
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
                    return highScore, AllTimeHS
                if event.key == py.K_q:
                    print(f'Session High Score was {highScore}')
                    quit()


py.init()

# PYGAME FRAME WINDOW
py.display.set_caption("Flappy Bird V2")
screen = py.display.set_mode((FrameWidth, FrameHeight))

t = time.time()
clock.tick(33)

if toggleMusic:
    py.mixer.music.play(-1)  # Repeats

while True:
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
                if evt.key == py.K_q:
                    quit()
    highScore, AllTimeHS = main(bgScroll, bseScroll, highScore, AllTimeHS, pipeInterval, pointWhenPassed)
