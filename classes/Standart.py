from Basic import BasicLabyrinth
from Basic import CustomVector3D
from Basic import random


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