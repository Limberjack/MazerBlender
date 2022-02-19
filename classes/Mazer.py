from datetime import date
import bpy
import os
import sys
import time

from pip import main

import Rooms1
import Rooms2
import Standart
import Random
from Basic import CustomVector3D


class MazeTypes:
    MAZE_TYPE_LABYRINTH = 1
    MAZE_TYPE_INVERTED_LABYRINTH = 2
    MAZE_TYPE_RANDOM_SPACE = 3
    MAZE_TYPE_ROOMS1 = 4
    MAZE_TYPE_ROOMS2 = 5

def toMesh(name: str, path=".", ext=".stl"):
    path = path + "/" + name
    os.mkdir(path)
    config = open(path+"/model.config", 'w')
    config_str = "<?xml version=\"1.0\"?><model><name>"+name+"</name>" + \
        "<version>1.0</version><sdf version=\"1.5\">model.sdf</sdf>" + \
        "<description>" + name + "</description></model>"
    config.write(config_str)
    config.flush()
    config.close()

    mesh_name = name + "/" + name + ext
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

    print(path+"/"+name+ext)
    if ext == ".stl":
        bpy.ops.export_mesh.stl(
            filepath=path+"/"+name+ext, batch_mode="OFF")
    elif ext == ".fbx":
        bpy.ops.export_scene.fbx(
            filepath=path+"/"+name+ext)
    else:
        bpy.ops.export_mesh.stl(
            filepath=path+"/"+name+ext, batch_mode="OFF")



def getTheConfiguration(filePath) -> dict:
    if not os.path.isfile(filePath):
        print("Given configuration file \""+filePath +
              "\" does not exist or can't be reached")
        exit(1)
    file = open(filePath, "r")
    string = file.readline()
    settings = dict()
    while len(string) != 0:
        if string[0] == "#":
            string = file.readline()
            continue
        keyAndVal = string.split("=")
        if len(keyAndVal) <= 1:
            string = file.readline()
            continue
        keyAndVal[0] = str(keyAndVal[0]).strip()
        keyAndVal[1] = str(keyAndVal[1]).strip()
        settings.update([keyAndVal])
        string = file.readline()

    file.close()
    return settings


def spawnConfigurationFile(fielPath=".", mazeType=MazeTypes.MAZE_TYPE_LABYRINTH):
    file = open(fielPath, "w")

    file.write(
        "#NAME_PATTERN is a string, that woul be added in the prefix of the mesh's name\n")
    file.write("#If it's set to default, the maze type would be used instead\n")
    file.write("NAME_PATTERN=default\n\n")

    file.write("#PATH is a path where to mesh would be saved\n")
    file.write(
        "#If it's set to default, the mesh would be saved in a current directory\n")
    file.write("PATH=default\n\n")

    file.write(
        "#TYPE could be \"labyrinth\", \"inverted\", \"random\", \"rooms1\", \"rooms2\"\n")
    if mazeType == MazeTypes.MAZE_TYPE_LABYRINTH:
        file.write("TYPE=labyrinth\n\n")
    elif mazeType == MazeTypes.MAZE_TYPE_INVERTED_LABYRINTH:
        file.write("TYPE=inverted\n\n")
    elif mazeType == MazeTypes.MAZE_TYPE_RANDOM_SPACE:
        file.write("TYPE=random\n\n")
    elif mazeType == MazeTypes.MAZE_TYPE_ROOMS1:
        file.write("TYPE=rooms1\n\n")
    elif mazeType == MazeTypes.MAZE_TYPE_ROOMS2:
        file.write("TYPE=rooms2\n\n")

    file.write(
        "#to use use current time as random funchion seed, set \"RANDOM_SEED=default\"\n")
    file.write(
        "#also you could set your own seed, but it should be a number \"RANDOM_SEED=42\"\n")
    file.write("RANDOM_SEED=default\n\n")

    if mazeType == MazeTypes.MAZE_TYPE_LABYRINTH or \
            mazeType == MazeTypes.MAZE_TYPE_INVERTED_LABYRINTH or \
            mazeType == MazeTypes.MAZE_TYPE_RANDOM_SPACE:
        file.write("#SIZE=x:y\n")
        file.write("SIZE=20:20\n\n")

        file.close()
        return

    file.write("#Number of rooms you want to have\n")
    file.write("ROOMS_COUNT=10\n\n")

    file.write("#Minimum room width and length: \"MIN_ROOM_SIZE=5:5\"\n")
    file.write("MIN_ROOM_SIZE=5:5\n\n")

    file.write("#Maximum room width and length: \"MAX_ROOM_SIZE=10:10\"\n")
    file.write("MAX_ROOM_SIZE=10:10\n\n")

    if mazeType == MazeTypes.MAZE_TYPE_ROOMS1:
        file.write(
            "#How many rooms you want to allow to be in one vertical line X, and horizontal line Y?\n")
        file.write("#Be sure that ROOMS_X * ROOMS_Y >= ROOMS_COUNT\n")
        file.write(
            "#You can set \"ROOMS_X=default\", \"ROOMS_X=default\" to make them equal to ROOMS_COUNT\n")
        file.write("ROOMS_X=5\n")
        file.write("ROOMS_Y=3\n\n")

    elif mazeType == MazeTypes.MAZE_TYPE_ROOMS2:
        file.write("#How many rooms you want to allow to be in one line?\n")
        file.write("#Be sure that ROOMS_IN_LINE * 2 >= ROOMS_COUNT\n")
        file.write(
            "#You can set \"ROOMS_IN_LINE=default\" to make it equal to ROOMS_COUNT\n")
        file.write("ROOMS_IN_LINE=5\n\n")

        file.write("#How wide you want main coridor to be?\n")
        file.write("#Be sure that MAIN_CORIDOR_WIDTH >= 3\n")
        file.write("MAIN_CORIDOR_WIDTH=5")

    file.close()
    return


def printInvalidInput():
    print("Input is invalid.")
    print("Please refer to a guideline in HOWTO.txt")


def initializeConfigs(foldePath="./"):
    foldePath += "/MazerConfigs"
    if not os.path.isdir(foldePath):
        os.mkdir(foldePath)

    spawnConfigurationFile(foldePath+"/Labyrinth",
                           MazeTypes.MAZE_TYPE_LABYRINTH)
    spawnConfigurationFile(foldePath+"/Inverted",
                           MazeTypes.MAZE_TYPE_INVERTED_LABYRINTH)
    spawnConfigurationFile(foldePath+"/Random",
                           MazeTypes.MAZE_TYPE_RANDOM_SPACE)
    spawnConfigurationFile(foldePath+"/Rooms1", MazeTypes.MAZE_TYPE_ROOMS1)
    spawnConfigurationFile(foldePath+"/Rooms2", MazeTypes.MAZE_TYPE_ROOMS2)


def doWork(configPath: str):
    def arrToVector(arr: list, defaultValue: CustomVector3D):
        result = CustomVector3D()
        try:
            result.x = int(arr[0])
            result.y = int(arr[1])
        except ValueError:
            return defaultValue
        return result

    def getNumerical(value, defaultValue):
        if value == None:
            return defaultValue
        try:
            value = int(value)
        except ValueError:
            return defaultValue
        return value

    settings = getTheConfiguration(configPath)
    type = settings.get("TYPE")

    seed = settings.get("RANDOM_SEED")
    seed = getNumerical(
        seed, time.time())

    namePattern = settings.get("NAME_PATTERN")
    if namePattern == None or namePattern == "default":
        namePattern = str(type) + "_"

    path = settings.get("PATH")
    if path == None or path == "default":
        path = "./"

    lab = None
    if type == "labyrinth" or type == "inverted" or type == "random":

        size = str(settings.get("SIZE"))
        size = arrToVector(size.split(":"), CustomVector3D(20, 20))

        if type == "labyrinth":
            lab = Standart.Labyrinth(width=size.y, length=size.x, seed=seed)
        elif type == "inverted":
            lab = Standart.InvertedLabyrinth(
                width=size.y, length=size.x, seed=seed)
        elif type == "random":
            lab = Random.OfficeLabyrinth(
                width=size.y, length=size.x, seed=seed)

    elif type == "rooms1" or type == "rooms2":
        maxRoomSize = str(settings.get("MAX_ROOM_SIZE"))
        maxRoomSize = arrToVector(
            maxRoomSize.split(":"), CustomVector3D(10, 10))

        minRoomSize = str(settings.get("MIN_ROOM_SIZE"))
        minRoomSize = arrToVector(minRoomSize.split(":"), CustomVector3D(5, 5))

        roomsCount = settings.get("ROOMS_COUNT")
        roomsCount = getNumerical(roomsCount, 10)

        if type == "rooms1":
            roomsX = settings.get("ROOMS_X")
            roomsX = getNumerical(roomsX, roomsCount)

            roomsY = settings.get("ROOMS_Y")
            roomsY = getNumerical(roomsY, roomsCount)

            lab = Rooms1.Rooms1(maxRoomSize=maxRoomSize, minRoomSize=minRoomSize,
                                roomsCount=roomsCount, seed=seed, roomsX=roomsX, roomsY=roomsY)
        elif type == "rooms2":
            roomsInLine = settings.get("ROOMS_IN_LINE")
            roomsInLine = getNumerical(roomsInLine, 5)
            
            mainCoridorWidth = settings.get("MAIN_CORIDOR_WIDTH")
            mainCoridorWidth = getNumerical(mainCoridorWidth, 5)

            lab = Rooms2.Rooms2(maxRoomSize=maxRoomSize, minRoomSize=minRoomSize,
            roomsCount=roomsCount,roomsInRow=roomsInLine, seed=seed)
    
    else:
        print("Unsupported maze type <",type,">", sep="", end=".")
        exit(1)
    
    lab.spawn()
    toMesh(name=namePattern+"_"+str(time.time()), path=path)
    lab.print_in_console()
    print("DONE")
    pass


if __name__ == "__main__":
    argv = sys.argv

    for i in argv:
        if "--init" in i:
            if "--init=" in i:
                initializeConfigs(str(i.split("=")[1]))
            else:
                initializeConfigs()
            exit()

        if i.find("--build=") == -1:
            continue
        else:
            doWork(str(i.split("=")[1]))
            exit()

    printInvalidInput()
    exit(1)