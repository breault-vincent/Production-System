#-------------------------------------------------------------------------------
# Name:        Game_Module
# Purpose:     Defines the Player class necessary to play
#               a game of Dodge Ball
#
# Authors:     Vincent Breault & Drew Blackmore
#
# Created:     2014-04-15
#-------------------------------------------------------------------------------

 
class Player:
    '''A player in the game of Dodge Ball.
        Just because, our players are actually cats.
        Please don't ask.'''

    def __init__(self, ID, raceVar, ListOfProductions, knowledge):
        '''The ID is 'Player_' followed by a number.

            The raceVar wasn't used in our final simulation,
             but could be used to support different kinds of agents
             with different sets of productions they are capable of using.

            The listOfProductions is the set of productions
             that the agent is capable of using.

            The knowledge is the agent's knowledge.  The knowledge we implemented
             tells an agent the indirect consequences of certain actions.'''
        self.ID = ID
        self.race = raceVar
        self.listOfProductions = []
        self.knowledge = []
        for facts in knowledge:
            self.knowledge.append(facts)
        if self.race == 'kitty':
            for productions in ListOfProductions:
                if 'red panda' not in productions.requirement:
                    self.listOfProductions.append(productions)
        elif self.race == 'red panda':
            for productions in ListOfProductions:
                if 'red panda' in productions.requirement:
                    self.listOfProductions.append(productions)

#End Player class.
