import math
import PlanetClass
## The physics for the program

def DetermineDistances(Planet1, Planet2):
    ## Determines the Dx, Dy, "r" value
    ## Pythagorean theorem is applicable here, only for r value
    Dx = Planet2.getX() - Planet1.getX()
    Dy = Planet2.getY() - Planet1.getY()
    r = (Dx**2 + Dy**2)**.5
    return {"Dx" : Dx, "Dy" : Dy, "r" : r} ## distance in pixels

def ComputeForce(Planet1, Planet2, G):  ## (G * m1 * m2) / (r + S)^2
    Softening = 2 ## in px, net as dit `n singularity approach
    Radius = DetermineDistances(Planet1, Planet2)["r"]

    Numerator = G * Planet1.Mass * Planet2.Mass
    if Radius < 5:
        Denominator = (Radius + Softening)**2
    else:
        Denominator = Radius**2

    return Numerator / Denominator



def ApplyForce(Planet1, Planet2, Force):
    ## Ek moet die Force en angle convert na Fx en Fy

    ## Fx = F cos Theta, Fy = F sin Theta
    Distances = DetermineDistances(Planet1, Planet2)


    Dx = Distances["Dx"]
    Dy = Distances["Dy"]
    r = Distances["r"]

    Fx = Force * Dx / r
    Fy = Force * Dy / r

    Planet1.setVx(Planet1.getVx() + Fx / Planet1.Mass)
    Planet1.setVy(Planet1.getVy() + Fy / Planet1.Mass)

    Planet2.setVx(Planet2.getVx() - Fx / Planet2.Mass)
    Planet2.setVy(Planet2.getVy() - Fy / Planet2.Mass)



def UpdatePosition(Planet):
    Planet.setX(Planet.getX() + Planet.getVx())
    Planet.setY(Planet.getY() + Planet.getVy())




