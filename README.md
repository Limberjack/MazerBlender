# MazerBlender
Blender add-on for creating Gazebo static meshes and buildings

**Advantages:**
	
	- Can with just two mouse-clicks wrap 3d-model file into a static gazebo mesh
	
	- Not only generates constructions, but also allows to modify them
	
	- Allows to add other models to labyrinths, so they can be exported as a single mesh

	- Has graphical user interface, built with blender Python API
	
**Disadvantages:**

	- For Only .stl is available for Gazebo-mesh export

**GUI Instructions:**

1) Install Blender and add Mazer.py as an addon
	
2) Open addons list and select "Maze Constructor"

3) Select the needed option

4) After the construction appearance, press "Export to the Gazebo mesh" on Mazer plate. 

5) Specify meshs location and it's name.


**- Classical labyrinth**
		
		It's a classical labyrinth where always exists only one way from one point to another. Due to the construction algorythm limitations, the sizes of this constructions would be counted by the following formula:
		
		result_size = initial_size + (initial_size + 1) % 2  

		So if you provide X as 10 and Y as 7, the final construction would have sizes: X: 11, and Y: 7.
		
		If you mark an "Invert" checkbox, the appeared construction will have walls and coridors swapped.
		
**- Rooms**
		
		This spawns a matrix with sizes A and B. 
		Then randomly selects N positions on that matrix. This will be the rooms.
		Iterates over rooms list and connect currently selected room with one of all the others.

		A and B should match condition where A * B >= N. If this condition was not fullfilled or A or B was not a natural number, they would be set with the value of N.

**- Rooms and coridor**
		
		This is much like "Rooms", but this one has two rows for possible rooms positioning. 
		Addon again randomly selects N positions. And then add one long room between those rows. This is a so called main coridor.
		As soon as room is being spawned, it's beeing connected to the main coridor.

		"Maximum number of rooms in a row" should have value that is not less, than "Number of rooms" divided by two. Otherwise it would be set with the value of thotal rooms number.


**Main features**

1) Random.	
	Random seed could be specified manually by user. To do so, uncheck "Use current time as..." checkbox and input the seed you need.

2) Obstacles.
	In room-based constructions it's possible to add obstacles.
	This repository provides four example stl-files.
	You may use any 3d-object files you want. To do this, put them all together in one folder and specify path to that folder in the corresponding input field.

	Please note that it is better to use obstacles that can be placed on 1 square meter, otherwise there is no guarantee that all points of the structure will be reachable.

For any questions, or suggestions write to snakeinacartonbox@gmail.com
