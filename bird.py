class Bird:
    def __init__(self, image, gravity, pos, mass, initVeloc=10, an1=None, an2=None):
        self.image = image
        self.an1 = an1
        self.an2 = an2
        self.gravity = gravity
        self.pos = pos
        self.velocity = initVeloc
        self.mass = mass
        self.gpe = self.gravity * self.mass * self.pos[1]

    def frameChange(self, dt):
        grav_force = -self.mass * self.gravity

        self.velocity = self.velocity + grav_force/self.mass * dt

        self.pos = (self.pos[0], self.pos[1] + self.velocity * dt)

        return self.pos

    def flap(self):
        self.velocity = 120
