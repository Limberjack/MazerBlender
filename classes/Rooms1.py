from Basic import BasicLabyrinth
from Basic import CustomVector3D


class Rooms1(BasicLabyrinth):

    class Way:
        steps = list()
        begin = CustomVector3D()
        corner = CustomVector3D()
        end = CustomVector3D()
        id = 0 
        def __init__(self):
            pass

        def implement(self, map:list):
            pass

    class Room:
        id = 0
        root = CustomVector3D(0, 0, 0)  # top left corner
        dimentions = CustomVector3D(0, 0, 0)
        visited = False

        def __init__(
            self, id_: int, root_: (CustomVector3D), dimentions_: CustomVector3D
        ):
            self.id = id_
            self.root = root_
            self.dimentions = dimentions_

        def paintWals(self, map):
            for d_x in range(self.dimentions.x + 1):
                #print("Paint wals x: ", self.root.x, d_x, "y: ", self.root.y, self.dimentions.y, "map",len(map),len(map[0]))
                map[self.root.x + d_x][self.root.y] = 0
                map[self.root.x + d_x][self.root.y + self.dimentions.y] = 0

            for d_y in range(self.dimentions.y + 1):
                #print("Paint wals y: ", self.root.y + d_y)
                map[self.root.x][self.root.y + d_y] = 0
                map[self.root.x + self.dimentions.x][self.root.y + d_y] = 0

            pass

        def paint(self, map):
            for d_x in range(
                1, self.dimentions.x
            ):  # since dimentions include borders, free space is less for 2 points
                for d_y in range(1, self.dimentions.y):
                    # print(
                    #    "PAINT x:", self.root.x + d_x, "y:", self.root.y + d_y
                    # )
                    map[self.root.x + d_x][self.root.y + d_y] = self.id
            pass

        def repaint(self, map, id):
            self.id = id
            self.paint(map)
            pass

        def isYours(self, point: CustomVector3D) -> bool:
            if point.x > self.root and point.x < self.root.x + self.dimentions.x \
                    and point.y > self.root and point.y < self.root.y + self.dimentions.y:
                return True
            return False

        def __collectLeftWays__(self, map)->list:
            
            pass

        def __collectRightWays__(self, map)->list:
            pass

        def __collectBottWays__(self, map)->list:
            pass

        def __collectTopWays__(self, map)->list:
            pass

        def collectWays(self, map:list)->list:
            ways = self.__collectBottWays__(map)
            ways.append(self.__collectTopWays__(map))
            ways.append(self.__collectLeftWays__(map))
            ways.append(self.__collectRightWays__(map))
            return ways

        def collectCorneredWays(self, map)->list:
            pass

    def __init__(
        self,
        maxRoomSize: CustomVector3D,
        minRoomSize: CustomVector3D,
        seed: int,
        room_number: int,
        maxRoomInARow=5,
        maxRoomInAColumn=5
    ):
        BasicLabyrinth.__init__(
            self=self,
            width=2,
            length=2,
            seed=seed,
        )
        # expand room sizes with summary walls thickness
        minRoomSize.x = minRoomSize.x + 2
        minRoomSize.y = minRoomSize.y + 2

        maxRoomSize.x = maxRoomSize.x + 2
        maxRoomSize.y = maxRoomSize.y + 2

        self.minRoomSize = minRoomSize
        self.maxRoomSize = maxRoomSize
        self.room_number = room_number
        self.maxRoomInARow_ = maxRoomInARow
        self.maxRoomInAColumn_ = maxRoomInAColumn

        self.map_matrix.clear()
        self.width = (maxRoomSize.y * maxRoomInARow) + 2
        self.length = (maxRoomSize.x * maxRoomInAColumn) + 2
        self.map_matrix = [[-1 for y in range((maxRoomSize.y * maxRoomInARow) + 2)]
                           for x in range((maxRoomSize.x * maxRoomInAColumn) + 2)]
        #print(len(self.map_matrix), len(self.map_matrix[0]))
        self.__buildMap__()

    def __buildMap__(self):
        sectors = list()
        default_id = 0
        for x in range(self.maxRoomInAColumn_):
            for y in range(self.maxRoomInARow_):
                sectors.append(
                    CustomVector3D(
                        x * self.maxRoomSize.x,
                        y * self.maxRoomSize.y,
                        default_id + (self.room_number * x + y + 1),
                    )
                )

        roomedSectors = set()
        while len(roomedSectors) < self.room_number:
            roomedSectors.add(
                sectors[self.__safe_randint__(0, len(sectors)-1)])

        rooms = list()
        for i in roomedSectors:
            size_x = self.__safe_randint__(
                self.minRoomSize.x, self.maxRoomSize.x)
            size_y = self.__safe_randint__(
                self.minRoomSize.y, self.maxRoomSize.y)
            dimentions = CustomVector3D(size_x, size_y, 0)

            root_x = self.__safe_randint__(
                0, self.maxRoomSize.x - size_x) + i.x + 1
            root_y = self.__safe_randint__(
                0, self.maxRoomSize.y - size_y) + i.y + 1
            root = CustomVector3D(root_x, root_y, 0)
            # print("root:",root.x, root.y," dim:",dimentions.x, dimentions.y)

            room = Rooms1.Room(root_=root, dimentions_=dimentions, id_=i.z)
            rooms.append(room)
            room.paintWals(self.map_matrix)
            room.paint(self.map_matrix)

    def __connectRooms__(self, rooms: list):
        notConnectedRooms = list()
        for i in rooms:
            ways = i.collectWays(self.map_matrix)
            if len(ways) == 0:
                notConnectedRooms.append(i)
                continue
            
            way = ways[self.__safe_randint__(0, len(ways) - 1)]
            way.implement(self.map_matrix)

        if len(notConnectedRooms) == 0:
            return
        
        for i in notConnectedRooms:
            ways = i.collectCorneredWays(self.map_matrix)
            way = ways[self.__safe_randint__(0, len(ways) - 1)]
            way.implement(self.map_matrix)

        pass    

    def spawn(self):
        pass


minRoomSize = CustomVector3D(1, 1)
maxRoomSize = CustomVector3D(10, 10)
a = Rooms1(seed=-1, room_number=5, minRoomSize=minRoomSize, maxRoomSize=maxRoomSize, maxRoomInAColumn=3, maxRoomInARow=10
           )
a.print_in_console()
