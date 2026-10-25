from PlanetClass import Planet
import PlanetColors

## The first preset is a smaller blue planet and a larger red planet orbiting
## eachother, where the central point of orbit is closer to the larger red planet
## because of the difference in mass.
## The smaller blue planet is moving faster than the larger red planet


def Preset1():
    Planet1 = Planet(
        [-150, 0],
        [0, 1],
        2000,
        10,
        PlanetColors.Colors["BLUE"]
    )

    Planet2 = Planet(
        [150, 0],
        [0, -0.25],
        8000,
        30,
        PlanetColors.Colors["RED"]
    )

    return [Planet1, Planet2]

def Preset2():
    Planet1 = Planet(
        [-100, 60],
        [0, 2.4],
        20,
        5,
        PlanetColors.Colors["PINK"]
    )

    Planet2 = Planet(
        [0, 0],
        [0, -0.0048],
        10000,
        15,
        PlanetColors.Colors["TEAL"]
    )

    return [Planet1, Planet2]



def Preset3():
    Planet1 = Planet(
        [0, 99.9001],
        [3.15912, 0],
        10,
        5,
        PlanetColors.Colors["GREEN"]
    )

    Planet2 = Planet(
        [0, -0.0999],
        [-0.00315912, 0],
        10000,
        20,
        PlanetColors.Colors["YELLOW"]
    )

    return [Planet1, Planet2]

def Preset4():
    Planet1 = Planet(
        [-130, 0],
        [0, 0],
        1000,
        10,
        PlanetColors.Colors["MAGENTA"]
    )

    Planet2 = Planet(
        [130, 0],
        [0, 0],
        1000,
        10,
        PlanetColors.Colors["LIME"]
    )

    return [Planet1, Planet2]

def Preset5():
    Planet1 = Planet(
        [-120, -70],
        [.32, 0],
        700,
        3,
        PlanetColors.Colors["LIGHT_GREY"]
    )

    Planet2 = Planet(
        [120, 70],
        [-.32, 0],
        700,
        3,
        PlanetColors.Colors["SKY_BLUE"]
    )

    return [Planet1, Planet2]

def Preset6():
    Planet1 = Planet(
        [-120, -80],
        [.4, -1],
        10,
        3,
        PlanetColors.Colors["MAROON"]
    )

    Planet2 = Planet(
        [120, 60],
        [0, 0],
        10000,
        35,
        PlanetColors.Colors["ORANGE"]
    )

    return [Planet1, Planet2]

