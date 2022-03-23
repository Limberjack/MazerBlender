import random

import bpy
import os


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
    CORIDOR_SPACE = 3

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
        diag_vector.x = dist_point.x - root_point.x + BasicLabyrinth.cube_width
        diag_vector.y = dist_point.y - root_point.y + BasicLabyrinth.cube_length
        diag_vector.z = dist_point.z - root_point.z + BasicLabyrinth.cube_height
        bpy.ops.mesh.primitive_cube_add(enter_editmode=False,
                                        location=(root_point.x + diag_vector.x / 2, root_point.y + diag_vector.y / 2,
                                                  root_point.z + diag_vector.z / 2),
                                        rotation=(0, 0, 0), scale=(diag_vector.x / 2, diag_vector.y / 2, diag_vector.z))

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
        self.length = len(self.map_matrix[0])
        self.width = len(self.map_matrix)
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
        for x in range(1, self.length-1):
            horisontal_list = list()
            for y in range(1, self.width-1):
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

        for y in range(1, self.width-1):
            vertical_list = list()
            for x in range(1, self.length-1):
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
        for x in range(0, len(self.map_matrix)):
            for y in range(0, len(self.map_matrix[x])):
                if self.map_matrix[x][y] == self.WALL_SPACE:
                    print("▓▓", end='')
                elif self.map_matrix[x][y] == self.ROOM_SPACE:
                    print("..", end="")
                else:
                    print("  ", end="")
            print("")


class ObstacleRoom:
    topLeft: CustomVector3D
    size: CustomVector3D
    numberOfObstacles: int
    pathToObstacles: str

    def __init__(self, topLeft: CustomVector3D, size: CustomVector3D, numberOfObstacles: int, pathToObstacles: int):
        self.numberOfObstacles = numberOfObstacles
        self.pathToObstacles = pathToObstacles
        self.size = size
        self.topLeft = topLeft

    def __collectMeshes__(self) -> list:
        result = list()
        for file in os.listdir(self.pathToObstacles):
            if file.endswith(".stl"):
                result.append(self.pathToObstacles + "/" + file)
        return result

    def __spawnMesh__(self, mesh: str, position: CustomVector3D):
        print(mesh)
        rotation = BasicLabyrinth.safeRand(0, 360)
        position.x += BasicLabyrinth.cube_width / 2
        position.y += BasicLabyrinth.cube_length / 2
        position.z += 2.25
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
        while dx < self.size.x + self.topLeft.x:
            dy = root.y
            while dy < self.size.y + self.topLeft.y:
                if mapMatrix[dx][dy] == BasicLabyrinth.ROOM_SPACE:
                    points.append(CustomVector3D(dx, dy))
                dy += 2
            dx += 2
        return points

    def spawnObstacles(self, mapMatrix: list):
        pointsSets = list()
        pointsSets.append(self.__collectPositions__(
            mapMatrix=mapMatrix, root=self.topLeft))
        pointsSets.append(self.__collectPositions__(
            mapMatrix=mapMatrix, root=CustomVector3D(self.topLeft.x + 1, self.topLeft.y)))
        pointsSets.append(self.__collectPositions__(
            mapMatrix=mapMatrix, root=CustomVector3D(self.topLeft.x, self.topLeft.y + 1)))
        pointsSets.append(self.__collectPositions__(
            mapMatrix=mapMatrix, root=CustomVector3D(self.topLeft.x + 1, self.topLeft.y + 1)))

        maxLen = len(pointsSets[0])
        longestList = pointsSets[0]
        for i in pointsSets:
            if len(i) > maxLen:
                maxLen = len(i)
                longestList = i

        objects = set()
        meshes = self.__collectMeshes__()
        while len(objects) < maxLen and len(objects) < self.numberOfObstacles:
            index = BasicLabyrinth.safeRand(0, len(longestList) - 1)
            objects.add(longestList[index])
            self.__spawnMesh__(
                meshes[BasicLabyrinth.safeRand(0, len(meshes) - 1)], longestList[index])
            longestList.remove(longestList[index])
