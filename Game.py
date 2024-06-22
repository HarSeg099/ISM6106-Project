from Displays import *
from Player import *
from Lights import *
from LightStrip import *
from Buzzer import *

class Game:

    def __init__(self):
      self._human = Person()
      self._pc = Computer()
      self._score = 0
      self._rounds = 0
      self._gameDisplay = LCDDisplay(sda=0, scl=1, i2cid=0)
      self._lightstrip = LightStrip(pin = 2, numleds = 8)
      self._gameBuzzer = PassiveBuzzer(16)

    def compareChoices(self, playerChoice, pcChoice):
      player1 = playerChoice
      player2 = pcChoice

      if player1 == player2:
        self._gameDisplay.reset()
        #self._gameDisplay.showText('Tie - Try again')
        return False
      elif player1 == 'Rock' and player2 == 'Scissor':
        self.winRound()
        return True
      elif player1 == 'Rock' and player2 == 'Paper':
        self.loseRound()
        return True
      elif player1 == 'Paper' and player2 == 'Scissor':
        self.loseRound()
        return True
      elif player1 == 'Paper' and player2 == 'Rock':
        self.winRound()
        return True
      elif player1 == 'Scissor' and player2 == 'Rock':
        self.loseRound()
        return True
      elif player1 == 'Scissor' and player2 == 'Paper':
        self.winRound()
        return True
      else:
        self._gameDisplay.reset()
        self._gameDisplay.showText('Error - Test')
        return False

    def winRound(self):
      self._gameDisplay.reset()
      self._gameDisplay.showText('You\'ve won')
      self._gameDisplay.showText('the round!', row=1)
      self._gameBuzzer.beep(tone=1000)
      self._lightstrip.setPixel(pixelno = self.getRounds(), color = GREEN)


      self._score = self._score + 1
      self._rounds = self._rounds + 1
    
    def loseRound(self):
      self._gameDisplay.reset()
      self._gameDisplay.showText('You\'ve lost')
      self._gameDisplay.showText('the round!', row = 1)
      self._gameBuzzer.beep(tone=100)
      self._lightstrip.setPixel(pixelno = self.getRounds(), color = RED)

      self._score = self._score - 1
      self._rounds = self._rounds + 1

    def getScore(self):
      return self._score

    def getRounds(self):
      return self._rounds

    def resetGame(self):
      self._score = 0
      self._rounds = 0
      self._lightstrip.off()

    def checkScore(self):
        if self._score == 3:
            return 'win'
        elif self._score == -3:
            return 'lose'
        elif self._score == 1 and self._rounds == 5:
            return 'win'
        elif self._score == -1 and self._rounds == 5:
            return 'lose'
        elif self._score == 2 and self._rounds == 4:
            return 'win'
        elif self._score == -2 and self._rounds == 4:
            return 'lose'
        else:
            return 'continue'
