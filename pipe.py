class Pipe:
    def __init__(self, pos, pipeLen, pipeHeight, img):
        self.pipeLen = pipeLen
        self.pipeHeight = pipeHeight
        self.pipeStartPos = pos[0]
        self.pipeEndPos = pos[0] + pipeLen
        self.pipeTop = pos[1]
        self.pipeBottom = pos[1] + pipeHeight
        self.img = img
        self.count = 0

    def nextFrame(self, scroll):
        pos = (self.pipeStartPos + scroll, self.pipeTop)
        self.pipeStartPos = pos[0]
        self.pipeEndPos = pos[0] + self.pipeLen
        self.pipeTop = pos[1]
        self.pipeBottom = pos[1] + self.pipeHeight

    def checkForScore(self, xpos, pointWhenPassed):
        if pointWhenPassed:
            if xpos > self.pipeEndPos:
                if self.count == 0:
                    self.count += 1
                    return 1
        else:
            if xpos > self.pipeStartPos:
                if self.count == 0:
                    self.count += 1
                    return 1
        return 0
