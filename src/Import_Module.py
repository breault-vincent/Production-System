#-------------------------------------------------------------------------------
# Name:        Import_Module
# Purpose:     Imports the information from the database
#               and uses it to set the initial conditions of the simulation.
#
# Authors:     Vincent Breault & Drew Blackmore
#
# Created:     2014-04-15
#-------------------------------------------------------------------------------


#This module uses every other one,
# as it does the heavy lifting of initializing the simulation.
import Chunk_Module
import Game_Module
import Interpreter_Module
import Productions_Module
import operator

#Creates an empty list of agents, to be used by both functions below.
listOfAgents = []


#This function imports the database
# and uses it to generate the initial conditions of the game.

#In order for the database to generate players and balls,
# it must include at least the following two lines:
#       Environment Contains Ball_{0}
#       Environment Contains Player_{0}
def importDatabase(filename, numberOfBalls, numberOfPlayers):
    '''Opens up the specified Dodge Ball database,
        imports the information it contains,
        and generates the start condition of the game.'''


    #Creates an empty enviornment.
    court = Chunk_Module.Environment([])

    #Imports the database
    database = open(filename)
    print ''
    print filename, "successfully opened."
    print ''

    #Establishes the empty list of balls, players, and pandas.
    ballList = []
    playerList = []

    for line in database:
        newline = line.split()
        if "Ball_{0}" in newline[2]:
            counter = 1
            #Populates the environment with a number of dodge balls.
            for item in range(numberOfBalls):
                theThingx = newline[0]
                theRelation = newline[1]
                theThingy = newline[2].format(counter)
                counter = counter + 1
                theChunkID = theThingx, theRelation, theThingy
                Chunk_Module.Chunk3(court, theChunkID, theThingx, theRelation, theThingy)
                ballList.append(theThingy)
        elif "Player_{0}" in newline[2]:
            counter = 1
            #Populates the environment with a number of players.
            for item in range(numberOfPlayers):
                theThingx = newline[0]
                theRelation = newline[1]
                theThingy = newline[2].format(counter)
                counter = counter + 1
                theChunkID = theThingx, theRelation, theThingy
                Chunk_Module.Chunk3(court, theChunkID, theThingx, theRelation, theThingy)
                playerList.append(theThingy)
        else:
            #Populates the environment with every other fact stated in the database.
            theThingx = newline[0]
            theRelation = newline[1]
            theThingy = newline[2]
            theChunkID = theThingx, theRelation, theThingy
            Chunk_Module.Chunk3(court, theChunkID, theThingx, theRelation, theThingy)

    #Turns balls and players into instances of Ball and Player classes.
    # Also splits the players into teams, and assigns starting positions to both balls and players.
    counter = 1
    for item in ballList:
        if counter <= (len(ballList))/2:
            theThingx = item
            theRelation = 'Is_In'
            theThingy = 'Red_Court'
            theChunkID = theThingx, theRelation, theThingy
            Chunk_Module.Chunk3(court, theChunkID, theThingx, theRelation, theThingy)
            counter = counter + 1
        else:
            theThingx = item
            theRelation = 'Is_In'
            theThingy = 'Blue_Court'
            theChunkID = theThingx, theRelation, theThingy
            Chunk_Module.Chunk3(court, theChunkID, theThingx, theRelation, theThingy)
            counter = counter + 1

    counter = 1
    for item in playerList:
        kitty = Game_Module.Player(item, 'kitty', Productions_Module.instantiateProduction(), Productions_Module.instantiateKnowledge())
        #Note below that each instance of the player class is also appended
        # to the listOfAgents.  This list is used by Run_Program.
        listOfAgents.append(kitty)
        if counter <= (len(playerList))/2:
            theThingx = item
            theRelation = 'Is_On'
            theThingy = 'Red_Team'
            theChunkID = theThingx, theRelation, theThingy
            Chunk_Module.Chunk3(court, theChunkID, theThingx, theRelation, theThingy)
            theRelation = 'Is_In'
            theThingy = 'Red_Court'
            theChunkID = theThingx, theRelation, theThingy
            Chunk_Module.Chunk3(court, theChunkID, theThingx, theRelation, theThingy)
            counter = counter + 1
        else:
            theThingx = item
            theRelation = 'Is_On'
            theThingy = 'Blue_Team'
            theChunkID = theThingx, theRelation, theThingy
            Chunk_Module.Chunk3(court, theChunkID, theThingx, theRelation, theThingy)
            theRelation = 'Is_In'
            theThingy = 'Blue_Court'
            theChunkID = theThingx, theRelation, theThingy
            Chunk_Module.Chunk3(court, theChunkID, theThingx, theRelation, theThingy)
            counter = counter + 1

    #Closes the database, prints the starting conditions of the simulation,
    # and returns the environment - which is used by Run_Program.
    database.close()
    for item in court.facts:
        print item.ID
    return court


#The two functions below create the ideal environments each team strives for.
# Each is its own instance of the Environment class,
# but is drastically simplified.
def createRedGoal(numberOfPlayers):

    redTeamGoal = Chunk_Module.Environment([])
    counter = 1

    #The ideal state for Red_Team is to have all of its players on Red_Court,
    # and all of the opposing players in Jail.
    for i in range(numberOfPlayers):
        if counter <= (numberOfPlayers/2):
            theThingx = "Player_{0}".format(counter)
            theRelation = "Is_In"
            theThingy = "Red_Court"
            theChunkID = theThingx, theRelation, theThingy
            Chunk_Module.Chunk3(redTeamGoal, theChunkID, theThingx, theRelation, theThingy)
            counter = counter + 1
        else:
            theThingx = "Player_{0}".format(counter)
            theRelation = "Is_In"
            theThingy = "Jail"
            theChunkID = theThingx, theRelation, theThingy
            Chunk_Module.Chunk3(redTeamGoal, theChunkID, theThingx, theRelation, theThingy)
            counter = counter + 1
    return redTeamGoal

def createBlueGoal(numberOfPlayers):

    blueTeamGoal = Chunk_Module.Environment([])
    counter = 1

    #The ideal state for Blue_Team is to have all of its players on Blue_Court,
    # and all of the opposing players in Jail.
    for i in range(numberOfPlayers):
        if counter <= (numberOfPlayers/2):
            theThingx = "Player_{0}".format(counter)
            theRelation = "Is_In"
            theThingy = "Jail"
            theChunkID = theThingx, theRelation, theThingy
            Chunk_Module.Chunk3(blueTeamGoal, theChunkID, theThingx, theRelation, theThingy)
            counter = counter + 1
        else:
            theThingx = "Player_{0}".format(counter)
            theRelation = "Is_In"
            theThingy = "Blue_Court"
            theChunkID = theThingx, theRelation, theThingy
            Chunk_Module.Chunk3(blueTeamGoal, theChunkID, theThingx, theRelation, theThingy)
            counter = counter + 1
    return blueTeamGoal


#This function simply returns the list of agents.
def returnListOfAgents():
    return listOfAgents







