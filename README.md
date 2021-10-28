# MazerBlender
Blender add-on for creating Gazebo static meshes

**Advantages:**
	
	- Can with just two mouse-clicks wrap 3d-model file into a static gazebo mesh
	
	- Not only generates labyrinths, but also allows to modify them
	
	- Allows to add other models to labyrinths, so they can be exported as a single mesh
	
**Disadvantages:**
	
	- Blender is needed
	
	- For only .stl and .fbx exporting is available
	
	- Blenders assets size is different from Gazebos
	
	- For now only three types of "labyrinths" are avaliable

**Instructions:**

1) Install Blender and add Mazer.py as an addon
	
2) Open addons list and select "Maze Constructor"

3) Press "Spawn maze", select "labyrinth" type and specify width and length. Then Press OK. Assembling large labyrinths will take some time.

4) After the maze appeared, and all needed actions were done, press "Export" on Mazer plate. 

5) Specify meshs location, it's name and 3d-models files extension.

Here you are.

Note that the width and the length of the labyrinth does not represent any metric system values.
Just how many squares 1x1 will have its map. By default corridor width is 1, and the wall thickness is also 1.
And that's without the border walls. So the result will minimem gain 2 on both dimentions.
And, of how the mazeconstructing algorythm works, makes avaliable only odd sizes. So if you have passed an even size, it wil gain 1.

>Desired width:  10		Result width:  10 + 1 + 2 = 13 
>Desired length: 11 		Result length: 11 + 2 = 13

For now only three laburinths are avaliable:
**- Labyrinth**
		
		It's a classical labyrinth where always exists only and only one way from one point to another.
		
**- Inverted labyrinth**
		
		A normal labyrinth where coridors are walls, and walls are coridors. Suposed to be treated as a complicated obstacle.
**- Office-like labyrinth**
		
		This one is different. Unlike of two previous, this one will have an absolutely unpredictable result.
		It may take a while, before it will generate something, that will satisfy you. 
		A chance of having some closed "rooms" could be as an advantage and as a disadvantage.
		
For any questions, or suggestions write to snakeinacartonbox@gmail.com
