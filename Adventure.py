import AdvCommand
from AdvCommand import AdvMotionCommand
from AdvObject import *
from AdvRoom import *

def main():
    try:
        filename = input('Which game files(Crowther, Small, etc.)? ')
        print()

        s = filename + '{}.txt'

        rooms, objs, synonyms = open(s.format('Rooms')), open(s.format('Objects')), open(s.format('Synonyms'))

        adventure = Adventure.readFromFile(rooms, objs, synonyms)

        rooms.close()
        objs.close()
        synonyms.close()

        adventure.fillObjects()
        adventure.enterRoom(1)

    except IOError:

        print('Check filename')
        main()

class Adventure:

    def __init__(self, rooms, objs, synonyms):

        self.__roomDict = rooms
        self.__objDict = objs
        self.__commandDict = synonyms
        self.__inventory = []
        self.__currentRoom = None

    def getUserCommand(self):

        command = [input('> ').upper(), None]

        command[0] = self.__commandDict[command[0]] if (command[0] in self.__commandDict) else command[0]

        command = command[0].split() if (" " in command[0]) else command

        if self.isValid(*command):

            command[1] = self.__objDict[command[1]] if (command[1] is not None) else command[1]

            self.doCommand(*command)

        else:

            print("> INVALID COMMAND")
            self.getUserCommand()

    def isValid(self, command, objName):

        if objName is None:

            return any(entry.getDirection() == command for entry in self.__currentRoom.getMotionTable())\
                   or command == 'HELP' or command == 'LOOK' or command == 'INVENTORY'

        if objName not in self.__objDict:

            return False

        return command == 'DROP' and self.__objDict[objName] in self.__inventory or\
               command == 'TAKE' and self.__currentRoom.containsObject(self.__objDict[objName])

    def doCommand(self, command, obj = None):

        if command == 'HELP':

            AdvCommand.HELP().execute(self, obj)

        elif command == 'TAKE':

            AdvCommand.TAKE().execute(self, obj)

        elif command == 'DROP':

            AdvCommand.DROP().execute(self, obj)

        elif command == 'QUIT':

            AdvCommand.QUIT().execute(self, obj)

        elif command == 'LOOK':

            AdvCommand.LOOK().execute(self, obj)

        elif command == 'INVENTORY':

            AdvCommand.INVENTORY().execute(self, obj)

        else:

            AdvMotionCommand(command).execute(self, obj)

        self.getUserCommand()

    def enterRoom(self, num):

        if num == 0:

            return

        room = self.__roomDict[num]

        room.display()

        entry = room.getMotionTable()[0]

        if entry.getDirection() == "FORCED":

            self.enterRoom(entry.getDestinationRoom())

        else:

            self.__currentRoom = room

            self.getUserCommand()

    def fillObjects(self):

        for key in self.__objDict:

            obj = self.__objDict[key]

            roomNum = obj.getInitialLocation()

            self.__roomDict[roomNum].addObject(obj)

    def executeMotionCommand(self, direction):

        entries = []

        for entry in self.__currentRoom.getMotionTable():

            if entry.getDirection() == direction:

                entries.append(entry)

        if len(entries) == 1 or any(obj.getName() == entries[0].getKeyName() for obj in self.__inventory):

            self.enterRoom(entries[0].getDestinationRoom())

        else:

            self.enterRoom(entries[1].getDestinationRoom())

    def executeQuitCommand(self):

        userInput = input('Are you sure you want to quit? ')

        if userInput.lower().startswith('y'):

            del self

    def executeHelpCommand(self):

        print('HELP')

    def executeLookCommand(self):

        self.__currentRoom.setVisited(False)

        self.__currentRoom.display()

    def executeInventoryCommand(self):

        if len(self.__inventory) == 0:

            print('You are empty handed')

        else:

            print('\n'.join([obj.getName()+': '+obj.getDescription() for obj in self.__inventory]))

    def executeTakeCommand(self, obj):

        self.__currentRoom.removeObject(obj)

        self.__inventory.append(obj)

    def executeDropCommand(self, obj):

        self.__inventory.remove(obj)

        self.__currentRoom.addObject(obj)

    @classmethod
    def readFromFile(cls, roomFile, objFile, synonymFile):

        rooms, room = {}, AdvRoom.readFromFile(roomFile)

        while room is not None:

            rooms[room.getRoomNumber()] = room

            room = AdvRoom.readFromFile(roomFile)

        objs, obj = {}, AdvObject.readFromFile(objFile)

        while obj is not None:

            objs[obj.getName()] = obj

            obj = AdvObject.readFromFile(objFile)

        synonyms = {}

        for line in synonymFile:

            split = line[:-1].split('=')

            synonyms[split[0]] = split[1]

        return cls(rooms, objs, synonyms)

main()