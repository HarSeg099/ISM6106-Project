"""
A basic template file for using the Model class in PicoLibrary
This will allow you to implement simple Statemodels with some basic
event-based transitions.

Currently supports only 4 buttons (hardcoded to BTN1 through BTN4)
and a TIMEOUT event for internal tranisitions.

For processing your own events such as sensors, you can implement
those in your run method for transitions based on sensor events.
"""

# Import whatever Library classes you need - Model is obviously needed
import time
import random
from Game import *
from StateModel import *
from Button import *
from Counters import *
from Log import *
from Displays import *
from Buzzer import *

"""
This is the template Model Runner - you should rename this class to something
that is supported by your class diagram. This should associate with your other
classes, and any PicoLibrary classes. If you are using Buttons, you will implement
buttonPressed and buttonReleased.

To implement the model, you will need to implement 3 methods to support entry actions,
exit actions, and state actions.

This template currently implements a very simple state model that uses a button to
transition from state 0 to state 1 then a 5 second timer to go back to state 0.
"""

class GameController:

    def __init__(self):
        
        # Instantiate whatever classes from your own model that you need to control
        # Handlers can now be set to None - we will add them to the model and it will
        # do the handling
        self._button1 = Button(10, "Paper", buttonhandler=None)
        self._button2 = Button(11, "Scissor", buttonhandler=None)
        self._button3 = Button(12, "Rock", buttonhandler=None)
        self._button4 = Button(13, "start", buttonhandler=None)

        self._display = LCDDisplay(sda=0, scl=1, i2cid=0)
        self._buzzer = PassiveBuzzer(16)
        self._game = Game()
        self._timer = SoftwareTimer(None)
        
        # Instantiate a Model. Needs to have the number of states, self as the handler
        # You can also say debug=True to see some of the transitions on the screen
        # Here is a sample for a model with 4 states
        self._model = StateModel(9, self, debug=True)
        
        # Up to 4 buttons and a timer can be added to the model for use in transitions
        # Buttons must be added in the sequence you want them used. The first button
        # added will respond to BTN1_PRESS and BTN1_RELEASE, for example
        self._model.addButton(self._button1)
        self._model.addButton(self._button2)
        self._model.addButton(self._button3)
        self._model.addButton(self._button4)
        # add other buttons (up to 3 more) if needed
        
        # Add any timer you have.
        self._model.addTimer(self._timer)
        
        # Now add all the transitions that are supported by my Model
        # obvously you only have BTN1_PRESS through BTN4_PRESS
        # BTN1_RELEASE through BTN4_RELEASE
        # and TIMEOUT
        
        # some examples:
        self._model.addTransition(0, [BTN4_PRESS], 1)
        
        self._model.addTransition(1, [BTN1_PRESS], 2)
        self._model.addTransition(1, [BTN2_PRESS], 3)
        self._model.addTransition(1, [BTN3_PRESS], 4)
        self._model.addTransition(5, [TIMEOUT], 1)
        self._model.addTransition(7, [TIMEOUT], 0)
        self._model.addTransition(8, [TIMEOUT], 0)
        # etc.
    
    """
    Create a run() method - you can call it anything you want really, but
    this is what you will need to call from main.py or someplace to start
    the state model.
    """

    def run(self):
        # The run method should simply do any initializations (if needed)
        # and then call the model's run method.
        # You can send a delay as a parameter if you want something other
        # than the default 0.1s. e.g.,  self._model.run(0.25)
        self._model.run()

    """
    stateDo - the method that handles the do/actions for each state
    """
    def stateDo(self, state):
        # Now if you want to do different things for each state you can do it:
        if state == 0:
            pass
        elif state == 1:
            # State1 do/actions
            # You can check your sensors here and perform transitions manually if needed
            # For example, if you want to go from state 1 to state 2 when the motion sensor
            # is tripped you can do something like this
            # if self.motionsensor.tripped():
            # 	gotoState(2)
            pass
        elif state in [2,3,4]:
            if self._game.compareChoices(self._game._human.getChoice(),self._game._pc.getChoice()) == True:
                time.sleep(2)
                self._model.gotoState(6)
            elif self._game.compareChoices(self._game._human.getChoice(),self._game._pc.getChoice()) == False:
                self._model.gotoState(5)
            else:
                #This is meant for troubleshooting only
                print(f'Error in State {state}')
                self._model.gotoState(0)
        elif state == 6 :
            if self._game.checkScore() == 'win':
                self._model.gotoState(7)
            elif self._game.checkScore() == 'lose':
                self._model.gotoState(8)
            else:
                self._model.gotoState(1)
        


    """
    stateEntered - is the handler for performing entry/actions
    You get the state number of the state that just entered
    Make sure actions here are quick
    """
    def stateEntered(self, state, event):
        # Again if statements to do whatever entry/actions you need
        Log.d(f'State {state} entered')
        if state == 0:
            self._display.reset()
            self._display.showText('Press White')
            self._display.showText('To Start', row=1)
        elif state == 1:
            self._display.reset()
            self._display.showText('Choose your move')
            self._display.scroll('Red = Paper  Yellow = Scissor  Blue = Rock', row=1, skip=6)
            #self._timer.start(5)
        elif state == 2:
            self._game._human.setChoice('Paper')
            self._game._pc.setChoice(self._game._pc.generateChoice())
        elif state == 3:
            self._game._human.setChoice('Scissor')
            self._game._pc.setChoice(self._game._pc.generateChoice())
        elif state == 4:
            self._game._human.setChoice('Rock')
            self._game._pc.setChoice(self._game._pc.generateChoice())
        elif state == 5:
            self._display.reset()
            self._display.showText('Tie!')
            self._display.showText('Replay the round', row = 1)
            self._buzzer.beep()
            self._timer.start(5)
        elif state == 6:
            self._display.reset()
            self._display.showText('Checking Score')
            self._timer.start(5)
        elif state == 7:
            self._display.reset()
            self._display.showText('You Won!')
            self._display.showText('Making new game', row =1)
            self._buzzer.beep(tone=1000, duration = 300)
            self._game.resetGame()
            self._timer.start(5)
        elif state == 8:
            self._display.reset()
            self._display.showText('You Lost!')
            self._display.showText('Making new game', row =1)
            self._buzzer.beep(tone=100, duration = 300)
            self._game.resetGame()
            self._timer.start(5)
            
    """
    stateLeft - is the handler for performing exit/actions
    You get the state number of the state that just entered
    Make sure actions here are quick
    
    This is just like stateEntered, perform only exit/actions here
    """

    def stateLeft(self, state, event):
        Log.d(f'State {state} exited')
        if state == 0:
            # exit actions for state 0
            pass
        elif state in [5,6,7,8]:
            self._timer.cancel()
        else:
            pass
        # etc.
    

# Test your model. Note that this only runs the template class above
# If you are using a separate main.py or other control script,
# you will run your model from there.
if __name__ == '__main__':
    MyControllerTemplate().run()