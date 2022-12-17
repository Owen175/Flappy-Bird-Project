import pygame as py
import os
import math

FrameHeight = 600
FrameWidth = 900


os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (500, 200)

py.init()
py.display.set_caption("Loading....")
screen = py.display.set_mode((1, 1))

# Loading sounds and images
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

wings = py.mixer.Sound('audio/wing.wav')
die = py.mixer.Sound('audio/die.wav')
point = py.mixer.Sound('audio/point.wav')
py.mixer.music.load('audio/theme_tune.mp3')

bseHeight = bse.get_height()
bgScroll = 0
bseScroll = 0
FPS = 150
gravity = 100
initialVelocity = 0
startPos = (FrameWidth // 4, FrameHeight // 2)
scoreDist = 25
pointWhenPassed = False
toggleSFX = False
toggleMusic = False
soundOnPoint = False
regularPipeIntervals = False  # False means that the intervals are randomised,
                              # however, there is a minimum to make it possible

minPipeInterval = 1  # Seconds. Could be 2 if regularPipeIntervals is true.
speed = 120  # How fast the bird moves
mass = 70  # Mass of bird
timeMultiplier = 3.5  # Changes the speed that gravity acts on the bird
anSpeed = 6  # Changes the animation speed

# Don't Change ...
if toggleSFX:
    toggleMusic = True
    soundOnPoint = True
clock = py.time.Clock()
highScore = 0
pipeInterval = minPipeInterval

# CHANGE THE BELOW 1 TO UPPER NUMBER IF
# BUFFERING OF THE IMAGE
# HERE 1 IS THE CONSTANT FOR REMOVING BUFFERING
tiles = math.ceil(FrameWidth / bg.get_width()) + 1
tilesBse = math.ceil(FrameWidth / bse.get_width()) + 1

with open('highScore.txt', 'r') as f:
    AllTimeHS = int(f.read())
    print(f'The all time High Score is {AllTimeHS}. Good luck!')
