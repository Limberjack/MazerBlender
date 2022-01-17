from Basic import BasicLabyrinth
from Basic import CustomVector3D
from Basic import random

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