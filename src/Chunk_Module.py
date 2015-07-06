#-------------------------------------------------------------------------------
# Name:        Chunk_Module
# Purpose:     Defines the Environment class and various Chunk classes
#
# Authors:     Vincent Breault & Drew Blackmore
#
# Created:     2014-04-15
#-------------------------------------------------------------------------------

class Environment:
    "The environment for Dodge Ball - where the game is played."

    #Facts is always renedered as a list of Chunk3s.
    def __init__(self, facts):
        self.facts = facts

    #This method removes facts from the environment.
    # It takes as input a specific fact,
    # and if it finds it in the environment,
    # it removes it.
    def removeFacts(self, factsToBeRemoved):
        for item in self.facts:
            if item.ID == factsToBeRemoved:
                self.facts.remove(item)

    #This method adds facts to the environment.
    # It takes as input a specific fact,
    # and if it can't find a duplicate of it in the environment,
    # it adds it as a Chunk3.
    def addFacts(self, factsToBeAdded):
        duplicateFound = 0
        for item in self.facts:
            if item.ID == factsToBeAdded:
                duplicateFound = 1
        if duplicateFound == 0:
            Chunk3(self, factsToBeAdded, factsToBeAdded[0], factsToBeAdded[1], factsToBeAdded[2])
#End class Environment.



#We did not modify the Chunk class.
class Chunk:
    "a bit of memory."

    def __init__(self, ID, activation=0.0):
        '''creates a new instance of a chunk

        ID is a string that identifies the chunk, it's identifier
        activation is an optional argument that takes a number between 0.0 and 1.0'''
        self.ID = ID
        self.activation = activation

    def addToActivation(self, addend):
        '''adds the addend to the activation of the chunk and returns the new activation

        addend is a number between -1.0 and 1.0'''
        self.activation = self.activation + addend
        if self.activation > 1.0:
            self.activation = 1.0
        if self.activation < 0.0:
            self.activation = 0.0
        return self.activation
#End class Chunk.


#We did not modify the Chunk1 class.
# We also didn't use it (as Chunk3s are better).
class Chunk1(Chunk):
    "a bit of memory that has only one part."

    def __init__(self, environment, ID, thingX=0.0, activation=0.0):
        '''creates a new instance of a chunk1, which is a single concept in memory

        ID is a string that identifies it
        thingX is a string that shows what the chunk represents
        activation is a number between 0.0 and 1.0'''
        # indicates whether the chunk is a chunk1 or a chunk3
        self.chunkType = 1
        self.ID = ID
        ## thingX should never be a number. If it is, it's going to be 0.0,
        ##   the default when nothing else is entered.
        ##   When this happens, make thingX equal to the ID.
        if thingX == 0.0:
            self.thingX= self.ID
        else:
            self.thingX = thingX
        self.activation = activation
        environment.facts.append(self)
#End class Chunk1.


#We did not modify the Chunk3 class.
class Chunk3(Chunk):
    "A fact that has 3 parts."
    def __init__(self, environment, ID, thingX, relation, thingY, activation=0.0):
        '''creates a new instance of a chunk3, which is a 3-part fact

        environment is where the fact is stored
        ID is a string that identifies it
        thingX is one of the two concepts in the fact
        thingY is the other concept
        relation is a description of how thingX and thingY are related
        activation is a number between 0.0 and 1.0'''
        # indicates whether the chunk is a chunk1 or a chunk3
        self.chunkType = 3
        self.ID = ID
        self.thingX = thingX
        self.relation = relation
        self.thingY = thingY
        self.activation = activation
        environment.facts.append(self)
#End class Chunk3
