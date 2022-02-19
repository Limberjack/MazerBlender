from Basic import CustomVector3D
from Basic import random
from Basic import BasicLabyrinth 
from Basic import time


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
        roomsX:int
        roomsY:int

    rooms = list()
    coridors = list()

    def __init__(self, maxRoomSize: CustomVector3D, minRoomSize: CustomVector3D, roomsCount: int, seed: int, roomsX = -1, roomsY = -1):

        if roomsX == -1:
            roomsX = roomsCount

        if roomsY == -1:
            roomsY = roomsCount

        maxPossibleWidth = maxRoomSize.x * roomsX  # X
        maxPossibleLength = maxRoomSize.y * roomsY  # Y
        BasicLabyrinth.__init__(self, length=0,
                                width=0, seed=seed)  # have no Idea how map is represented there
        Rooms1.SettingsStorage.roomsCount = roomsCount
        Rooms1.SettingsStorage.minRoomSize = minRoomSize
        Rooms1.SettingsStorage.maxRoomSize = maxRoomSize
        Rooms1.SettingsStorage.mapSize = CustomVector3D(
            x=maxPossibleWidth, y=maxPossibleLength)
        Rooms1.SettingsStorage.roomsX = roomsX
        Rooms1.SettingsStorage.roomsY = roomsY

        self.map_matrix.clear()
        for x in range(0, Rooms1.SettingsStorage.mapSize.x):
            self.map_matrix.append(list())
            for y in range(0, Rooms1.SettingsStorage.mapSize.y):
                self.map_matrix[x].append(Rooms1.EMPTY_SPACE)
        pass

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
        for x in range(1, self.SettingsStorage.mapSize.x):
            for y in range(1, self.SettingsStorage.mapSize.y):
                if self.map_matrix[x][y] == self.ROOM_SPACE:
                    if self.map_matrix[x-1][y] == self.EMPTY_SPACE:
                        self.map_matrix[x-1][y] = self.WALL_SPACE
                    if self.map_matrix[x+1][y] == self.EMPTY_SPACE:
                        self.map_matrix[x+1][y] = self.WALL_SPACE
                    if self.map_matrix[x][y-1] == self.EMPTY_SPACE:
                        self.map_matrix[x][y-1] = self.WALL_SPACE
                    if self.map_matrix[x][y+1] == self.EMPTY_SPACE:
                        self.map_matrix[x][y+1] = self.WALL_SPACE

    def spawn(self):
        self.length = len(self.map_matrix)
        self.width = len(self.map_matrix[0])
        self.print_in_console()
        bottom_root_point = CustomVector3D(0, 0, 0)
        bottom_target_point = CustomVector3D(
            self.length - 1, self.width - 1, 0.5)
        self.spawn_cube(bottom_root_point, bottom_target_point)

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