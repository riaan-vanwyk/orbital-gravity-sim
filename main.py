from ursina import *

import Renderer
import PlanetColors
import Physics
from PlanetClass import Planet
import Presets

from tkinter import *
from tkinter import messagebox

import time

window.borderless = False
window.size = (Renderer.WIN_WIDTH, Renderer.WIN_HEIGHT)
window.title = "GraviSim: 2D Orbital Gravity Simulator"

app = Ursina()

camera.orthographic = True
camera.fov = Renderer.FOV

screen = Renderer.NewScreen()

LastClickedTime = time.time()

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

ShowTrailsEnabled = False
TrailsBuffer = []
TRAIL_LENGTH = 100

def UpdateTrails(p1_x, p1_y, p2_x, p2_y):
    global TrailsBuffer

    if len(TrailsBuffer) <= TRAIL_LENGTH:
        TrailsBuffer.append([[p1_x, p1_y], [p2_x, p2_y]])
        ## print(TrailsBuffer)
    else:
        del TrailsBuffer[0]
        TrailsBuffer.append([[p1_x, p1_y], [p2_x, p2_y]])

def ShowTrails():
    global TrailsBuffer
    UpdateTrails(Planet1.getX(), Planet1.getY(), Planet2.getX(), Planet2.getY())
    for item in TrailsBuffer:
        Renderer.DrawPixelInBuff(int(Renderer.XCoordToScreen(item[0][0])),
        int(Renderer.YCoordToScreen(item[0][1])), PlanetColors.Colors.get("WHITE"))

        Renderer.DrawPixelInBuff(int(Renderer.XCoordToScreen(item[1][0])),
        int(Renderer.YCoordToScreen(item[1][1])), PlanetColors.Colors.get("WHITE"))


G = 0.1

TOP_OF_MENU = Renderer.EFF_HEIGHT // 2 ## 169
LEFT = Renderer.EFF_WIDTH // -2 ## -300
MENU_HEIGHT = 15



def MenuClickHandler():

    global LastClickedTime

    if Renderer.GetMouseClicked() and (time.time() - LastClickedTime >= 0.5):

        LastClickedTime = time.time()

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
    global Planet1, Planet2
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



    elif MenuString == "CreateSimulation":

        root = Tk()
        root.title("Create Simulation")
        root.geometry("400x630")


        lblTitle = Label(
            root,
            text="Create Simulation",
            font=("Arial", 20)
        )
        lblTitle.pack(pady=10)


        lblSubTitle = Label(
            root,
            text=(
                "Enter custom parameters for both objects.\n"
                "Values will be applied instantly."
            ),
            font=("Arial", 9)
        )
        lblSubTitle.pack(pady=5)


        # -------------------------
        # Planet Frames
        # -------------------------

        planet_frame = Frame(root)
        planet_frame.pack(pady=10)


        planet1_frame = Frame(planet_frame)
        planet1_frame.pack(
            side="left",
            padx=10
        )


        planet2_frame = Frame(planet_frame)
        planet2_frame.pack(
            side="left",
            padx=10
        )


        def make_field(frame, label_text, default):

            lbl = Label(
                frame,
                text=label_text
            )

            lbl.pack()

            entry = Entry(
                frame,
                width=20
            )

            entry.insert(
                0,
                str(default)
            )

            entry.pack(pady=3)

            return entry


        # -------------------------
        # Planet 1
        # -------------------------

        Label(
            planet1_frame,
            text="Planet 1",
            font=("Arial", 14)
        ).pack(pady=(10, 5))


        p1_x = make_field(
            planet1_frame,
            "X:",
            Planet1.getX()
        )

        p1_y = make_field(
            planet1_frame,
            "Y:",
            Planet1.getY()
        )

        p1_vx = make_field(
            planet1_frame,
            "Vx:",
            Planet1.getVx()
        )

        p1_vy = make_field(
            planet1_frame,
            "Vy:",
            Planet1.getVy()
        )

        p1_mass = make_field(
            planet1_frame,
            "Mass:",
            Planet1.Mass
        )

        p1_radius = make_field(
            planet1_frame,
            "Radius:",
            Planet1.Radius
        )

        p1_color = make_field(
            planet1_frame,
            "Color:",
            PlanetColors.getColorName(Planet1.Color)
        )


        # -------------------------
        # Planet 2
        # -------------------------

        Label(
            planet2_frame,
            text="Planet 2",
            font=("Arial", 14)
        ).pack(pady=(10, 5))


        p2_x = make_field(
            planet2_frame,
            "X:",
            Planet2.getX()
        )

        p2_y = make_field(
            planet2_frame,
            "Y:",
            Planet2.getY()
        )

        p2_vx = make_field(
            planet2_frame,
            "Vx:",
            Planet2.getVx()
        )

        p2_vy = make_field(
            planet2_frame,
            "Vy:",
            Planet2.getVy()
        )

        p2_mass = make_field(
            planet2_frame,
            "Mass:",
            Planet2.Mass
        )

        p2_radius = make_field(
            planet2_frame,
            "Radius:",
            Planet2.Radius
        )

        p2_color = make_field(
            planet2_frame,
            "Color:",
            PlanetColors.getColorName(Planet2.Color)
        )


        def ApplyValues():
            try:

                Planet1.setX(float(p1_x.get()))
                Planet1.setY(float(p1_y.get()))

                Planet1.setVx(float(p1_vx.get()))
                Planet1.setVy(float(p1_vy.get()))

                Planet1.Mass = float(p1_mass.get())
                Planet1.Radius = int(p1_radius.get())

                Planet1.Color = PlanetColors.Colors[
                    p1_color.get().upper()
                ]


                Planet2.setX(float(p2_x.get()))
                Planet2.setY(float(p2_y.get()))

                Planet2.setVx(float(p2_vx.get()))
                Planet2.setVy(float(p2_vy.get()))

                Planet2.Mass = float(p2_mass.get())
                Planet2.Radius = int(p2_radius.get())

                Planet2.Color = PlanetColors.Colors[
                    p2_color.get().upper()
                ]
            except:
                messagebox.showerror(
                    "Invalid Values",
                    "One or more values entered are invalid."
                )


        Button(
            root,
            text="Apply Values",
            command=ApplyValues
        ).pack(pady=15)


        root.mainloop()

    elif MenuString == "ToggleTrails":
        global ShowTrailsEnabled, TrailsBuffer
        TrailsBuffer = []
        ShowTrailsEnabled = not ShowTrailsEnabled


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

    global ShowTrailsEnabled
    if ShowTrailsEnabled:
        ShowTrails() ## I do this before I draw the planets so that the planets are
    ## Drawn on top of the trail so that the trail is behind the planet and not on
    ## top of it

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