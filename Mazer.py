import random

import bpy
import logging
import os
import time


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
    ROOM_SPACE = 1
    EMPTY_SPACE = 0
    WALL_SPACE = 2

    cube_width = 1.0
    cube_length = 1.0
    cube_height = 1.0

    def __init__(self, width, length, seed: int):
        self.width = width + (width + 1) % 2
        self.length = length + (length + 1) % 2
        self.seed = seed
        self.map_matrix = [
            [0 for x in range(self.width)] for y in range(self.length)]
        random.seed(seed)

    def spawn_cube(self, root_point: CustomVector3D, dist_point: CustomVector3D):
        diag_vector = CustomVector3D()
        diag_vector.x = dist_point.x - root_point.x + 1
        diag_vector.y = dist_point.y - root_point.y + 1
        diag_vector.z = dist_point.z - root_point.z + 1
        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False,
                                        location=(root_point.x + diag_vector.x / 2, root_point.y + diag_vector.y / 2,
                                                  root_point.z + diag_vector.z / 2),
                                        rotation=(0, 0, 0), scale=(diag_vector.x, diag_vector.y, diag_vector.z))

    def name(self):
        result_str = "seed_" + str(self.seed)
        return result_str

    def __spawn_wall__(self, wall_list: list):
        if len(wall_list) == 0:
            return

        point_a = wall_list[0]
        point_b = wall_list[len(wall_list)-1]
        point_b.z = 4 + 1.5

        diag_vector = CustomVector3D()
        diag_vector.x = point_b.x - point_a.x + 1
        diag_vector.y = point_b.y - point_a.y + 1
        diag_vector.z = point_b.z - point_a.z + 1

        if len(wall_list) == 1:
            bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False,
                                            location=(point_a.x + diag_vector.x / 2, point_a.y + diag_vector.y / 2,
                                                      4),
                                            rotation=(0, 0, 0), scale=(1, 1, 5))
            return

        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False,
                                        location=(point_a.x + diag_vector.x / 2, point_a.y + diag_vector.y / 2,
                                                  point_a.z + diag_vector.z / 2),
                                        rotation=(0, 0, 0), scale=(diag_vector.x, diag_vector.y, diag_vector.z))

    def spawn(self):
        self.length = len(self.map_matrix)
        self.width = len(self.map_matrix[0])
        self.print_in_console()
        bottom_root_point = CustomVector3D(0, 0, 0)
        bottom_target_point = CustomVector3D(
            self.length - 1, self.width - 1, 0.5)
        self.spawn_cube(bottom_root_point, bottom_target_point)

        if(self.map_matrix[0][0] == self.WALL_SPACE):

            point_a = CustomVector3D(0, 0, 1.5)
            point_b = CustomVector3D(self.length-1, 0, 4 + 1.5)
            self.spawn_cube(point_a, point_b)

            point_a = CustomVector3D(0, self.width-1, 1.5)
            point_b = CustomVector3D(self.length-1, self.width-1, 4 + 1.5)
            self.spawn_cube(point_a, point_b)

            point_a = CustomVector3D(0, 1, 1.5)
            point_b = CustomVector3D(0, self.width-2, 4 + 1.5)
            self.spawn_cube(point_a, point_b)

            point_a = CustomVector3D(self.length-1, 1, 1.5)
            point_b = CustomVector3D(self.length-1, self.width-2, 4 + 1.5)
            self.spawn_cube(point_a, point_b)

#
        for x in range(0, self.length):
            horisontal_list = list()
            for y in range(0, self.width):
                if(self.map_matrix[x][y] == self.WALL_SPACE):
                    self.map_matrix[x][y] = -1
                    horisontal_list.append(CustomVector3D(x, y, 1.5))
                else:
                    if len(horisontal_list) > 1:
                        self.__spawn_wall__(horisontal_list)
                    else:
                        if len(horisontal_list) == 1:
                            point = horisontal_list[0]
                            self.map_matrix[point.x][point.y] = self.WALL_SPACE
                    horisontal_list = list()
            self.__spawn_wall__(horisontal_list)

        for y in range(0, self.width):
            vertical_list = list()
            for x in range(0, self.length):
                if self.map_matrix[x][y] == self.WALL_SPACE:
                    vertical_list.append(CustomVector3D(x, y, 1.5))
                else:
                    self.__spawn_wall__(vertical_list)
                    vertical_list = list()
            self.__spawn_wall__(vertical_list)

    def to_mesh(self, path: str, name: str, extention: str):
        path = path
        if os.path.exists(path):
            copy_number = 1
            new_path = path
            while os.path.exists(path):
                new_path = path + "(" + str(copy_number)+")"
            path = new_path

        os.mkdir(path)
        path = path + "/" + name
        config = open(path+"/model.config", 'w')
        config_str = "<?xml version=\"1.0\"?><model><name>test labyrinth</name>" + \
            "<version>1.0</version><sdf version=\"1.5\">model.sdf</sdf>" + \
            "<description>" + name + "</description></model>"
        config.write(config_str)
        config.flush()
        config.close()

        mesh_name = name + "/" + name + "." + extention
        sdf_file = open(path+"/model.sdf", 'w')
        sdf_str = "<?xml version=\'1.0\' ?><sdf version=\'1.6\'><model name=\'"+name+"\'>" + \
            "<static>true</static><link name=\'link\'><pose>0 0 0 0 0 0</pose>" +\
            "<collision name=\'collision\'><geometry><mesh><uri>model://" + \
            mesh_name + "</uri>" + \
            "</mesh></geometry></collision><visual name=\'visual\'>" +\
            "<geometry><mesh><uri>model://" + mesh_name + "</uri>" + \
            "</mesh></geometry></visual></link></model></sdf>"
        sdf_file.write(sdf_str)
        sdf_file.flush()
        sdf_file.close()
        pass

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
        print(len(self.map_matrix))
        for x in range(0, len(self.map_matrix)-1):
            for y in range(0, len(self.map_matrix[x])-1):
                if self.map_matrix[x][y] == self.WALL_SPACE:
                    print("▓▓", end='')
                elif self.map_matrix[x][y] == self.ROOM_SPACE:
                    print("..", end="")
                else:
                    print("  ", end="")
            print("")


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
        BasicLabyrinth.__init__(self, width, length, seed)
        x_counter = 1
        y_counter = 1
        free_points_list = []
        while x_counter < self.length:
            if x_counter % 2 == 1:
                while y_counter < self.width:
                    if y_counter % 2 == 1:
                        self.map_matrix[x_counter][y_counter] = 1
                        free_points_list.append(
                            CustomVector3D(x_counter, y_counter, 0))
                    y_counter += 1
                y_counter = 0
            x_counter += 1

        pipes = []
        while len(free_points_list) > 0:
            start_point_number = random.randint(1, len(free_points_list)) - 1
            tmp_point = free_points_list[start_point_number]
            if self.map_matrix[tmp_point.x][tmp_point.y] == 1:
                pipes.append(Labyrinth.Pipe(
                    len(pipes) + 3, free_points_list[start_point_number], self.map_matrix))
            del free_points_list[start_point_number]
        point = pipes[0].cut_the_wall(self.map_matrix)

        while len(pipes) > 1:
            for pipe in pipes:
                if pipe.is_yours(point):
                    pipes[0].merge(pipe.points, self.map_matrix)
                    pipes.remove(pipe)
                    break
            point = pipes[0].cut_the_wall(self.map_matrix)

    def name(self):
        return BasicLabyrinth.name(self) + "_Labyrinth"


class OfficeLabyrinth(BasicLabyrinth):
    class Room:
        def __init__(self, root: CustomVector3D, map: list):
            end_point = CustomVector3D(root.x, root.y)

            end_point.x = random.randint(root.x + 1, len(map) - 1)
            end_point.y = random.randint(root.y + 1, len(map[1]) - 1)

            wall_points = list()
            for i in range(root.x, end_point.x):
                map[i][root.y] = 0
                map[i][end_point.y] = 0

            for i in range(root.y, end_point.y):
                map[root.x][i] = 0
                map[end_point.x][i] = 0

    def __init__(self, width, length, seed: int):
        BasicLabyrinth.__init__(self, width, length, seed)
        for i in range(1, len(self.map_matrix) - 1):
            for j in range(1, len(self.map_matrix[i]) - 1):
                self.map_matrix[i][j] = 1

        room_number = self.__safe_randint__(
            1, self.width * self.length // (self.width + self.length))
        room_list = list()
        for i in range(room_number):
            next_room_root = self.__find_free_position()
            OfficeLabyrinth.Room(next_room_root, self.map_matrix)

        unmarked_points = list()

        for i in range(1, len(self.map_matrix) - 1):
            for j in range(1, len(self.map_matrix[i]) - 1):
                if self.map_matrix[i][j] != 0:
                    unmarked_points.append(CustomVector3D(i, j))

        marked_groups = list()

        id = 2
        while len(unmarked_points) != 0:
            new_group = list()
            self.__mark_neighbour_points__(
                unmarked_points[0], id, old_id=1, new_group=new_group)
            id += 1
            marked_groups.append(new_group.copy())
            while len(new_group) != 0:
                for i in range(len(unmarked_points)):
                    if len(new_group) > 0 and len(unmarked_points) > 0:
                        if new_group[0].x == unmarked_points[i].x and new_group[0].y == unmarked_points[i].y:
                            del unmarked_points[i]
                            del new_group[0]
                            break

        for i in range(len(marked_groups)):
            if len(marked_groups[i]) == 0:
                continue
            point_index = self.__safe_randint__(
                0, len(marked_groups[i]) - 1)
            selected_point = marked_groups[i][point_index]
            self.__spawn_cross__(selected_point)
        self.print_in_console()

    def __spawn_cross__(self, point: CustomVector3D):
        for i in range(point.x, len(self.map_matrix) - 1):
            if self.map_matrix[i][point.y] == 0 or self.map_matrix[i][point.y] == self.map_matrix[point.x][point.y]:
                self.map_matrix[i][point.y] = 1
            else:
                break

        for i in range(point.y, len(self.map_matrix[0]) - 1):
            if self.map_matrix[point.x][i] == 0 or self.map_matrix[point.x][i] == self.map_matrix[point.x][point.y]:
                self.map_matrix[point.x][i] = 1
            else:
                break

        i = point.x
        while i > 1:
            i -= 1
            if self.map_matrix[i][point.y] == 0 or self.map_matrix[i][point.y] == self.map_matrix[point.x][point.y]:
                self.map_matrix[i][point.y] = 1
            else:
                break

        i = point.y
        while i > 1:
            i -= 1
            if self.map_matrix[point.x][i] == 0 or self.map_matrix[point.x][i] == self.map_matrix[point.x][point.y]:
                self.map_matrix[point.x][i] = 1
            else:
                break

    def __mark_neighbour_points__(self, point: CustomVector3D, id: int, old_id=1, new_group=list):

        self.map_matrix[point.x][point.y] = id
        new_group.append(point)
        if self.map_matrix[point.x + 1][point.y] == old_id:
            self.__mark_neighbour_points__(CustomVector3D(
                point.x + 1, point.y), id, old_id=old_id, new_group=new_group)

        if self.map_matrix[point.x][point.y + 1] == old_id:
            self.__mark_neighbour_points__(CustomVector3D(
                point.x, point.y + 1), id, old_id=old_id, new_group=new_group)

    def __find_path_down__(self, point: CustomVector3D):
        result = list()
        for i in range(point.y, len(self.map_matrix[0])):
            if self.map_matrix[point.x][i] == self.map_matrix[point.x][point.y]:
                result.append(CustomVector3D(point.x, i))
            elif self.map_matrix[point.x][i] == 0:
                result.append(CustomVector3D(point.x, i))
            else:
                result.append(CustomVector3D(point.x, i))
                return result

        return list()

    def __find_path_up__(self, point: CustomVector3D):
        result = list()
        i = point.y - 1
        while i > 1:
            if self.map_matrix[point.x][i] == self.map_matrix[point.x][point.y]:
                result.append(CustomVector3D(point.x, i))
            elif self.map_matrix[point.x][i] == 0:
                result.append(CustomVector3D(point.x, i))
            else:
                result.append(CustomVector3D(point.x, i))
                return result
            i -= 1

        return list()

    def __find_path_left__(self, point: CustomVector3D):
        result = list()
        i = point.y - 1
        while i > 1:
            if self.map_matrix[i][point.y] == self.map_matrix[point.x][point.y]:
                result.append(CustomVector3D(i, point.y))
            elif self.map_matrix[i][point.y] == 0:
                result.append(CustomVector3D(i, point.y))
            else:
                result.append(CustomVector3D(i, point.y))
                return result
            i -= 1

        return list()

    def __find_path_right__(self, point: CustomVector3D):
        result = list()
        for i in range(point.x, len(self.map_matrix)):
            if self.map_matrix[i][point.y] == self.map_matrix[point.x][point.y]:
                result.append(CustomVector3D(i, point.y))
            elif self.map_matrix[i][point.y] == 0:
                result.append(CustomVector3D(i, point.y))
            else:
                result.append(CustomVector3D(i, point.y))
                return result

        return list()

    def __find_free_position(self) -> CustomVector3D:
        root = CustomVector3D()
        while self.map_matrix[root.x][root.y] == 0:
            root.x = random.randint(1, len(self.map_matrix) - 1)
            root.y = random.randint(1, len(self.map_matrix[1]) - 1)

        return root


class InvertedLabyrinth(Labyrinth):
    def __init__(self, width, length, seed: int):
        Labyrinth.__init__(self, width, length, seed)
        x_counter = 0
        while x_counter < self.length:
            y_counter = 0
            while y_counter < self.width:
                if self.map_matrix[x_counter][y_counter] != 0:
                    self.map_matrix[x_counter][y_counter] = 0
                else:
                    self.map_matrix[x_counter][y_counter] = 1
                y_counter += 1
            x_counter += 1


class Rooms1 (BasicLabyrinth):
    class Room:
        size: CustomVector3D
        leftTop: CustomVector3D
        id: int

        def __init__(self, size: CustomVector3D, root: CustomVector3D):
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
                        map[x][y] = BasicLabyrinth.ROOM_SPACE
                        if map[x-1][y] == BasicLabyrinth.EMPTY_SPACE:
                            map[x-1][y] = BasicLabyrinth.WALL_SPACE
                        if map[x+1][y] == BasicLabyrinth.EMPTY_SPACE:
                            map[x+1][y] = BasicLabyrinth.WALL_SPACE
                else:
                    if self.A.x > self.B.x:
                        delta = -1
                    else:
                        delta = 1
                    while x != self.B.x:
                        x += delta
                        map[x][y] = BasicLabyrinth.ROOM_SPACE
                        if map[x][y-1] == BasicLabyrinth.EMPTY_SPACE:
                            map[x][y-1] = BasicLabyrinth.WALL_SPACE
                        if map[x][y+1] == BasicLabyrinth.EMPTY_SPACE:
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

    class SettingsStorage:
        maxRoomSize: CustomVector3D
        minRoomSize: CustomVector3D
        roomsCount: int
        mapSize: CustomVector3D

    rooms = list()
    coridors = list()

    def __init__(self, maxRoomSize: CustomVector3D, minRoomSize: CustomVector3D, roomsCount: int, seed: int):
        maxPossibleWidth = maxRoomSize.x * roomsCount  # X
        maxPossibleLength = maxRoomSize.y * roomsCount  # Y
        BasicLabyrinth.__init__(self, length=0,
                                width=0, seed=seed)  # have no Idea how map is represented there
        Rooms1.SettingsStorage.roomsCount = roomsCount
        Rooms1.SettingsStorage.minRoomSize = minRoomSize
        Rooms1.SettingsStorage.maxRoomSize = maxRoomSize
        Rooms1.SettingsStorage.mapSize = CustomVector3D(
            x=maxPossibleWidth + 2, y=maxPossibleLength + 2)

        self.map_matrix.clear()
        for x in range(0, Rooms1.SettingsStorage.mapSize.x):
            self.map_matrix.append(list())
            for y in range(0, Rooms1.SettingsStorage.mapSize.y):
                self.map_matrix[x].append(Rooms1.EMPTY_SPACE)
        pass

        self.__build__()

    def __build__(self):
        cellMap = list()
        x = self.SettingsStorage.roomsCount
        y = self.SettingsStorage.roomsCount

        for i in range(x):
            cellMap.append(list())
            for j in range(y):
                cellMap[i].append(0)

        while len(self.rooms) < self.SettingsStorage.roomsCount:
            x_ = self.__safe_randint__(0, x-1)
            y_ = self.__safe_randint__(0, y-1)
            if cellMap[x_][y_] == BasicLabyrinth.EMPTY_SPACE:
                room = self.__spawnRoomInCell__(CustomVector3D(x_, y_))
                room.paint(self.map_matrix)
                self.rooms.append(room)
                cellMap[x_][y_] = BasicLabyrinth.ROOM_SPACE

        self.__addCoridors__()
        self.__verifyPainting__()
        pass

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
        while len(self.rooms) > 1:
            start = self.rooms[0].getCenter()
            targetIndex = self.__safe_randint__(1, len(self.rooms)-1)
            end = self.rooms[targetIndex].getCenter()
            coridor = Rooms1.Coridor(start, end)
            print("start:", start, "end:", end)
            coridor.paint(self.map_matrix)
            self.coridors.append(coridor)
            self.rooms.remove(self.rooms[0])

    def __verifyPainting__(self):
        for x in range(1, self.SettingsStorage.mapSize.x-1):
            for y in range(1, self.SettingsStorage.mapSize.y-1):
                if self.map_matrix[x][y] == self.ROOM_SPACE:
                    if self.map_matrix[x-1][y] == self.EMPTY_SPACE:
                        self.map_matrix[x-1][y] = self.WALL_SPACE
                    if self.map_matrix[x+1][y] == self.EMPTY_SPACE:
                        self.map_matrix[x+1][y] = self.WALL_SPACE
                    if self.map_matrix[x][y-1] == self.EMPTY_SPACE:
                        self.map_matrix[x][y-1] = self.WALL_SPACE
                    if self.map_matrix[x][y+1] == self.EMPTY_SPACE:
                        self.map_matrix[x][y+1] = self.WALL_SPACE


class MazeMainPanel(bpy.types.Panel):
    bl_label = "Maze Construct"
    bl_idname = "MAZE_PT_MAINPANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Maze Construct"

    text2: bpy.props.StringProperty(name="Test")

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("wm.export")
        row = layout.row()
        row.operator("wm.spawn_maze")


class WM_OT_Export(bpy.types.Operator):
    bl_label = "Export"
    bl_idname = "wm.export"

    file_extensions = [  # ('.obj', ".obj", '.obj extension'),
        ('.stl', ".stl", '.stl extension'),
        ('.fbx', ".fbx", '.fbx extension')]

    file_extension: bpy.props.EnumProperty(
        name="File extension", items=file_extensions)
    file_name: bpy.props.StringProperty(name="File name")
    filepath: bpy.props.StringProperty(subtype="DIR_PATH")
    filter_glob: bpy.props.StringProperty(
        default='*.jpg;*.jpeg;*.png;*.tif;*.tiff;*.bmp',
        options={'HIDDEN'}
    )

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        #self.filepath = os.path.join(self.filepath, self.file_name + self.file_extension)
        # file = open(self.filepath, 'w')
        # file.write("Hello World " + context.object.name)

        path = self.filepath + "/" + self.file_name
        os.mkdir(path)
        config = open(path+"/model.config", 'w')
        config_str = "<?xml version=\"1.0\"?><model><name>"+self.file_name+"</name>" + \
            "<version>1.0</version><sdf version=\"1.5\">model.sdf</sdf>" + \
            "<description>" + self.file_name + "</description></model>"
        config.write(config_str)
        config.flush()
        config.close()

        mesh_name = self.file_name + "/" + self.file_name + self.file_extension
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

        print(path+self.file_name+self.file_extension)
        if self.file_extension == ".stl":
            bpy.ops.export_mesh.stl(
                filepath=path+"/"+self.file_name+self.file_extension, batch_mode="OFF")
        if self.file_extension == ".fbx":
            bpy.ops.export_scene.fbx(
                filepath=path+"/"+self.file_name+self.file_extension)
        self.filepath = ""
        self.file_name = ""
        # self.file_extension = ""
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class WM_OT_SpawnPar(bpy.types.Operator):
    bl_label = "Spawn parallelepiped"
    bl_idname = "wm.spawn_par"

    text: bpy.props.StringProperty(name="Test", default='asd')
    text2: bpy.props.StringProperty(name="Test2", default='asda')

    def execute(self, context):
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


class WM_OT_SpawnRooms(bpy.types.Operator):
    bl_label = "Spawn rooms"
    bl_idname = "wm.rooms1"

    max_x: bpy.props.IntProperty(name="Max room size x", default=5)
    max_y: bpy.props.IntProperty(name="Max room size y", default=5)
    min_x: bpy.props.IntProperty(name="Min room size x", default=5)
    min_y: bpy.props.IntProperty(name="Min room size y", default=5)
    rooms_counter:  bpy.props.IntProperty(name="Number of rooms", default=5)
    global lab
    lab = Rooms1(CustomVector3D(max_x, max_y), CustomVector3D(
        min_x, min_y), rooms_counter, time.time())


class WM_OT_SpawnMaze(bpy.types.Operator):
    bl_label = "Spawn maze"
    bl_idname = "wm.spawn_maze"

    maze_select_choices = [
        ('OP1', "Labyrinth", "Spawn common labyrinth"),
        ('OP2', "Inverted labyrinth", "Spawn inverted labyrinth"),
        ('OP3', "Office-like labyrinth", "Spawn office-like labyrinth"),
        ('OP4', "Rooms algo 1", "Spawn rooms system")
    ]
    preset_enum: bpy.props.EnumProperty(
        name="Select labyrinth type", items=maze_select_choices)

    maze_width: bpy.props.IntProperty(name="Width", default=20)
    maze_length: bpy.props.IntProperty(name="Length", default=20)

    def execute(self, context):
        global lab
        if self.preset_enum == 'OP1':
            lab = Labyrinth(self.maze_width, self.maze_length, time.time())
        elif self.preset_enum == 'OP2':
            lab = InvertedLabyrinth(
                self.maze_width, self.maze_length, time.time())
        elif self.preset_enum == 'OP3':
            lab = OfficeLabyrinth(
                self.maze_width, self.maze_length, time.time())
        elif self.preset_enum == 'OP4':
            pass
        lab.spawn()
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


def register():
    bpy.utils.register_class(MazeMainPanel)
    bpy.utils.register_class(WM_OT_Export)
    bpy.utils.register_class(WM_OT_SpawnPar)
    bpy.utils.register_class(WM_OT_SpawnMaze)
    bpy.utils.register_class(WM_OT_SpawnRooms)


def unregister():
    bpy.utils.unregister_class(MazeMainPanel)
    bpy.utils.unregister_class(WM_OT_Export)
    bpy.utils.unregister_class(WM_OT_SpawnPar)
    bpy.utils.unregister_class(WM_OT_SpawnMaze)
    bpy.utils.register_class(WM_OT_SpawnRooms)


if __name__ == "__main__":
    register()

    maxS = CustomVector3D(6, 10)
    minS = CustomVector3D(5,10)
    romN = 10
    a = Rooms1(maxRoomSize=maxS, minRoomSize=minS, roomsCount=romN, seed=time.time())
    a.spawn()