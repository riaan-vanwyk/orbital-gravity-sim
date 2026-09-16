from ursina import *

import Renderer
import PlanetColors
import Physics
from PlanetClass import Planet
import Presets

from tkinter import *

window.borderless = False
window.size = (Renderer.WIN_WIDTH, Renderer.WIN_HEIGHT)
window.title = "GraviSim: 2D Orbital Gravity Simulator"

app = Ursina()

camera.orthographic = True
camera.fov = Renderer.FOV

screen = Renderer.NewScreen()

## Predefined Preset setter functions

def Preset1():
    global Planet1, Planet2
    Planet1, Planet2 = Presets.Preset1()

def Preset2():
    global Planet1, Planet2
    Planet1, Planet2 = Presets.Preset2()

def Preset3():
    global Planet1, Planet2
    Planet1, Planet2 = Presets.Preset3()

def Preset4():
    global Planet1, Planet2
    Planet1, Planet2 = Presets.Preset4()

def Preset5():
    global Planet1, Planet2
    Planet1, Planet2 = Presets.Preset5()

def Preset6():
    global Planet1, Planet2
    Planet1, Planet2 = Presets.Preset6()

## When the program starts, the program auto-loads the first preset.

Preset1()

## This is the gravitational constant, which can be adjusted to change the strength of gravity in the simulation.

G = 0.1

TOP_OF_MENU = Renderer.EFF_HEIGHT // 2 ## 169
LEFT = Renderer.EFF_WIDTH // -2 ## -300
MENU_HEIGHT = 15



def MenuClickHandler():

    if Renderer.GetMouseClicked():

        mouseX, mouseY = Renderer.GetMousePosition()

        # Convert mouse coordinates to framebuffer coordinates.
        mouseX = Renderer.XCoordToScreen(mouseX)
        mouseY = Renderer.YCoordToScreen(mouseY)

        print(mouseX, mouseY)

        if mouseY >= TOP_OF_MENU - MENU_HEIGHT:

            print("Menu is clicked")

            if (
                -300 <= mouseX < -185
            ):
                print("Load Preset is clicked")
                return "LoadPreset"

            elif (
                -185 <= mouseX < -10
            ):
                print("Create Simulation is clicked")
                return "CreateSimulation"

            elif (
                -10 <= mouseX < 130
            ):
                print("Toggle Trails is clicked")
                return "ToggleTrails"

def OpenMenu(MenuString):
    if MenuString == "LoadPreset":
        root = Tk()
        root.title("Load Preset")
        root.geometry("380x440")

        PresetFunctions = [
            Preset1,
            Preset2,
            Preset3,
            Preset4,
            Preset5,
            Preset6
        ]

        lblTitle = Label(
            root,
            text="Preset Loader",
            font=("Arial", 20)
        )
        lblTitle.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        lblSubTitle = Label(
            root,
            text=(
                "This menu allows you to choose from a predetermined list\n"
                "to change the look, behaviour and configuration of the\n"
                "two objects / planets in empty space."
            ),
            font=("Arial", 9)
        )
        lblSubTitle.grid(row=1, column=0, columnspan=2, pady=(0, 15))

        # Preset buttons
        for i in range(6):
            row = i // 2
            column = i % 2

            btnPreset = Button(
                root,
                text=f"Preset {i + 1}",
                width=12,
                height=4,
                font=("Arial", 9),
                command=PresetFunctions[i]
            )

            btnPreset.grid(
                row=row + 2,
                column=column,
                padx=10,
                pady=10
            )

        root.mainloop()

def update():

    Renderer.ClearBuff()

    # Calculate gravitational force
    Force = Physics.ComputeForce(
        Planet1,
        Planet2,
        G
    )

    # Apply force
    Physics.ApplyForce(
        Planet1,
        Planet2,
        Force
    )

    # Update positions
    Physics.UpdatePosition(Planet1)
    Physics.UpdatePosition(Planet2)



    # Draw Planet 1
    Renderer.DrawCircleInBuff(
        Renderer.XCoordToScreen(int(Planet1.getX())),
        Renderer.YCoordToScreen(int(Planet1.getY())),
        Planet1.Radius,
        Planet1.Color
    )

    # Draw Planet 2
    Renderer.DrawCircleInBuff(
        Renderer.XCoordToScreen(int(Planet2.getX())),
        Renderer.YCoordToScreen(int(Planet2.getY())),
        Planet2.Radius,
        Planet2.Color
    )

    ## Draw the top UI menu bar, the light-grey rectangle is to distinguish the menu from the simulation
    Renderer.DrawRectInBuff(Renderer.XCoordToScreen(LEFT), Renderer.YCoordToScreen(TOP_OF_MENU), Renderer.EFF_WIDTH, MENU_HEIGHT, PlanetColors.Colors.get("LIGHT_GREY"))
    Renderer.PrintString(Renderer.XCoordToScreen(LEFT), Renderer.YCoordToScreen(TOP_OF_MENU - 3), "Load Preset...")
    Renderer.PrintString(Renderer.XCoordToScreen(-175), Renderer.YCoordToScreen(TOP_OF_MENU - 3), "Create Simulation...")
    Renderer.PrintString(Renderer.XCoordToScreen(0), Renderer.YCoordToScreen(TOP_OF_MENU - 3), "Toggle Trails...")

    # Update framebuffer
    screen.texture = Renderer.UpdateScreen()
    OpenMenu(MenuClickHandler())


app.run()