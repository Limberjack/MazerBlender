from basic import CustomVector3D
from basic import random
from basic import BasicLabyrinth


class Rooms1 (BasicLabyrinth):

    class SettingsStorage:
        maxRoomSize: CustomVector3D
        minRoomSize: CustomVector3D
        minCoridorLength: int
        maxCoridorLength: int
        roomsCount: int
        mapSize: CustomVector3D

    rooms = list()
    coridors = list()

    def __init__(self, maxRoomSize: CustomVector3D, minRoomSize: CustomVector3D, minMaxCoridorLength: CustomVector3D, roomsCount: int, seed: int):
        maxPossibleWidth = maxRoomSize.x * roomsCount + \
            minMaxCoridorLength.y * (roomsCount - 1)
        maxPossibleLength = maxRoomSize.y * roomsCount + \
            minMaxCoridorLength.x * (roomsCount - 1)
        BasicLabyrinth(length=maxPossibleLength,
                       width=maxPossibleWidth, seed=seed)
        Rooms1.SettingsStorage.roomsCount = roomsCount
        Rooms1.SettingsStorage.minRoomSize = minRoomSize
        Rooms1.SettingsStorage.maxRoomSize = maxRoomSize
        Rooms1.SettingsStorage.minCoridorLength = minMaxCoridorLength.x
        Rooms1.SettingsStorage.maxCoridorLength = minMaxCoridorLength.y
        self.build()
        Rooms1.SettingsStorage.mapSize = CustomVector3D(
            x=maxPossibleWidth, y=maxPossibleLength)

        self.map_matrix.clear()
        for x in range(0, Rooms1.SettingsStorage.mapSize.x):
            self.map_matrix.append(list())
            for y in range(0, Rooms1.SettingsStorage.mapSize.y):
                self.map_matrix[x].append(Rooms1.EMPTY_SPACE)
        pass

    def build(self):
        initialRoomSize = CustomVector3D()
        initialRoomSize.x = self.__safe_randint__(
            Rooms1.SettingsStorage.minRoomSize.x, Rooms1.SettingsStorage.maxRoomSize.x)
        initialRoomSize.y = self.__safe_randint__(
            Rooms1.SettingsStorage.minRoomSize.y, Rooms1.SettingsStorage.maxRoomSize.y)

        initialRoomRoot = CustomVector3D()
        initialRoomRoot.x = self.__safe_randint__(
            0, Rooms1.SettingsStorage.x - initialRoomSize.x)
        initialRoomRoot.y = self.__safe_randint__(
            0, Rooms1.SettingsStorage.y - initialRoomSize.y)

        initialRoom = Rooms1.Room(initialRoomSize, initialRoomRoot)
        self.rooms.append(initialRoomRoot)

        while len(self.rooms) < Rooms1.SettingsStorage.roomsCount:
            for i in self.rooms:
                possibleWays = i.getWays(self.map_matrix)
                selectedWay = possibleWays[self.__safe_randint__(
                    0, len(possibleWays) - 1)]
                selectedWay.paint()
                self.coridors.append(selectedWay)
                possibleRooms = selectedWay.getRooms()
                selectedRoom = possibleRooms[self.__safe_randint__(
                    0, len(possibleRooms) - 1)]
                selectedRoom.paint()
                self.rooms.append(selectedRoom)
        pass

    class Room:
        size: CustomVector3D
        rightTop: CustomVector3D
        leftTop: CustomVector3D
        rightBot: CustomVector3D
        leftBot: CustomVector3D
        id: int

        def __init__(self, size: CustomVector3D, root: CustomVector3D):
            self.buildWithTopLeftCorner(size=size, leftTop=root)

        def buildWithTopLeftCorner(self, size: CustomVector3D, leftTop: CustomVector3D):
            self.size = size
            self.leftTop = leftTop
            self.rightTop = CustomVector3D(leftTop.x, leftTop.y + size.y)
            self.rightBot = CustomVector3D(
                self.rightBot.x + size.x, self.rightTop.y)
            self.leftBot = CustomVector3D(leftTop.x + size.x, leftTop.y)

        def buildWithTopRightCorner(self, size: CustomVector3D, rightTop: CustomVector3D):
            self.size = size
            self.rightTop = rightTop
            self.leftTop = CustomVector3D(rightTop.x, rightTop.y - size.y)
            self.rightBot = CustomVector3D(rightTop.x + size.x, rightTop.y)
            self.leftBot = CustomVector3D(
                rightTop.x + size.x, rightTop.y - size.y)

        def getWays(self, map: list) -> list:
            ways = list()
            for x in range(self.leftTop.x, self.leftBot.x):
                wayRoot = CustomVector3D(x, self.leftTop.y)
                ways += self.__collectWaysFromRoot__(
                    type=Rooms1.Way.TYPE_LEFT, root=wayRoot)
                wayRoot = CustomVector3D(x, self.RightTop.y)
                ways += self.__collectWaysFromRoot__(
                    type=Rooms1.Way.TYPE_RIGHT, root=wayRoot)

            for y in range(self.leftTop.y, self.rightTop.y):
                wayRoot = CustomVector3D(self.leftTop.x, y)
                ways += self.__collectWaysFromRoot__(
                    type=Rooms1.Way.TYPE_UP, root=wayRoot)
                wayRoot = CustomVector3D(self.rightBot.x, y)
                ways += self.__collectWaysFromRoot__(
                    type=Rooms1.Way.TYPE_DOWN, root=wayRoot)

            return ways

        def __collectWaysFromRoot__(self, type, root: CustomVector3D) -> list:
            result = list()
            for i in range(Rooms1.SettingsStorage.minCoridorLength, Rooms1.SettingsStorage.maxCoridorLength + 1):
                way = Rooms1.Way(root, type)
                if way.build(map=map, len=i):
                    result.append(way)

        def paint(self, map: list):
            for x in range(self.rightTop.x + 1, self.rightTop.x + self.size.x - 1):
                for y in range(self.rightTop.y + 1, self.rightTop.y + self.size.y - 1):
                    map[x][y] = Rooms1.ROOM_SPACE

            for x in range(self.rightTop.x, self.rightTop.x + self.size.x):
                map[x][self.rightTop.y] = Rooms1.WALL_SPACE
                map[x][self.rightTop.y + self.size.y] = Rooms1.WALL_SPACE

            for y in range(self.rightTop.y, self.rightTop.y + self.size.y):
                map[self.rightTop.x][y] = Rooms1.WALL_SPACE
                map[self.rightTop.x + self.size.x][y] = Rooms1.WALL_SPACE

    class Way:
        TYPE_UP = 1
        TYPE_DOWN = 2
        TYPE_LEFT = 3
        TYPE_RIGHT = 4

        __end__: CustomVector3D
        __root__: CustomVector3D
        __room__: object

        def __init__(self, root: CustomVector3D, type: int):
            self.__root__ = root
            self.__type__ = type

        def build(self, map: list, len: int):
            if self.__type__ == self.TYPE_UP:
                return self.__buildUp__(map=map, length=len)
            elif self.__type__ == self.TYPE_DOWN:
                return self.__buildDown__(map=map, length=len)
            elif self.type == self.TYPE_RIGHT:
                return self.__buildRight__(map=map, length=len)
            elif self.type == self.TYPE_LEFT:
                return self.__buildLeft__(map=map, length=len)
            pass

        def paint():
            pass

        def __buildDown__(self, map: list, length: int) -> bool:

            if len(map) <= length + self.__root__.x :
                return False

            for i in range(length - 1):  # should not check root point as soon as it will be a wall
                if map[self.__root__.x + i + 1][self.__root__.y] != BasicLabyrinth.EMPTY_SPACE:
                    return False

            self.__end__.x = self.__root__.x + (length - 1)
            self.__end__.y = self.__root__.y

            rooms = list()
            # as soon as we should not connect coridor entrance to a corner block
            yRight = self.__end__.y - 1
            yLeft = yRight - (Rooms1.SettingsStorage.minRoomSize.y - 2 - 1)
            for y in range(yLeft, yRight + 1):
                root = CustomVector3D(self.__end__.x, y)
                list.extend(self.__collectRoomsWithBruteForce__(
                    map=map, root=root))

            if len(rooms) == 0:
                return False

            chosenRoomIndex = BasicLabyrinth.safeRand(0, len(rooms))
            self.__room__ = rooms[chosenRoomIndex]
            return True

        def __buildUp__(self, map: list, length: int) -> bool:
            if self.__root__.x - length <= 0:
                return False 

            for i in range(len - 1):
                if map[self.__root__.x + i + 1][self.__root__.y] != BasicLabyrinth.EMPTY_SPACE:
                    return False

            self.__end__.x = self.__root__.x + (len - 1)
            self.__end__.y = self.__root__.y

            rooms = list()
            # as soon as we should not connect coridor entrance to a corner block
            yRight = self.__end__.y - 1
            yLeft = yRight - (Rooms1.SettingsStorage.minRoomSize.y - 2 - 1)
            for y in range(yLeft, yRight + 1):
                root = Rooms1.Room(self.__end__.x, 0)
                root.
                list.extend(self.__collectRoomsWithBruteForce__(
                    map=map, root=root))

            if len(rooms) == 0:
                return False

            chosenRoomIndex = BasicLabyrinth.safeRand(0, len(rooms))
            self.__room__ = rooms[chosenRoomIndex]
            return True
            pass

        def __buildLeft__(self, map: list, length: int) -> bool:
            pass

        def __buildRight__(self, map: list, length: int) -> bool:
            pass

        def __prepareRoomUp__(self, map: list):
            pass

        def __collectRoomsWithBruteForceLeftTop__(self, map, root: CustomVector3D):

            def roomCanBePlaced(map, room: Rooms1.Room) -> bool:
                x1 = room.leftTop.x
                y1 = room.leftTop.y

                x2 = room.rightBot.x
                y2 = room.rightBot.y

                if x1 < 0 or y1 < 0 or x2 >= len(map) or y2 >= len(map[0]):
                    return False

                for x in range(x1, x2 + 1):
                    for y in range(y1, y2 + 1):
                        if map[x][y] != BasicLabyrinth.EMPTY_SPACE:
                            return False

                return True

            rooms = list()
            for x_ in range(Rooms1.SettingsStorage.minRoomSize.x, Rooms1.SettingsStorage.maxRoomSize.x):
                for y_ in range(Rooms1.SettingsStorage.minRoomSize.y, Rooms1.SettingsStorage.maxRoomSize.y):
                    room = Rooms1.Room(
                        size=CustomVector3D(x_, y_), leftTop=root)
                    if roomCanBePlaced(map, room):
                        rooms.append(room)
            return rooms

            