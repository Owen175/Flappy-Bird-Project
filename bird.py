class Bird:
    def __init__(self, image, gravity, pos, mass, initVeloc=0, an1=None, an2=None):
        self.image = image
        self.an1 = an1
        self.an2 = an2
        self.gravity = gravity
        self.pos = pos
        self.velocity = initVeloc
        self.mass = mass
        self.gpe = self.gravity * self.mass * self.pos[1]
        self.height = self.image.get_height()
        self.width = self.image.get_width()

        self.shape = []
        for y in range(self.height):
            startPos = 0
            endPos = 0
            for x in range(self.width):
                R, G, B, _ = self.image.get_at((x,y))
                if R == 0 and G == 0 and B == 0:
                    if endPos == 0:
                        endPos = x
                else:
                    if startPos == 0:
                        startPos = x
                    endPos = 0
            self.shape.append([[startPos, self.height-y], [endPos, self.height-y]])

    def frameChange(self, dt):
        grav_force = -self.mass * self.gravity

        self.velocity = self.velocity + grav_force/self.mass * dt

        self.pos = (self.pos[0], self.pos[1] + self.velocity * dt)

        return self.pos

    def flap(self):
        self.velocity = 120
