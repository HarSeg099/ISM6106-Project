import Player

class Person(Player):
    def __init__(self, name):
        super().__init__(name)

    def getInput(self, buttonInput):
        print('This would get the button input from human player.')
