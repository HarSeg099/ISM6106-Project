import random
import Player

class Computer(Player):
    def __init__(self, name="Computer"):
        super().__init__(name)

    def makeMove(self):
        #Return a random choise between Rock, Paper, or Scissor
        return random.choice(["Rock", "Paper", "Scissor"])
