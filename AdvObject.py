class AdvObject:

    def __init__(self, name, description, roomNum):

        self.__name = name
        self.__description = description
        self.__roomNum = roomNum

    def getName(self):

        return self.__name

    def getDescription(self):

        return self.__description

    def getInitialLocation(self):

        return self.__roomNum
    
    @classmethod
    def readFromFile(cls, file):

        name = file.readline()

        if name == '':

            return None
        
        if name == '\n':

            name = file.readline()[:-1]

        else:

            name = name[:-1]
        
        description = file.readline()[:-1]
        
        roomNum = int(file.readline()[:-1])

        return cls(name, description, roomNum)
