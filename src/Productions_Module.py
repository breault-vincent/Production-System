#-------------------------------------------------------------------------------
# Name:        Productions_Module
# Purpose:     Defines the various productions to be used in the simulation,
#               along with a knowledge database to be used by the agents.
#
# Authors:     Vincent Breault & Drew Blackmore
#
# Created:     2014-04-15
#-------------------------------------------------------------------------------


class Production:
    '''The form of a production in our system.

        ID is the production's name.
        
        leftSideTrue is a list of facts that must be true in order for the production to be legal.
        leftSideFalse is a list of facts that cannot be true in order for the production to be legal.

        rightSideAdd is a list of facts that, when fired, the production adds to the environment.
        rightSideDel is a list of facts that, when fired, the production removes from the environment.

        requirement is a string that describes what types of agents may use the production.
         It was not used in our particular simulation.'''

    def __init__(self, ID, leftSideTrue, leftSideFalse, rightSideAdd, rightSideDel, requirement):
        self.ID = ID
        self.requirement = requirement
        self.leftSideTrue = leftSideTrue
        self.leftSideFalse = leftSideFalse
        self.rightSideAdd = rightSideAdd
        self.rightSideDel = rightSideDel
#End class Production.


#The following function simply returns the list of productions used in our simulation.
# You will notice a quirk about it, however.
# Namely, the productions it returns involve general terms,
# such as 'OtherPlayer' or 'AnyBall'.
# In order to create variability in our productions,
# such general terms are specified by the interpreter.
def instantiateProduction():
    "Returns the list of generalized productions used by the agents in our Dodge Ball simulation."

    throwBall = Production('throwBall',[['CurrentPlayer', 'Carrying', 'PlayerBall']], [['CurrentPlayer', 'Is_In', 'Jail'], ['OtherPlayer', 'Is_In', 'Jail']], [['PlayerBall', 'Flying_At', 'OtherPlayer']], [['CurrentPlayer', 'Carrying', 'PlayerBall']], 'kitty')
    pickUpBall = Production('pickUpBall', [['AnyBall', 'Is_In', 'CurrentPlayerCourt']], [['CurrentPlayer', 'Carrying', 'PlayerBall'], ['CurrentPlayer', 'Is_In', 'Jail']], [['CurrentPlayer', 'Carrying', 'AnyBall']], [['AnyBall', 'Is_In', 'CurrentPlayerCourt']], 'kitty')
    blockBall = Production('blockBall', [['AnyBall', 'Flying_At', 'CurrentPlayer'], ['CurrentPlayer', 'Carrying', 'PlayerBall']], [['CurrentPlayer', 'Is_In', 'Jail']], [['AnyBall', 'Is_In', 'CurrentPlayerCourt']], [['AnyBall', 'Flying_At', 'CurrentPlayer']], 'kitty')
    dodgeBall = Production('dodgeBall', [['AnyBall', 'Flying_At', 'CurrentPlayer']], [['CurrentPlayer', 'Is_In', 'Jail']], [['AnyBall', 'Is_In', 'CurrentPlayerCourt']], [['AnyBall', 'Flying_At', 'CurrentPlayer']], 'kitty')
    catchBall = Production('catchBall', [['AnyBall', 'Flying_At', 'CurrentPlayer']], [['CurrentPlayer', 'Is_In', 'Jail'], ['CurrentPlayer', 'Carrying', 'PlayerBall']], [['CurrentPlayer', 'Carrying', 'AnyBall']], [['AnyBall', 'Flying_At', 'CurrentPlayer']], 'kitty')
    doNothing = Production('doNothing', [], [], [], [], 'kitty')


    dodgeBallProductions = [throwBall, pickUpBall, blockBall, dodgeBall, catchBall, doNothing]
    return dodgeBallProductions


class Knowledge:
    '''Each instance of the knowledge class represents a single piece of causal knowledge.
        In our system, causal knowledge takes the form of conditional statements.

        The condition is the antecedent.
        The result is the consequent.
        They are both rendered as three-part facts in a list, similar to Chunk3s.

        Therefore, any agent endowed with a piece of knowledge
         understands that any action that brings about the condition
         ultimately leads to the result.'''

    def __init__(self, ID, condition, result):
        self.ID = ID
        self.condition = condition
        self.result = result
#End class Knowledge.
        

#The following function simply instantiates the knowledge we used in our simulation.
# That knowledge concerns what happens either when a player is hit by a ball,
# or when the player successfully lands a hit on another player using a ball.
def instantiateKnowledge():

    getHit = Knowledge('getHit', [['AnyBall', 'Flying_At', 'CurrentPlayer']], [['CurrentPlayer', 'Is_In', 'Jail']])
    makeHit = Knowledge('makeHit', [['PlayerBall', 'Flying_At', 'OtherPlayer']], [['OtherPlayer', 'Is_In', 'Jail']])

    dodgeBallKnowledge = [getHit, makeHit]
    return dodgeBallKnowledge
