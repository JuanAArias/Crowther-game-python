from AdvMotionTableEntry import *

class AdvRoom:

    def __init__(self, num, name, description, motionTable):

        self.__num = num
        self.__name = name
        self.__description = description        
        self.__motionTable = motionTable
        self.__objList = []
        self.__flag = False

    def getRoomNumber(self):

        return self.__num

    def getName(self):

        return self.__name

    def getDescription(self):

        return self.__description

    def addObject(self, obj):

        self.__objList.append(obj)

    def removeObject(self, obj):

        self.__objList.remove(obj)

    def containsObject(self, obj):

        return obj in self.__objList

    def getObjectCount(self):

        return len(self.__objList)

    def setVisited(self, flag):

        self.__flag = flag

    def hasBeenVisited(self):

        return self.__flag

    def getMotionTable(self):

        return self.__motionTable

    def display(self):

        if not self.hasBeenVisited():

            print('\n'.join(self.getDescription()))

            self.setVisited(True)

        else:

            print(self.getName())

        for obj in self.__objList:

            name = obj.getName().lower()

            p = 'are' if name.endswith('s') else 'is a'

            print('There {0} {1} here.'.format(p, name))

    @classmethod
    def readFromFile(cls, file):

        num = file.readline()

        if num == '':

            return None

        if num.isspace():
            
            num = int(file.readline()[:-1])
            
        else:
            
            num = int(num[:-1])
            
        name, description = file.readline()[:-1], []

        line = file.readline()

        while '--' not in line:

            description.append(line[:-1])

            line = file.readline()
        
        line, motionTable = file.readline(), []

        while not line.isspace() and line != '':
            
            line = line[:-1].split()

            key = None

            if '/' in line[1]:

                s = line[1].split('/')

                line[1] = s[0]

                key = s[1]

            motionTable.append(AdvMotionTableEntry(line[0], int(line[1]), key) )

            line = file.readline()
            
        return cls(num, name, description, motionTable)
