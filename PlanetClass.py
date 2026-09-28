import PlanetColors

class Planet:
    def __init__(self, Coords, Velocity, Mass, Radius, Color):
        self.Color = Color
        self.Radius = Radius
        self.Mass = Mass
        self.Coords = Coords   ## [x,y]
        self.Velocity = Velocity ## [Vx, Vy]

    def getX(self):
        return self.Coords[0]

    def getY(self):
        return self.Coords[1]

    def setX(self, x):
        self.Coords[0] = x

    def setY(self, y):
        self.Coords[1] = y

    def getVx(self):
        return self.Velocity[0]

    def getVy(self):
        return self.Velocity[1]

    def setVx(self, Vx):
        self.Velocity[0] = Vx

    def setVy(self, Vy):
        self.Velocity[1] = Vy

