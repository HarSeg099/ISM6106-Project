import random

class Player:
    def __init__(self):
        self._name
        self._choice

    def getChoice(self):
        return self._choice

    def setChoice(self, chosen):
        self._choice = chosen

class Person(Player):
    def __init__(self):
        self._name = 'Human'
        self._choice = None

    def getChoice(self):
        return self._choice

    def setChoice(self, chosen):
        self._choice = chosen

class Computer(Player):
    def __init__(self):
        self._name = 'PC'
        self._choice = None
        #self._generator = random()
    
    def generateChoice(self):
        #ranNum = 2
        ranNum = random.randint(1,3)
        return ranNum

    def setChoice(self, chosen):
        if chosen == 1:
            self._choice = 'Paper'
        elif chosen == 2:
            self._choice = 'Scissor'
        else:
            self._choice = 'Rock'

    def getChoice(self):
        return self._choice
