import bpy
from bpy_extras.io_utils import ExportHelper

import random
import os
import sys
import time

###------------------------------BasicLabyrinth------------------------------------------###

class CustomVector3D:
    x = 0
    y = 0
    z = 0

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "x:"+str(self.x)+",y:"+str(self.y)+",z:"+str(self.z)


class BasicLabyrinth:
    """Inherited by all constructions"""
    ROOM_SPACE = 1
    EMPTY_SPACE = 0
    WALL_SPACE = 2
    CORIDOR_SPACE = 3

    CUBE_WIDTH = 1.0
    CUBE_LENGTH = 1.0
    CUBE_HEIGHT = 1.0
    
    WALL_HEIGHT = 2.0

    __map_matrix__ : list()
    __seed__ : int()

    def __init__(self, seed: int):
        self.__seed__ = seed
        random.seed(seed)

    def __spawn_cube__(self, root_point: CustomVector3D, dist_point: CustomVector3D):
        diag_vector = CustomVector3D()
        diag_vector.x = dist_point.x - root_point.x + BasicLabyrinth.CUBE_WIDTH
        diag_vector.y = dist_point.y - root_point.y + BasicLabyrinth.CUBE_LENGTH
        diag_vector.z = dist_point.z - root_point.z + BasicLabyrinth.CUBE_HEIGHT
        bpy.ops.mesh.primitive_cube_add(enter_editmode=False,
                                        location=(root_point.x + diag_vector.x / 2, root_point.y + diag_vector.y / 2,
                                                  root_point.z + diag_vector.z / 2),
                                        rotation=(0, 0, 0), scale=(diag_vector.x / 2, diag_vector.y / 2, diag_vector.z / 2))

    def __spawn_wall__(self, wall_list: list):
        if len(wall_list) == 0:
            return

        point_a = wall_list[0]
        point_b = wall_list[len(wall_list)-1]
        point_b.z = BasicLabyrinth.WALL_HEIGHT + BasicLabyrinth.CUBE_HEIGHT

        diag_vector = CustomVector3D()
        diag_vector.x = point_b.x - point_a.x + BasicLabyrinth.CUBE_WIDTH
        diag_vector.y = point_b.y - point_a.y + BasicLabyrinth.CUBE_LENGTH
        diag_vector.z = point_b.z - point_a.z + BasicLabyrinth.CUBE_HEIGHT

        if len(wall_list) == 1:
            bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False,
                                            location=(point_a.x + diag_vector.x / 2, point_a.y + diag_vector.y / 2,
                                                      BasicLabyrinth.CUBE_HEIGHT + BasicLabyrinth.WALL_HEIGHT / 2),
                                            rotation=(0, 0, 0), scale=(BasicLabyrinth.CUBE_WIDTH, BasicLabyrinth.CUBE_LENGTH, BasicLabyrinth.WALL_HEIGHT))
            return

        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False,
                                        location=(point_a.x + diag_vector.x / 2, point_a.y + diag_vector.y / 2,
                                                  BasicLabyrinth.CUBE_HEIGHT + BasicLabyrinth.WALL_HEIGHT / 2),
                                        rotation=(0, 0, 0), scale=(diag_vector.x, diag_vector.y, BasicLabyrinth.WALL_HEIGHT ))

    def spawn(self):
        self.length = len(self.__map_matrix__)
        self.width = len(self.__map_matrix__[0])
        self.print_in_console()
        bottom_root_point = CustomVector3D(0, 0, 0)
        bottom_target_point = CustomVector3D(
            self.length - 1, self.width - 1, 0)
        self.__spawn_cube__(bottom_root_point, bottom_target_point)

        for x in range(0, self.length):
            horisontal_list = list()
            for y in range(0, self.width):
                if(self.__map_matrix__[x][y] == self.WALL_SPACE):
                    self.__map_matrix__[x][y] = -1
                    horisontal_list.append(CustomVector3D(x, y, BasicLabyrinth.CUBE_HEIGHT))
                else:
                    if len(horisontal_list) > 1:
                        self.__spawn_wall__(horisontal_list)
                    else:
                        if len(horisontal_list) == 1:
                            point = horisontal_list[0]
                            self.__map_matrix__[point.x][point.y] = self.WALL_SPACE
                    horisontal_list = list()
            self.__spawn_wall__(horisontal_list)

        for y in range(0, self.width):
            vertical_list = list()
            for x in range(0, self.length):
                if self.__map_matrix__[x][y] == self.WALL_SPACE:
                    vertical_list.append(CustomVector3D(x, y, BasicLabyrinth.CUBE_HEIGHT))
                else:
                    self.__spawn_wall__(vertical_list)
                    vertical_list = list()
            self.__spawn_wall__(vertical_list)
            
    def __verifyPainting__(self):
        for x in range(1, self.SettingsStorage.mapSize.x):
            for y in range(1, self.SettingsStorage.mapSize.y):
                if self.__map_matrix__[x][y] == self.ROOM_SPACE or self.CORIDOR_SPACE:
                    if x != 0 and self.__map_matrix__[x-1][y] == self.EMPTY_SPACE:
                        self.__map_matrix__[x-1][y] = self.WALL_SPACE
                    if x + 1 < self.SettingsStorage.mapSize.x and self.__map_matrix__[x+1][y] == self.EMPTY_SPACE:
                        self.__map_matrix__[x+1][y] = self.WALL_SPACE
                    if y != 0 and self.__map_matrix__[x][y-1] == self.EMPTY_SPACE:
                        self.__map_matrix__[x][y-1] = self.WALL_SPACE
                    if y + 1 < self.SettingsStorage.mapSize.y and self.__map_matrix__[x][y+1] == self.EMPTY_SPACE:
                        self.__map_matrix__[x][y+1] = self.WALL_SPACE

    @staticmethod
    def safeRand(min: int, max: int):
        return BasicLabyrinth.__safe_randint__(min=min, max=max)

    @staticmethod
    def __safe_randint__(min: int, max: int) -> int:
        if min == max:
            return min
        if min > max:
            return min

        return random.randint(min, max)

    def print_in_console(self):
        print("PRINTING")
        print(len(self.__map_matrix__))
        for x in range(0, len(self.__map_matrix__)):
            for y in range(0, len(self.__map_matrix__[x])):
                if self.__map_matrix__[x][y] == self.WALL_SPACE:
                    print("▓▓", end='')
                elif self.__map_matrix__[x][y] == self.ROOM_SPACE:
                    print("..", end="")
                else:
                    print("  ", end="")
            print("")
            
            
###------------------------------ObstacleRoom------------------------------------------###

class ObstacleRoom:
    __topLeft__: CustomVector3D
    __size__: CustomVector3D
    __numberOfObstacles__: int
    __pathToObstacles__: str

    def __init__(self, topLeft: CustomVector3D, size: CustomVector3D):
        self.__size__ = size
        self.__topLeft__ = topLeft
        

    def __collectMeshes__(self) -> list:
        result = list()
        for file in os.listdir(self.__pathToObstacles__):
            if file.endswith(".stl"):
                result.append(self.__pathToObstacles__ + "/" + file)
        return result

    def __spawnMesh__(self, mesh: str, position: CustomVector3D):
        print(mesh)
        rotation = BasicLabyrinth.safeRand(0, 360)
        position.x += BasicLabyrinth.CUBE_WIDTH / 2
        position.y += BasicLabyrinth.CUBE_LENGTH / 2
        position.z += BasicLabyrinth.CUBE_HEIGHT
        bpy.ops.import_mesh.stl(filepath=mesh)
        activeObject = bpy.context.object
        activeObject.rotation_euler.z += rotation
        activeObject.location.x += position.x
        activeObject.location.y += position.y
        activeObject.location.z += position.z


    def __collectPositions__(self, mapMatrix, root: CustomVector3D):
        points = list()
        dx = root.x
        dy = root.y
        while dx < self.__size__.x + self.__topLeft__.x:
            dy = root.y
            while dy < self.__size__.y + self.__topLeft__.y:
                if mapMatrix[dx][dy] == BasicLabyrinth.ROOM_SPACE:
                    points.append(CustomVector3D(dx, dy))
                dy += 2
            dx += 2
        return points

    def spawnObstacles(self, mapMatrix: list, path:str, number:int):
        
        self.__numberOfObstacles__ = number
        self.__pathToObstacles__ = path
        
        pointsSets = list()
        pointsSets.append(self.__collectPositions__(
            mapMatrix=mapMatrix, root=self.__topLeft__))
        pointsSets.append(self.__collectPositions__(
            mapMatrix=mapMatrix, root=CustomVector3D(self.__topLeft__.x + 1, self.__topLeft__.y)))
        pointsSets.append(self.__collectPositions__(
            mapMatrix=mapMatrix, root=CustomVector3D(self.__topLeft__.x, self.__topLeft__.y + 1)))
        pointsSets.append(self.__collectPositions__(
            mapMatrix=mapMatrix, root=CustomVector3D(self.__topLeft__.x + 1, self.__topLeft__.y + 1)))

        maxLen = len(pointsSets[0])
        longestList = pointsSets[0]
        for i in pointsSets:
            if len(i) > maxLen:
                maxLen = len(i)
                longestList = i

        objects = set()
        meshes = self.__collectMeshes__()
        while len(objects) < maxLen and len(objects) < self.__numberOfObstacles__:
            index = BasicLabyrinth.safeRand(0, len(longestList) - 1)
            objects.add(longestList[index])
            self.__spawnMesh__(
                meshes[BasicLabyrinth.safeRand(0, len(meshes) - 1)], longestList[index])
            longestList.remove(longestList[index])
            
            
            
###------------------------------ClassicalLabyrinth------------------------------------###

class Labyrinth(BasicLabyrinth):
    class Pipe:
        def __init__(self, id, root, map_matrix):
            self.id = id
            self.points = []

            self.points.append(root)
            map_matrix[root.x][root.y] = self.id
            list_of_potentioal_steps = self.get_next_step(root, map_matrix, 1)

            while len(list_of_potentioal_steps) > 0:
                next_point = list_of_potentioal_steps[random.randint(
                    1, len(list_of_potentioal_steps)) - 1]
                middle_point = CustomVector3D(
                    root.x + (next_point.x - root.x) // 2,
                    root.y + (next_point.y - root.y) // 2,
                    root.z + (next_point.z - root.z) // 2
                )
                self.points.append(middle_point)
                map_matrix[middle_point.x][middle_point.y] = self.id
                self.points.append(next_point)
                map_matrix[next_point.x][next_point.y] = self.id
                root = next_point
                list_of_potentioal_steps = self.get_next_step(
                    root, map_matrix, 1)

        def cut_the_wall(self, map_matrix: list) -> CustomVector3D:
            possible_neighbours = []
            for point in self.points:
                if point.x - 2 > 0:
                    if map_matrix[point.x - 1][point.y] == 0 and map_matrix[point.x - 2][point.y] > self.id:
                        possible_neighbours.append([point,
                                                    CustomVector3D(point.x - 2, point.y, point.z)])
                if point.x + 2 < len(map_matrix):
                    if map_matrix[point.x + 1][point.y] == 0 and map_matrix[point.x + 2][point.y] > self.id:
                        possible_neighbours.append([point,
                                                    CustomVector3D(point.x + 2, point.y, point.z)])
                if point.y - 2 > 0:
                    if map_matrix[point.x][point.y - 1] == 0 and map_matrix[point.x][point.y - 2] > self.id:
                        possible_neighbours.append([point,
                                                    CustomVector3D(point.x, point.y - 2, point.z)])
                if point.y + 2 < len(map_matrix[0]):
                    if map_matrix[point.x][point.y + 1] == 0 and map_matrix[point.x][point.y + 2] > self.id:
                        possible_neighbours.append([point,
                                                    CustomVector3D(point.x, point.y + 2, point.z)])
            if len(possible_neighbours) == 0:
                return CustomVector3D(-1, -1, -1)

            cut_position = random.randint(0, len(possible_neighbours) - 1)
            door = CustomVector3D(
                possible_neighbours[cut_position][0].x + (
                    possible_neighbours[cut_position][1].x - possible_neighbours[cut_position][0].x) // 2,
                possible_neighbours[cut_position][0].y + (
                    possible_neighbours[cut_position][1].y - possible_neighbours[cut_position][0].y) // 2,
                possible_neighbours[cut_position][0].z + (
                    possible_neighbours[cut_position][1].z - possible_neighbours[cut_position][0].z) // 2
            )
            map_matrix[door.x][door.y] = self.id

            return possible_neighbours[cut_position][1]

        def is_yours(self, point: CustomVector3D):
            for i in self.points:
                if i.x == point.x and i.y == point.y and i.z == point.z:
                    return True
            return False

        def merge(self, another_pipe_points: list, map_matrix: list):
            for i in another_pipe_points:
                self.points.append(i)
                map_matrix[i.x][i.y] = self.id

        def get_next_step(self, root: CustomVector3D, map_matrix: list, free_point: int):
            potential_doores_list = []

            if root.x - 2 > 0:
                if map_matrix[root.x - 1][root.y] == 0 and map_matrix[root.x - 2][root.y] == free_point:
                    potential_doores_list.append(
                        CustomVector3D(root.x - 2, root.y, root.z))
            if root.x + 2 < len(map_matrix):
                if map_matrix[root.x + 1][root.y] == 0 and map_matrix[root.x + 2][root.y] == free_point:
                    potential_doores_list.append(
                        CustomVector3D(root.x + 2, root.y, root.z))
            if root.y - 2 > 0:
                if map_matrix[root.x][root.y - 1] == 0 and map_matrix[root.x][root.y - 2] == free_point:
                    potential_doores_list.append(
                        CustomVector3D(root.x, root.y - 2, root.z))
            if root.y + 2 < len(map_matrix[0]):
                if map_matrix[root.x][root.y + 1] == 0 and map_matrix[root.x][root.y + 2] == free_point:
                    potential_doores_list.append(
                        CustomVector3D(root.x, root.y + 2, root.z))
            return potential_doores_list

    def __init__(self, width, length, seed: int):
        BasicLabyrinth.__init__(self, seed)
        
        self.width = width + (width + 1) % 2
        self.length = length + (length + 1) % 2
        self.__map_matrix__ = [
            [0 for x in range(self.width)] for y in range(self.length)]
        x_counter = 1
        y_counter = 1
        free_points_list = []
        while x_counter < self.length:
            if x_counter % 2 == 1:
                while y_counter < self.width:
                    if y_counter % 2 == 1:
                        self.__map_matrix__[x_counter][y_counter] = 1
                        free_points_list.append(
                            CustomVector3D(x_counter, y_counter, 0))
                    y_counter += 1
                y_counter = 0
            x_counter += 1

        pipes = []
        while len(free_points_list) > 0:
            start_point_number = random.randint(1, len(free_points_list)) - 1
            tmp_point = free_points_list[start_point_number]
            if self.__map_matrix__[tmp_point.x][tmp_point.y] == 1:
                pipes.append(Labyrinth.Pipe(
                    len(pipes) + 3, free_points_list[start_point_number], self.__map_matrix__))
            del free_points_list[start_point_number]
        point = pipes[0].cut_the_wall(self.__map_matrix__)

        while len(pipes) > 1:
            for pipe in pipes:
                if pipe.is_yours(point):
                    pipes[0].merge(pipe.points, self.__map_matrix__)
                    pipes.remove(pipe)
                    break
            point = pipes[0].cut_the_wall(self.__map_matrix__)
        
        for x in range(self.length):
            for y in range(self.width):
                if self.__map_matrix__[x][y] == pipes[0].id:
                    self.__map_matrix__[x][y] = BasicLabyrinth.ROOM_SPACE
                else:
                    self.__map_matrix__[x][y] = BasicLabyrinth.WALL_SPACE
                    

    def name(self):
        return BasicLabyrinth.name(self) + "_Labyrinth"

###------------------------------------InvertedLabyrinth-----------------------------------------------###

class InvertedLabyrinth(Labyrinth):
    def __init__(self, width, length, seed: int):
        Labyrinth.__init__(self, width, length, seed)
        x_counter = 0
        while x_counter < self.length:
            y_counter = 0
            while y_counter < self.width:
                if self.__map_matrix__[x_counter][y_counter] != BasicLabyrinth.WALL_SPACE:
                    self.__map_matrix__[x_counter][y_counter] = BasicLabyrinth.WALL_SPACE
                else:
                    self.__map_matrix__[x_counter][y_counter] = BasicLabyrinth.ROOM_SPACE
                y_counter += 1
            x_counter += 1


###------------------------------------Rooms1-----------------------------------------------###

class Rooms1 (BasicLabyrinth):

    class SettingsStorage:
        maxRoomSize: CustomVector3D
        minRoomSize: CustomVector3D
        roomsCount: int
        mapSize: CustomVector3D
        roomsX: int
        roomsY: int
        numberOfObstacles = 10
        pathToMeshes = "./ExampleFurneture"

    class Room (ObstacleRoom):
        size: CustomVector3D
        leftTop: CustomVector3D
        id: int

        def __init__(self, size: CustomVector3D, root: CustomVector3D):
            ObstacleRoom.__init__(self=self, topLeft=root, size=size)
            self.size = size
            self.leftTop = root

        def paint(self, map: list):
            x1 = self.leftTop.x
            y1 = self.leftTop.y

            x2 = x1 + self.size.x - 1
            y2 = y1 + self.size.y - 1

            for i in range(x1+1, x2):
                for j in range(y1+1, y2):
                    map[i][j] = BasicLabyrinth.ROOM_SPACE

            for i in range(x1, x2+1):
                map[i][y1] = BasicLabyrinth.WALL_SPACE
                map[i][y2] = BasicLabyrinth.WALL_SPACE

            for i in range(y1, y2+1):
                map[x1][i] = BasicLabyrinth.WALL_SPACE
                map[x2][i] = BasicLabyrinth.WALL_SPACE

        def getCenter(self) -> CustomVector3D:
            x = (self.size.x+1)//2 + self.leftTop.x
            y = (self.size.y+1)//2 + self.leftTop.y
            return CustomVector3D(x, y)

    class Coridor:

        class SubCoridor:
            A: CustomVector3D
            B: CustomVector3D

            def __init__(self, start, end):
                self.A = start
                self.B = end

            def paint(self, map: list):

                delta = 0
                y = self.A.y
                x = self.A.x
                if self.A.x == self.B.x:
                    if self.A.y > self.B.y:
                        delta = -1
                    else:
                        delta = 1
                    while y != self.B.y:
                        # print("x:",x,",y:",y)
                        y += delta
                        map[x][y] = BasicLabyrinth.CORIDOR_SPACE
                        if x != 0 and map[x-1][y] == BasicLabyrinth.EMPTY_SPACE:
                            map[x-1][y] = BasicLabyrinth.WALL_SPACE
                        if x + 1 < len(map) and map[x+1][y] == BasicLabyrinth.EMPTY_SPACE:
                            map[x+1][y] = BasicLabyrinth.WALL_SPACE
                else:
                    if self.A.x > self.B.x:
                        delta = -1
                    else:
                        delta = 1
                    while x != self.B.x:
                        x += delta
                        map[x][y] = BasicLabyrinth.CORIDOR_SPACE
                        if y != 0 and map[x][y-1] == BasicLabyrinth.EMPTY_SPACE:
                            map[x][y-1] = BasicLabyrinth.WALL_SPACE
                        if y  + 1 < len(map[x]) and map[x][y+1] == BasicLabyrinth.EMPTY_SPACE:
                            map[x][y+1] = BasicLabyrinth.WALL_SPACE



        A: SubCoridor
        B: SubCoridor

        def __init__(self, start: CustomVector3D, end: CustomVector3D):
            d_x = end.x - start.x
            d_y = end.y - start.y

            randFlag = BasicLabyrinth.__safe_randint__(0, 1)
            if randFlag == 1:
                corner = CustomVector3D(start.x + d_x, start.y)
            else:
                corner = CustomVector3D(start.x, start.y + d_y)
            self.A = self.SubCoridor(start, corner)
            self.B = self.SubCoridor(corner, end)

        def paint(self, map: list):
            self.A.paint(map)
            self.B.paint(map)

    rooms = list()
    coridors = list()

    def __init__(self, maxRoomSize: CustomVector3D, minRoomSize: CustomVector3D, roomsCount: int, seed: int, roomsX=-1, roomsY=-1):

        if roomsX == -1:
            roomsX = roomsCount

        if roomsY == -1:
            roomsY = roomsCount

        maxPossibleWidth = maxRoomSize.x * roomsX  # X
        maxPossibleLength = maxRoomSize.y * roomsY  # Y
        BasicLabyrinth.__init__(self, seed=seed) 
        Rooms1.SettingsStorage.roomsCount = roomsCount
        Rooms1.SettingsStorage.minRoomSize = minRoomSize
        Rooms1.SettingsStorage.maxRoomSize = maxRoomSize
        Rooms1.SettingsStorage.mapSize = CustomVector3D(
            x=maxPossibleWidth, y=maxPossibleLength)
        Rooms1.SettingsStorage.roomsX = roomsX
        Rooms1.SettingsStorage.roomsY = roomsY

        self.__map_matrix__ = list()
        for x in range(0, Rooms1.SettingsStorage.mapSize.x):
            self.__map_matrix__.append(list())
            for y in range(0, Rooms1.SettingsStorage.mapSize.y):
                self.__map_matrix__[x].append(Rooms1.EMPTY_SPACE)

        self.__build__()

    def __build__(self):
        cellMap = list()
        x = self.SettingsStorage.roomsX
        y = self.SettingsStorage.roomsY

        for i in range(x):
            cellMap.append(list())
            for j in range(y):
                cellMap[i].append(0)

        while len(self.rooms) < self.SettingsStorage.roomsCount:
            x_ = self.__safe_randint__(0, x-1)
            y_ = self.__safe_randint__(0, y-1)
            if cellMap[x_][y_] == BasicLabyrinth.EMPTY_SPACE:
                room = self.__spawnRoomInCell__(CustomVector3D(x_, y_))
                room.paint(self.__map_matrix__)
                self.rooms.append(room)
                cellMap[x_][y_] = BasicLabyrinth.ROOM_SPACE      

        self.__addCoridors__()
        self.__verifyPainting__()
        pass

    def __spawnObstacles__(self):
        for i in self.rooms:
            i.spawnObstacles(self.__map_matrix__, Rooms1.SettingsStorage.pathToMeshes, Rooms1.SettingsStorage.numberOfObstacles)

    def __spawnRoomInCell__(self, cell: CustomVector3D) -> Room:
        xSize = self.__safe_randint__(self.SettingsStorage.minRoomSize.x,
                                      self.SettingsStorage.maxRoomSize.x)
        ySize = self.__safe_randint__(self.SettingsStorage.minRoomSize.y,
                                      self.SettingsStorage.maxRoomSize.y)

        xRoot = self.__safe_randint__(
            0, self.SettingsStorage.maxRoomSize.x - xSize)
        yRoot = self.__safe_randint__(
            0, self.SettingsStorage.maxRoomSize.y - ySize)

        xRoot += cell.x * self.SettingsStorage.maxRoomSize.x
        yRoot += cell.y * self.SettingsStorage.maxRoomSize.y

        room = self.Room(root=CustomVector3D(xRoot, yRoot),
                         size=CustomVector3D(xSize, ySize))

        return room

    def __addCoridors__(self):

        backUpRooms = self.rooms.copy()

        while len(backUpRooms) > 1:
            start = backUpRooms[0].getCenter()
            targetIndex = self.__safe_randint__(1, len(backUpRooms)-1)
            end = backUpRooms[targetIndex].getCenter()
            coridor = Rooms1.Coridor(start, end)
            print("start:", start, "end:", end)
            coridor.paint(self.__map_matrix__)
            self.coridors.append(coridor)
            backUpRooms.remove(backUpRooms[0])

    
    def spawnObstacles(self, number:int, path:str):
        Rooms1.SettingsStorage.numberOfObstacles = number
        Rooms1.SettingsStorage.pathToMeshes = path
        self.__spawnObstacles__() 


###------------------------------------Rooms2-----------------------------------------------###

class Rooms2 (BasicLabyrinth):
    
    class SettingsStorage:
        maxRoomSize: CustomVector3D
        minRoomSize: CustomVector3D
        roomsCount: int
        roomsInRow: int
        mapSize: CustomVector3D
        numberOfObstacles= 10
        pathToMeshes="./ExampleFurneture"

    class Room (ObstacleRoom):
        size: CustomVector3D
        leftTop: CustomVector3D
        id: int

        def __init__(self, size: CustomVector3D, root: CustomVector3D):
            ObstacleRoom.__init__(self=self, topLeft=root, size=size)
            self.size=size
            self.leftTop=root

        def paint(self, map: list):
            x1 = self.leftTop.x
            y1 = self.leftTop.y

            x2 = x1 + self.size.x - 1
            y2 = y1 + self.size.y - 1

            for i in range(x1+1,x2):
                for j in range(y1+1,y2):
                    map[i][j] = BasicLabyrinth.ROOM_SPACE

            for i in range(x1,x2+1):
                map[i][y1] = BasicLabyrinth.WALL_SPACE
                map[i][y2] = BasicLabyrinth.WALL_SPACE

            for i in range(y1,y2+1):
                map[x1][i] = BasicLabyrinth.WALL_SPACE
                map[x2][i] = BasicLabyrinth.WALL_SPACE
        
        def getRandomPoint(self)->CustomVector3D:
            x = BasicLabyrinth.safeRand(1, self.size.x - 2)
            y = BasicLabyrinth.safeRand(1, self.size.y - 2)
            x += self.leftTop.x
            y += self.leftTop.y
            return CustomVector3D(x,y)

    class Coridor:
        A: CustomVector3D
        B: CustomVector3D

        def __init__(self, start, end):
            self.A = start
            self.B = end

        def paint(self, map: list):
            delta = 0
            if self.A.x > self.B.x:
                delta = -1
            else:
                delta = 1
            
            x = self.A.x
            y = self.A.y
            while x != self.B.x:
                map[x][y] = Rooms2.CORIDOR_SPACE
                if map[x][y + 1] == Rooms2.EMPTY_SPACE:
                    map[x][y + 1] = Rooms2.WALL_SPACE
                if map[x][y - 1] == Rooms2.EMPTY_SPACE:
                    map[x][y - 1] = Rooms2.WALL_SPACE
                x += delta


    topRooms = list()
    botRooms = list()
    coridors = list()
    mainCoridor : Room

    def __init__(self, maxRoomSize: CustomVector3D, minRoomSize: CustomVector3D, roomsCount: int, roomsInRow = -1, seed = 0, mainCoridorWidth = 3):
        maxPossibleWidth = maxRoomSize.x * 2 + mainCoridorWidth # X
        if roomsInRow == -1:
            roomsInRow = roomsCount
        maxPossibleLength = maxRoomSize.y * roomsInRow  # Y
        BasicLabyrinth.__init__(self, seed=seed)  # have no Idea how map is represented there
        Rooms2.SettingsStorage.roomsCount = roomsCount
        Rooms2.SettingsStorage.minRoomSize = minRoomSize
        Rooms2.SettingsStorage.maxRoomSize = maxRoomSize
        Rooms2.SettingsStorage.mapSize = CustomVector3D(
            x=maxPossibleWidth, y=maxPossibleLength)
        Rooms2.SettingsStorage.mainCoridorWidth = mainCoridorWidth
        Rooms2.SettingsStorage.roomsInRow = roomsInRow

        self.__map_matrix__ = list()
        for x in range(0, Rooms2.SettingsStorage.mapSize.x):
            self.__map_matrix__.append(list())
            for y in range(0, Rooms2.SettingsStorage.mapSize.y):
                self.__map_matrix__[x].append(Rooms2.WALL_SPACE)
        pass

        self.__build__()

    def __build__(self):
        cellMap = list()
        x = 3
        y = self.SettingsStorage.roomsInRow

        for i in range(x):
            cellMap.append(list())
            for j in range(y):
                if i == 1: 
                    cellMap[i].append(Rooms2.ROOM_SPACE)
                else:
                    cellMap[i].append(Rooms2.EMPTY_SPACE)

        while len(self.botRooms) + len(self.topRooms) < self.SettingsStorage.roomsCount:
            x_ = 0
            y_ = self.__safe_randint__(0, y-1)
            isTop = self.__safe_randint__(0, 1) == 0
            if isTop:
                x_ = 0
            else:
                x_ = 2

            if cellMap[x_][y_] == BasicLabyrinth.EMPTY_SPACE:
                room = self.__spawnRoomInCell__(CustomVector3D(x_, y_))
                room.paint(self.__map_matrix__)
                if isTop:
                    self.topRooms.append(room)
                else:
                    self.botRooms.append(room)
                cellMap[x_][y_] = BasicLabyrinth.ROOM_SPACE

        
        self.__spawnMainCoridor__()
        self.__addCoridors__()    
        self.__verifyPainting__()
        pass

    def __spawnMainCoridor__(self):
        x_ = self.SettingsStorage.maxRoomSize.x
        y_ = 0
        root = CustomVector3D(x_, y_)
        size = CustomVector3D(self.SettingsStorage.mainCoridorWidth, self.SettingsStorage.mapSize.y)
        self.mainCoridor = Rooms2.Room(root=root, size=size)
        self.mainCoridor.paint(self.__map_matrix__)
    
    def spawnObstacles(self, path, number):
        for i in self.topRooms:
            i.spawnObstacles(self.__map_matrix__, path, number)

        for i in self.botRooms:
            i.spawnObstacles(self.__map_matrix__, path, number)

    def __spawnRoomInCell__(self, cell: CustomVector3D) -> Room:
        xSize = self.__safe_randint__(self.SettingsStorage.minRoomSize.x,
                              self.SettingsStorage.maxRoomSize.x)
        ySize = self.__safe_randint__(self.SettingsStorage.minRoomSize.y,
                              self.SettingsStorage.maxRoomSize.y)

        xRoot = self.__safe_randint__(0, self.SettingsStorage.maxRoomSize.x - xSize)
        yRoot = self.__safe_randint__(0, self.SettingsStorage.maxRoomSize.y - ySize)

        if cell.x == 0:
            xRoot += 0
        else:
            xRoot += Rooms2.SettingsStorage.maxRoomSize.x + Rooms2.SettingsStorage.mainCoridorWidth
        yRoot += cell.y * self.SettingsStorage.maxRoomSize.y

        room = self.Room(root=CustomVector3D(xRoot, yRoot),
                         size=CustomVector3D(xSize, ySize))

        return room

    def __addCoridors__(self):
        for i in self.topRooms:
            A = i.getRandomPoint()
            B = CustomVector3D(self.mainCoridor.leftTop.x + 1, A.y)
            coridor = Rooms2.Coridor(A, B)
            self.coridors.append(coridor)
            coridor.paint(self.__map_matrix__)

        for i in self.botRooms:
            A = i.getRandomPoint()
            B = CustomVector3D(self.mainCoridor.leftTop.x + 1, A.y)
            coridor = Rooms2.Coridor(A, B)
            self.coridors.append(coridor)
            coridor.paint(self.__map_matrix__)


###------------------------------LabyrinthOperator------------------------------------------###


class WT_OT_LabyrinthOperator(bpy.types.Operator):
    """
    This is a classical labyrinth.
    It's better to use odd numbers
    as sizes of construction.
    
    Due to how the algorythm works,
    any even values will be turned into 
    the closest odd number by adding 1.
    
    Random's seed will be used in initiating
    random algorythm.
    
    """
    bl_idname = "wm.labyrinth_operator"
    bl_label = "Labyrinth settings"
    
    x_text : bpy.props.IntProperty(name = "Size by X", default = 21, min=3)
    y_text : bpy.props.IntProperty(name = "Size by Y", default = 21, min=3)
    invert_construction_bool: bpy.props.BoolProperty(name="Invert", default = False) 
    seed_text : bpy.props.IntProperty(name = "Random's seed", default = 0)
    use_time_as_seed_bool: bpy.props.BoolProperty(name="Use current time as a seed", default = True) 
    
    
    def draw(self, context):
        layout = self.layout

        layout.prop(self, "x_text")
        layout.prop(self, "y_text")
        row = layout.row()
        row.prop(self, "seed_text")
        row.prop(self, "use_time_as_seed_bool")
        layout.prop(self, "invert_construction_bool")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        x = self.x_text
        y = self.y_text
        seed : 0
        
        if self.use_time_as_seed_bool == True:
            seed = time.time()
        else:
            seed = self.seed_text
        
        lab : BasicLabyrinth
        if self.invert_construction_bool == True:
            lab = InvertedLabyrinth(y, x, seed)
        else:
            lab = Labyrinth(y, x, seed)

            
        lab.print_in_console()
        lab.spawn()
        
        return {'FINISHED'}
    
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

###------------------------------Rooms1Operator------------------------------------------###
class WT_OT_Rooms1Operator(bpy.types.Operator):
    
    """
    This construction is a group of randomly placed rooms,
    connected together in one system by coridores.
    
    Random's seed will be used in initiating
    random algorythm.
    
    """
    
    bl_idname = "wm.rooms1_operator"
    bl_label = "Rooms and coridors"

    
    max_room_x_text : bpy.props.IntProperty(name = "X", default = 10, min=3)
    max_room_y_text : bpy.props.IntProperty(name = "Y", default = 10, min=3)
    
    min_room_x_text : bpy.props.IntProperty(name = "X", default = 5, min=3)
    min_room_y_text : bpy.props.IntProperty(name = "Y", default = 5, min=3)
    
    rooms_amount_text : bpy.props.IntProperty(name = "N", default = 5, min=1)
    rooms_amount_x_text : bpy.props.IntProperty(name = "X", default = 5, min=1)
    rooms_amount_y_text : bpy.props.IntProperty(name = "Y", default = 5, min=1)
    
        
    seed_text : bpy.props.IntProperty(name = "Random's seed", default = 0)
    
    obstacle_dir_path_text : bpy.props.StringProperty(name = "", default = "", subtype="DIR_PATH")
    add_obstackes_bool: bpy.props.BoolProperty(name="Enable obstacles", default = False) 
    obstacle_per_room_amount_text : bpy.props.IntProperty(name = "Obstacles", default = 5, min=0)
    
    use_time_as_seed_bool: bpy.props.BoolProperty(name="Use current time as a seed", default = True) 
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        
        row = col.row()
        row.label(text="Maximum room size:")
        row = col.row()
        row.prop(self, "max_room_x_text")
        row.prop(self, "max_room_y_text")
        
        row = col.row()
        row.label(text="Minimum room size:")
        row = col.row()
        row.prop(self, "min_room_x_text")
        row.prop(self, "min_room_y_text")
        
        row = col.row()
        row.label(text="Number of rooms:")
        row = col.row()
        row.prop(self, "rooms_amount_text")
        
        row = col.row()
        row.label(text="Maximum number of rooms by:")
        row = col.row()
        row.prop(self, "rooms_amount_x_text")
        row.prop(self, "rooms_amount_y_text")
        
        row = col.row()
        row.label(text="Randomizer settings:")
        row = col.row()
        row.prop(self, "seed_text")
        row.prop(self, "use_time_as_seed_bool")  

        row = col.row()
        row.label(text="")
        row = col.row()
        row.prop(self, "obstacle_per_room_amount_text")
        row.prop(self, "add_obstackes_bool")
        row = col.row()
        row.label(text="Path to obstacles:")
        row.prop(self, "obstacle_dir_path_text")
        
        
    def execute(self, context):
        roomMax = CustomVector3D(self.max_room_x_text, self.max_room_y_text)
        roomMin = CustomVector3D(self.min_room_x_text, self.min_room_y_text)
        
        N = self.rooms_amount_text
        X = self.rooms_amount_x_text
        Y = self.rooms_amount_y_text
        
        seed : int()
        if self.use_time_as_seed_bool == True:
            seed = time.time()
        else:
            seed = self.seed_text
        
        if X * Y < N:
            X = -1
            Y = -1
            
        lab = Rooms1(roomMax, roomMin, N, seed, X, Y)
        lab.spawn()
        if self.add_obstackes_bool == True and self.obstacle_per_room_amount_text > 0:
            lab.spawnObstacles(number = self.obstacle_per_room_amount_text, path = self.obstacle_dir_path_text)
            
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


###------------------------------Rooms2Operator------------------------------------------###
class WT_OT_Rooms2Operator(bpy.types.Operator):
        
    """
    This construction is a two groups of rooms,
    with a coridor between them.
    
    Rooms are connected only with coridor.
    Ti's called a main coridor.
    
    Random's seed will be used in initiating
    random algorythm.
    
    """
    
    bl_idname = "wm.rooms2_operator"
    bl_label = "Rooms and coridor settings"
    
    max_room_x_text : bpy.props.IntProperty(name = "X", default = 10, min=3)
    max_room_y_text : bpy.props.IntProperty(name = "Y", default = 10, min=3)
    
    min_room_x_text : bpy.props.IntProperty(name = "X", default = 5, min=3)
    min_room_y_text : bpy.props.IntProperty(name = "Y", default = 5, min=3)
    
    main_coridor_width_text : bpy.props.IntProperty(default = 5, min=3)
    rooms_amount_text : bpy.props.IntProperty(name = "N", default = 15, min=1)
    rooms_in_a_row_amount_text : bpy.props.IntProperty(name = "K", default = 5, min=1)
        
    seed_text : bpy.props.IntProperty(name = "Random's seed", default = 0)
    use_time_as_seed_bool: bpy.props.BoolProperty(name="Use current time as a seed", default = True) 
    
    obstacle_dir_path_text : bpy.props.StringProperty(name = "Path to obstacles", default = "", subtype="DIR_PATH")
    add_obstackes_bool: bpy.props.BoolProperty(name="Enable obstacles", default = False) 
    obstacle_per_room_amount_text : bpy.props.IntProperty(name = "Obstacles", default = 5, min=0)
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        
        row = col.row()
        row.label(text="Maximum room size:")
        row = col.row()
        row.prop(self, "max_room_x_text")
        row.prop(self, "max_room_y_text")
        
        
        row = col.row()
        row.label(text="Minimum room size:")
        row = col.row()
        row.prop(self, "min_room_x_text")
        row.prop(self, "min_room_y_text")
        
        
        row = col.row()
        row.label(text="Main coridor width:")
        row = col.row()
        row.prop(self, "main_coridor_width_text")
        
        row = col.row()
        row.label(text="Number of rooms:")
        row = col.row()
        row.prop(self, "rooms_amount_text")
        
        row = col.row()
        row.label(text="Maximum number of rooms in a row:")
        row = col.row()
        row.prop(self, "rooms_in_a_row_amount_text")
                
        row = col.row()
        row.label(text="Randomizer settings:")
        row = col.row()
        row.prop(self, "seed_text")
        row.prop(self, "use_time_as_seed_bool")  

        row = col.row()
        row.label(text="")
        row = col.row()
        row.prop(self, "obstacle_per_room_amount_text")
        row.prop(self, "add_obstackes_bool")
        row = col.row()
        row.label(text="Path to obstacles:")
        row.prop(self, "obstacle_dir_path_text")

    def execute(self, context):
        roomMax = CustomVector3D(self.max_room_x_text, self.max_room_y_text)
        roomMin = CustomVector3D(self.min_room_x_text, self.min_room_y_text)
        
        N = self.rooms_amount_text
        K = self.rooms_in_a_row_amount_text
        W = self.main_coridor_width_text
        
        seed : int()
        if self.use_time_as_seed_bool == True:
            seed = time.time()
        else:
            seed = self.seed_text
        
        if K * 2 < N:
            K = -1
            
        lab = Rooms2(roomMax, roomMin, N, K, seed, W)
        lab.spawn()
        if self.add_obstackes_bool == True and self.obstacle_per_room_amount_text > 0:
            lab.spawnObstacles(number = self.obstacle_per_room_amount_text, path = self.obstacle_dir_path_text)
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
###------------------------------RoomWithObstacles------------------------------------------###
class WT_OT_RoomWithObstaclesOperator(bpy.types.Operator):
    """
    Just a simple closed area filled with
    randomly generated obstacles.
    You also may add your own obstacles
    if you want to.
    
    Random's seed will be used in initiating
    random algorythm.
    
    """
    
    bl_idname = "wm.room_with_obstacles_operator"
    bl_label = "Room with obstacles settings"
    
    room_x_text : bpy.props.IntProperty(name = "X", default = 30)
    room_y_text : bpy.props.IntProperty(name = "Y", default = 30)
    
    obstacles_amount_text : bpy.props.IntProperty(name = "Number of obstacles", default = 10)
        
    seed_text : bpy.props.IntProperty(name = "Random's seed", default = 0)
    use_time_as_seed_bool: bpy.props.BoolProperty(name="Use current time as a seed", default = True) 
    
    genegrate_convex_obstacles_bool: bpy.props.BoolProperty(name="Generate convex obstacles", default = False) 
    genegrate_concave_obstacles_bool: bpy.props.BoolProperty(name="Generate concave obstacles", default = False) 
    
    use_custom_obstacles_bool: bpy.props.BoolProperty(name="Use custom obstacles", default = False) 
    obstacle_dir_path_text : bpy.props.StringProperty(name = "Path to obstacles", default = "", subtype="DIR_PATH")
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        
        row = col.row()
        row.label(text="Room size:")
        row = col.row()
        row.prop(self, "room_x_text")
        row.prop(self, "room_y_text")
        
        row = col.row()
        row.prop(self, "obstacles_amount_text")
                
        row = col.row()
        row.prop(self, "genegrate_convex_obstacles_bool")
        row = col.row()
        row.prop(self, "genegrate_concave_obstacles_bool")
        
        row = col.row()
        row.label(text="Randomizer settings:")
        row = col.row()
        row.prop(self, "seed_text")
        row.prop(self, "use_time_as_seed_bool")  

        row = col.row()
        row.label(text="")
        row = col.row()
        row.prop(self, "obstacle_dir_path_text")
        row = col.row()
        row.prop(self, "use_custom_obstacles_bool")

    def execute(self, context):
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

###------------------------------ExportToMesh------------------------------------------###
class WT_OT_ExportToMeshOperator(bpy.types.Operator):
    """
    Will convert a scene with all content into a Gazebo mesh.
    
    """
    bl_label = "Export to the Gazebo mesh"
    bl_idname = "wm.export_to_mesh_operator"

    file_name: bpy.props.StringProperty(name="Mesh name")
    filepath: bpy.props.StringProperty(subtype="DIR_PATH")

    def execute(self, context):        
        path = self.filepath + "/" + self.file_name
        os.mkdir(path)
        config = open(path+"/model.config", 'w')
        config_str = "<?xml version=\"1.0\"?><model><name>"+self.file_name+"</name>" + \
            "<version>1.0</version><sdf version=\"1.5\">model.sdf</sdf>" + \
            "<description>" + self.file_name + "</description></model>"
        config.write(config_str)
        config.flush()
        config.close()

        mesh_name = self.file_name + "/" + self.file_name + ".stl"
        sdf_file = open(path+"/model.sdf", 'w')
        sdf_str = "<?xml version=\'1.0\' ?><sdf version=\'1.6\'><model name=\'"+self.file_name+"\'>" + \
            "<static>true</static><link name=\'link\'><pose>0 0 0 0 0 0</pose>" +\
            "<collision name=\'collision\'><geometry><mesh><uri>model://" + \
            mesh_name + "</uri>" + \
            "</mesh></geometry></collision><visual name=\'visual\'>" +\
            "<geometry><mesh><uri>model://" + mesh_name + "</uri>" + \
            "</mesh></geometry></visual></link></model></sdf>"
        sdf_file.write(sdf_str)
        sdf_file.flush()
        sdf_file.close()
        bpy.ops.export_mesh.stl(filepath=path+"/"+self.file_name+".stl", batch_mode="OFF")

        self.file_name = ""
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    @classmethod
    def poll(cls, context):
        return context.object is not None

###------------------------------MainPanel------------------------------------------###

class WT_OT_MainPanel(bpy.types.Panel):
    bl_idname = "wm.main_panel"
    bl_label = "Mazer Main Menue"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        row = layout.row() 
        row.operator("wm.labyrinth_operator", text="Classical labyrinth") 
        row = layout.row() 
        row.operator("wm.rooms1_operator", text="Rooms") 
        row = layout.row() 
        row.operator("wm.rooms2_operator", text="Rooms and coridor") 
        row = layout.row() 
        row.operator("wm.room_with_obstacles_operator", text="Room with obstacles") 
        row = layout.row() 
        row.operator("wm.export_to_mesh_operator", text="Export to the Gazebo mesh") 

###------------------------------------------------------------------------###    
    

bl_info = {
    "name" : "MazerGUI",
    "author" : "Limberjack",
    "description" : "Mazer GUI",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

def register():
    bpy.utils.register_class(WT_OT_MainPanel)
    bpy.utils.register_class(WT_OT_LabyrinthOperator)
    bpy.utils.register_class(WT_OT_Rooms1Operator)
    bpy.utils.register_class(WT_OT_Rooms2Operator)
    bpy.utils.register_class(WT_OT_RoomWithObstaclesOperator)
    bpy.utils.register_class(WT_OT_ExportToMeshOperator)
    

def unregister():
    bpy.utils.unregister_class(WT_OT_MainPanel)
    bpy.utils.unregister_class(WT_OT_LabyrinthOperator)
    bpy.utils.unregister_class(WT_OT_Rooms1Operator)
    bpy.utils.unregister_class(WT_OT_Rooms2Operator)
    bpy.utils.unregister_class(WT_OT_RoomWithObstaclesOperator)
    bpy.utils.unregister_class(WT_OT_ExportToMeshOperator)

if __name__ == "__main__":
    register()