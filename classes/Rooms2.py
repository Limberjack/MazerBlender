from Basic import CustomVector3D
from Basic import random
from Basic import BasicLabyrinth
from Basic import ObstacleRoom

class Rooms2 (BasicLabyrinth):
    
    class SettingsStorage:
        maxRoomSize: CustomVector3D
        minRoomSize: CustomVector3D
        roomsCount: int
        roomsInRow: int
        mapSize: CustomVector3D
        numberOfObstacles:int
        pathToMeshes:str

    class Room (ObstacleRoom):
        size: CustomVector3D
        leftTop: CustomVector3D
        id: int

        def __init__(self, size: CustomVector3D, root: CustomVector3D):
            ObstacleRoom.__init__(self=self, topLeft=root, size=size, numberOfObstacles=Rooms2.SettingsStorage.numberOfObstacles, pathToObstacles=Rooms2.SettingsStorage.pathToMeshes)
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
                map[x][y] = Rooms2.ROOM_SPACE
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
        BasicLabyrinth.__init__(self, length=0,
                       width=0, seed=seed)  # have no Idea how map is represented there
        Rooms2.SettingsStorage.roomsCount = roomsCount
        Rooms2.SettingsStorage.minRoomSize = minRoomSize
        Rooms2.SettingsStorage.maxRoomSize = maxRoomSize
        Rooms2.SettingsStorage.mapSize = CustomVector3D(
            x=maxPossibleWidth, y=maxPossibleLength)
        Rooms2.SettingsStorage.mainCoridorWidth = mainCoridorWidth
        Rooms2.SettingsStorage.roomsInRow = roomsInRow

        self.map_matrix.clear()
        for x in range(0, Rooms2.SettingsStorage.mapSize.x):
            self.map_matrix.append(list())
            for y in range(0, Rooms2.SettingsStorage.mapSize.y):
                self.map_matrix[x].append(Rooms2.EMPTY_SPACE)
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
                room.paint(self.map_matrix)
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
        self.mainCoridor.paint(self.map_matrix)
        

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
            coridor.paint(self.map_matrix)

        for i in self.botRooms:
            A = i.getRandomPoint()
            B = CustomVector3D(self.mainCoridor.leftTop.x + 1, A.y)
            coridor = Rooms2.Coridor(A, B)
            self.coridors.append(coridor)
            coridor.paint(self.map_matrix)


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
