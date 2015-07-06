#-------------------------------------------------------------------------------
# Name:        Run_Program
# Purpose:     Runs the Dodge Ball Simulation
#
# Authors:     Vincent Breault & Drew Blackmore
#
# Created:     2014-04-15
#-------------------------------------------------------------------------------


#In order to run the simulation, every module we wrote must be imported.
# So must the built-in modules operator, copy, and time, as we use them.
import Chunk_Module
import Game_Module
import Interpreter_Module
import Productions_Module
import Import_Module
import operator
import copy
import time


#This function initializes and runs the simulation itself.
def main():
    print "How many Kitties are playing per team?"
    print "There must be at least 1."
    playerCount = input()*2
    print "How many balls does each team receive?"
    print "There must be at least 1."
    ballCount = input()*2
    print "Please type in the full filename of the database you with to use (in quotes)."
    print "(For Purposes of the project, please input exactly the following: 'Database.txt')"
    fileName = input()
    time.sleep(1)

    playerTotal = playerCount

    #The following creates the environment,
    # the ideal state of the environment each team strives for,
    # a small knowledge database given to each player,
    # and a list of the players.
    court = Import_Module.importDatabase(fileName, ballCount, playerCount)
    redTeamGoal = Import_Module.createRedGoal(playerCount)
    blueTeamGoal = Import_Module.createBlueGoal(playerCount)
    dodgeBallKnowledge = Productions_Module.instantiateKnowledge()
    listOfAgents = Import_Module.returnListOfAgents()
    time.sleep(6)
    print ''


    #This loop is what simulates the game of dodge-ball,
    # with each player choosing one action (production) each for each iteration of the loop.
    notDone = True
    listOfActions = {}
    while notDone == True:

        listOfActionsToremove = []

        #This function is what causes throwing a ball to take two iterations
        # of the loop to hit a player.  When the throwBall action is taken,
        # the ball thrown begins flying through the air at its target,
        # and within the listOfActions, the throwBall action's value is increased by 1.
        # Once the the throwBall action's value is higher than 2,
        # it is marked for removal from the environment.



        for actions in listOfActions:
            for items in actions.rightSideAdd:
                flightIncrement = 'notNeeded'
                if 'Flying_At' in items and listOfActions[actions] <= 2:
                    for facts in court.facts:
                        if items == facts.ID:
                            flightIncrement = 'needed'
                    if flightIncrement == 'needed':
                        listOfActions[actions]+=1
                    else:
                        listOfActionsToremove.append(actions)
                else:
                    listOfActionsToremove.append(actions)

        #This is where throwBall actions that have been ongoing
        # for a sufficient amount of time are removed.
        for items in listOfActionsToremove:
            del listOfActions[items]



        #This function is what causes a ball that has been flying through the air
        # for a turn to hit its target.  It goes through the list of actions looking for any
        # statement concerning balls in flight that have persisted for two iterations
        # of the main loop.  If it finds any, it causes them to hit their targets,
        # which sends that target to jail and causes the ball to land on the target's
        # side of the court.
        for actions in listOfActions:
            for items in actions.rightSideAdd:
                if 'Flying_At' in items and listOfActions[actions] == 3:
                    court.removeFacts(items)
                    ball = items[0]
                    playerThatDied = items[2]
                    for facts in court.facts:
                        if playerThatDied in facts.ID and 'Is_On' in facts.ID:
                            colourOfPlayerThatDied = facts.thingY
                    if 'Red_Team' in colourOfPlayerThatDied:
                        court.addFacts((ball, 'Is_In', 'Red_Court'))
                        court.removeFacts((playerThatDied, 'Is_In', 'Red_Court'))
                    elif 'Blue_Team' in colourOfPlayerThatDied:
                        court.addFacts((ball, "Is_In", 'Blue_Court'))
                        court.removeFacts((playerThatDied, 'Is_In', 'Blue_Court'))

                    court.addFacts((playerThatDied, 'Is_In', 'Jail'))
                    print ''
                    print playerThatDied, 'was sent to Jail!'
                    print ''
                    for facts in court.facts:
                        if playerThatDied in facts.ID and 'Carrying' in facts.ID:
                            court.removeFacts(facts)
        print ''
        time.sleep(4)

        #All of the above functions must occur before each player takes their actions,
        # as they involve curating the facts in the environment.
        # The players take their actions via the functions below.


        #This function determines the team of each player,
        # and then has each player choose which production to fire,
        # based upon the goal of the team they belong to.
        for players in listOfAgents:
            for facts in court.facts:
                if players.ID in facts.ID and 'Is_On' in facts.ID:
                    agentTeam = facts.thingY

            if agentTeam == 'Red_Team':
                listOfActions[Interpreter_Module.chooseProduction(players, court, redTeamGoal, blueTeamGoal, playerTotal, ballCount)] = 0

            else:
                listOfActions[Interpreter_Module.chooseProduction(players, court, blueTeamGoal, redTeamGoal, playerTotal, ballCount)] = 0

        #Following each player choosing their action,
        # the consequences of those actions occur,
        # either adding or removing facts from the environment.
        # As facts in the environment change, they are printed out,
        # along with player actions.

        #Note that player actions have numbers on the end.
        # Those numbers are meaningless and are simply there
        # for the purposes of the program.
            stuffToDelete = []
            for actions in listOfActions:
                if listOfActions[actions] == 0:
                    print players.ID + 'uses: ' + actions.ID
                    print ''
                    for addFacts in actions.rightSideAdd:
                        court.addFacts(addFacts)
                    for removeFacts in actions.rightSideDel:
                        court.removeFacts(removeFacts)
                    for facts in actions.rightSideAdd:
                        if 'Flying_At' in facts:
                            listOfActions[actions] += 1
                    if listOfActions[actions] == 0:
                        stuffToDelete.append(actions)
                    for item in court.facts:
                        if 'Carrying' in item.ID:
                            print item.ID
                        if 'Flying_At' in item.ID:
                            print item.ID
                        if 'Is_In' in item.ID:
                            print item.ID
                    print ''
                    time.sleep(3)

            for items in stuffToDelete:
                del listOfActions[items]



        #Now that the players have taken their actions,
        # and the results of those actions have had their effects upon the environment,
        # it is time to see if either time has won via their actions this turn.


        #First, the system checks how many players are in jail.
        # This value is calculated anew every round, and not carried over
        # from round to round.
        redPlayersInJail = 0
        bluePlayersInJail = 0

        redPlayersInJail == 0
        bluePlayersInJail == 0

        #For each player, this function first calculates whether or not they're in jail.
        # If so, it determines which team that player is on,
        # and then adds 1 to the value of number of players in jail on that player's team.
        for players in listOfAgents:

            playerInJail = 0
            redPlayer = 0
            bluePlayer = 0

            playerInJail == 0
            redPlayer == 0
            bluePlayer == 0

            for statements in court.facts:
                if players.ID in statements.ID and 'Jail' in statements.ID:
                    playerInJail += 1
                if players.ID in statements.ID and "Red_Team" in statements.ID:
                    redPlayer += 1
                elif players.ID in statements.ID and 'Blue_Team' in statements.ID:
                    bluePlayer += 1

                if playerInJail == 1 and redPlayer == 1:
                    redPlayersInJail += 1
                    playerInJail -= 1
                    redPlayer -= 1
                elif playerInJail == 1 and bluePlayer == 1:
                    bluePlayersInJail += 1
                    playerInJail -= 1
                    bluePlayer -= 1


        #Winning is achieved by having the entire other team in jail,
        # so if the number of players in either jail is equal to
        # half of the players on the field, the opposing team wins.
        if redPlayersInJail == playerTotal/2:
            print 'Blue Team won!'
            notDone = False

        elif bluePlayersInJail == playerTotal/2:
            print 'Red Team Won!'
            notDone = False

        #Thus marks the end of a single turn of dodge-ball.


if __name__ == '__main__':
    main()
