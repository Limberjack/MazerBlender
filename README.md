# MazerBlender
Blender add-on for creating Gazebo static meshes

**Advantages:**
	
	- Can with just two mouse-clicks wrap 3d-model file into a static gazebo mesh
	
	- Not only generates labyrinths, but also allows to modify them
	
	- Allows to add other models to labyrinths, so they can be exported as a single mesh

	- Could be ran from the system termial, what could be used in automatation 
	
**Disadvantages:**
	
	- Blender is needed
	
	- For only .stl is available

**GUI Instructions:**

1) Install Blender and add Mazer.py as an addon
	
2) Open addons list and select "Maze Constructor"

3) Press "Spawn maze", select "labyrinth" type and specify width and length. Then Press OK. Assembling large labyrinths will take some time.

4) After the maze appeared, and all needed actions were done, press "Export" on Mazer plate. 

5) Specify meshs location, it's name and 3d-models files extension.


**Terminal Instructions:**
Go to "classes" folder and run 
	blender -b -P Mazer.py -- --init=path_where_you_want_your_configs_to_be_initialized
then this:
	blender -b -P Mazer.py -- --build=path_to_a_config_file

**- Labyrinth**
		
		It's a classical labyrinth where always exists only and only one way from one point to another.
		
**- Inverted labyrinth**

		A normal labyrinth where coridors are walls, and walls are coridors. Suposed to be treated as a complicated obstacle.

**- Random labyrinth**
		
		This one is different. Unlike of two previous, this one will have an absolutely unpredictable result.
		It may take a while, before it will generate something, that will satisfy you. 
		A chance of having some closed "rooms" could be as an advantage and as a disadvantage.
		
**- Rooms1 labyrinth**
		
		This spawns a matrix with sizes A and B. 
		Then randomly selects N positions on that matrix. This will be the rooms.
		Iterates over rooms list and connect currently selected room with one of all the others.

**- Rooms2 labyrinth**
		
		This is much like Rooms1, but this one has two rows for possible rooms positioning. 
		Then randomly selects N positions. And then add one long room between those rows. This is a main coridor.
		As soon as room is being spawned, we connect it to the main coridor.

For any questions, or suggestions write to snakeinacartonbox@gmail.com
