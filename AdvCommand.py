from abc import ABC, abstractmethod

class AdvCommand(ABC):

    @abstractmethod
    def execute(self, game, obj):

        pass
    

class AdvMotionCommand(AdvCommand):

    def __init__(self, direction):

        self.__direction = direction

    def execute(self, game, obj = None):

        game.executeMotionCommand(self.__direction)
        

class QUIT(AdvCommand):

    def execute(self, game, obj = None):

        game.executeQuitCommand()
        

class LOOK(AdvCommand):

    def execute(self, game, obj = None):

        game.executeLookCommand()
        

class INVENTORY(AdvCommand):

    def execute(self, game, obj = None):

        game.executeInventoryCommand()
        

class TAKE(AdvCommand):

    def execute(self, game, obj):

        game.executeTakeCommand(obj)
        

class DROP(AdvCommand):

    def execute(self, game, obj):

        game.executeDropCommand(obj)


class HELP(AdvCommand):

    def execute(self, game, obj = None):

        game.executeHelpCommand()
