# GraviSim: 2D Orbital Gravity Simulator

Presentation: [📄 View Full Presentation](https://riaanvanwyk.onrender.com/view?https://riaanvwyk.onrender.com/GraviSim_Presentation.html)
<br><br>
![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)

#### Description:

##### 1. Introduction 
This Python project has not been made in one week, it has evolved from a simple way for me to learn how to draw pixels to the screen using `pygame`, till making a program with a single preset, no menus, no `<Create Simulation> ` feature, but working physics, to what it is today; which is a fully functional 2d Orbital Gravity Simulator, feauturing the ability to simulate 2 circular objects interacting gravitationally in space, where you can manually alter the Color, Radius, Weight, Velocity (x and y), and starting position (x and y), using the `<Create Simulation>` button, and 6 Presets that have altered these values in a predefined way. Also the ability to `<Toggle Trails>`, which just adds a nice color-gradient trail after one of the objects.
##### 2. Architectural Overview and Design 
When I was adding a menu function to the program, after I have implemented the core Newton's Laws Logic, I decided to use 2 independant menu systems, the first, the program's File, and Options Menu, I decided to implement in pure `pygame`, but when clicking on the `<Create Simulation>`, as well as the `<Load Preset...>` I decided to use `tkinter`. There was several reasons for this choice, the first because if i wanted to implement the `<Create Simulation>`, and  the `<Load Preset...>` menus actual popup windows in pygame, i would have to constanly check one or more of the objects were trying to render on top of the menu, and then not let it render. But the problem was that there was not just one menu with a dialog, there were 2, meaning that the sizes for each menu could probably be different. Let alone, I also only have a basic state management handler for the menu system, I would have to expand it to accommodate both systems. That's why I used `tkinter` to make a seperate window, so that the OS could handle all of the tricky stuff.
Pygame is also much better suited towards High-performance GPU-bound rendering, while tkinter is mostly used for GUI interfaces. 
Both of these menu systems run on the same main event loop, meaning that cross-integration was easy.
##### 3. Core Physics engine Mathematics 
This paragraph is focussing entirely on the `Update_coords_and_vel()` function, since that is basically the entire physics engine. The first part of the function just uses Pythagoras' theorem to determine the distance between the 2 planets/objects, then, if the distance is smaller than 1 unit 1 make it 1 unit, otherwise I risk a `ZeroDivisionError` or very unpredictable behaviour, especially in the preset where the balls are flying directly towards eachother. Then I use a version of Newton's Universal Gravitation Law, except with much less power since the program does not understand Newton units. The `velocity_pull` and  `total_force` ideas you will not find in any Newtonian textbook, this is just some custom python code to determine the change in velocity from the force between the objects, which I did not use any real formula for; I just experimented until it worked. I also used the unit vector approach, although I also do not have much expererience working with it, but it is less complex than using Sin() and Cos() to determine the force magnitudes. Then I just update the 4 variables, the x and y coordinate of the first and second object, as well as the velocity for both objects. 
##### 3. Installation, Prerequisites, and Execution:
You'll need Python, and if between versions 3.8 - 3.12, also `pip install pygame`. If above v. 3.12, use `pip install pygame-ce`. Your python `tkinter` module should also be installed. If on Windows 7+, you can just double-click the `start.bat` file. If not on Windows, manually launch `python3 project.py` from the Terminal.

##### 4. Usage 
When the `project.py` is open, Preset 1 will be loaded an a menu of `File | Options` will be at the top. To exit the program, either use File-> Exit , or The 'x' button on your device. To Load a preset, use the File -> Load Preset... button, which will give you an option of 6 presets. Preset 1 is the one already loaded at the start of the program, the pink object orbiting somewhat elliptically around the larger teal object. Preset 2 

### **Usage**

When `project.py` is open, **Preset 1** will be loaded, and a menu bar appears at the top with:

-   **File**
    
-   **Options**
    

#### **Exiting the Program**

You can exit the simulator using either:

-   `File -> Exit`
    
-   The window’s close button (`X`)
    

#### **Loading Presets**

To load a preset:

-   Go to `File -> Load Preset...`
    
-   Choose one of the six available presets
    

Preset 1 is the default preset shown at startup. Each preset simply provides a different set of initial conditions (mass, radius, velocity, position, color). They demonstrate various orbital behaviors. For example, Preset 3 looks like a small green planet orbiting very non-uniformly around a big yellow "sun".

#### **Creating a Custom Simulation**

To create your own simulation:

-   Go to `Options -> Create Simulation`
    
-   A Tkinter window will appear where you can set:
    
    -   Color
        
    -   Radius
        
    -   Mass
        
    -   Initial X/Y position
        
    -   Initial X/Y velocity
        

#### **Trails**

You can toggle orbital trails using:

-   `Options -> Toggle Trails`
    

This adds a color‑gradient trail behind one of the objects.
#### **Testing**

To test project.py, just run `python pytest.py`, and it will run all of the tests.

##### 5. Project Structure 
```
Project Structure -> 

(Folder) FinalProject 
   ---> project.py - Where the whole menu system, presets, custom simulation, and orbital simulator code is located 
   ---> test_project.py - Like week 5's pytest exercises where we need to test the functions inside of the program
   ---> requirements.txt - what python packages you need installed 
   ---> README.md - Description of everything
   ---> start.bat - It opens project.py , and keeps the console open afterwards so that you can read any errors that might occur
   ---> Struct.txt - A copy of this same Project Structure definition
   ---> pytest.py - This is for testing the program.
   
          
