class AdvMotionTableEntry:

    def __init__(self, direction, roomNum, key = None):

        self.__direction = direction.upper()
        self.__roomNum = roomNum
        self.__key = None if key is None else key.upper()

    def getDirection(self):

        return self.__direction

    def getDestinationRoom(self):

        return self.__roomNum

    def getKeyName(self):

        return self.__key
