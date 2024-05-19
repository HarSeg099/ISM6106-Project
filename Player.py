class Player:
    def __init__(self, name):
        self._name = name
        self._score = 0
        self._move = ''

    def makeMove(self):
        raise NotImplementedError("Subclasses should implement this!")

    def getMove(self):
        return print('This would get the move of a player')

    def resetScore(self):
        return print('This would reset the score for the specified player; may become part of the Game class.')
