#-------------------------------------------------------------------------------
# Name:        Interpreter_Module
# Purpose:     Specifies general productions, determines which specified
#               productions are legal, and returns the best specific production
#               to fire (using a point-based ranking system).
#
# Authors:     Vincent Breault & Drew Blackmore
#
# Created:     2014-04-15
#-------------------------------------------------------------------------------


#The built-in Operater and Copy modules are necessary for this module to run.
import operator
import copy


#The following function takes the generalized productions and knowledge
# found in the Productions_Module and specifies them, turning statements
# like 'OtherPlayer' or 'AnyBall' into specific designators,
# such as 'Player_2' or 'Ball_3'.
def specifier(listOfThingToSpecify, agent, environment, playerTotal, ballCount):
    '''listOfThingToSpecify is the general production or pieces of knowledge that requires specification.

        agent is the player running the production or making use of the knowledge.
        environment is the environment which will be affected by the specified productions.

        playerTotal is the number of agents in the game.
        ballCount is the number of balls in play.
         These last two are necessary because the function points out specific players and balls.'''
    

    #Determining the location of the agent using the production or knowledge is important.
    # It allows the function to specify statements like 'CurrentPlayerCourt' or 'OtherPlayerCourt',
    # replacing them with the actual location of the agent or the agent's opponent.
    for facts in environment.facts:
        if agent.ID in facts.ID and 'Is_In' in facts.ID:
            agentLocation = facts.thingY


    #This loop goes through a production or piece of knowledge given to it,
    # and specifies 'CurrentPlayer' to the agent given as an argument in the
    # main function call.
    # It also specifies 'PlayerBall' to the ball held by the agent given
    # as an argument in the main function call, and uses the loop above
    # to determine the location of the agent or agent's opponent.
    for productions in listOfThingToSpecify:
            for attributes in dir(productions):
                if '_' not in attributes:
                    if hasattr(getattr(productions,attributes), '__iter__'):
                        for facts in getattr(productions,attributes):
                            if isinstance(getattr(productions,attributes), list):
                                if len(facts) > 0:
                                    for word in range(3):
                                        if facts[word] == 'CurrentPlayer':
                                            facts[word] = agent.ID
                                        if facts[word] == 'PlayerBall':
                                            for statements in environment.facts:
                                                if agent.ID in statements.ID and 'Carrying' in statements.ID:
                                                    try:
                                                        facts[word] = statements.thingY
                                                    except:
                                                        continue
                                        if facts[word] == 'CurrentPlayerCourt':
                                            facts[word] = agentLocation
                                        elif facts[word] == 'OtherPlayerCourt':
                                            if agentLocation == 'Red_Court':
                                                facts[word] = 'Blue_Court'
                                            else:
                                                facts[word] = 'Red_Court'

    #Prepares an empty list for the agent-specific productions.
    variableProductionList = []

    #Goes through the copy of the agent's production list.
    # Replaces every instance of "OtherPlayer" with an actual player ID,
    # such as "Player_1".  This is done for each player in the game.
    for productions in listOfThingToSpecify:
        playerChange = 'notNeeded'
        ballChange = 'notNeeded'

        for attributes in dir(productions):
            if '_' not in attributes:
                if isinstance(getattr(productions,attributes), list):
                    for facts in getattr(productions,attributes):
                        if len(facts) > 0:
                            for word in range(3):
                                if facts[word] == 'OtherPlayer':
                                    playerChange = 'needed'
                                if facts[word] == 'AnyBall':
                                    ballChange = 'needed'

        #The playerChange and ballChange variables are included
        # in order to cut down on the number of nested loops.
        if playerChange == 'notNeeded' and ballChange == 'notNeeded':
            variableProductionList.append(productions)

        #When playerChange is 'needed', the function specifies 'OtherPlayer'
        # to some player that is not the agent given as an argument in the main
        # function call.
        if playerChange == 'needed':
            for i in range(playerTotal):
                newProduction = copy.deepcopy(productions)
                for attributes in dir(newProduction):
                    if '_' not in attributes:
                        if isinstance(getattr(newProduction,attributes), list):
                            for facts in getattr(newProduction,attributes):
                               for word in range(3):
                                    if facts[word] == 'OtherPlayer':
                                        facts[word] = 'Player_' + str(i+1)
                                        newProduction.ID = newProduction.ID+str(i+1)
                variableProductionList.append(newProduction)

        #When ballChange is 'needed', the function specifies 'AnyBall'
        # to some ball that is not the ball held by the agent given as an argument
        # in the main function call.
        if ballChange == 'needed':
            for i in range(ballCount):
                newProduction = copy.deepcopy(productions)
                for attributes in dir(newProduction):
                    if '_' not in attributes:
                        if isinstance(getattr(newProduction,attributes), list):
                            for facts in getattr(newProduction,attributes):
                               for word in range(3):
                                    if facts[word] == 'AnyBall':
                                        facts[word] = 'Ball_' + str(i+1)
                                        newProduction.ID = newProduction.ID+str(i+1)

                #Finally, all these agent-specific productions are appended to a single list.
                # This list is used to determine legal productions below,
                # and is cleared when the next agent acts.
                variableProductionList.append(newProduction)
    return variableProductionList


#Uses the specified productions to create a list of legal productions,
# and then ranks those productions through a point-assignment method.
def chooseProduction(agent, environment, myListOfGoals, enemyListOfGoals, playerTotal, ballCount):
    '''agent is the player running the production or making use of the knowledge.
        environment is the environment which will be affected by the specified productions.

        myListOfGoals is the ideal environment the agent is choosing productions in an attempt to reach.
        enemyListOfGoals is the environment (ideal for the enemy) that the agent is attempting to avoid.

        playerTotal is the number of agents in the game.
        ballCount is the number of balls in play.'''
    

    #Makes a copy of the agent's production list.
    # And then runs the specifier function on those copies.
    productionListCopy = copy.deepcopy(agent.listOfProductions)
    agentKnowledgeCopy = copy.deepcopy(agent.knowledge)
    variableProductionList = specifier(productionListCopy, agent, environment, playerTotal, ballCount)
    variableAgentKnowledge = specifier(agentKnowledgeCopy, agent, environment, playerTotal, ballCount)

    #Prepares an empty dictionary for the list of legal productions an agent may take.
    listOfLegalProductions = {}
    

    #Since each fact in the productions or knowledge is expressed as a list,
    # the interpreter must convert them to tuples after specifying them,
    # as Chunk3 IDs are expressed as tuples (and we want to compare the
    # facts with them).
    for productions in variableProductionList:
        for attributes in dir(productions):
            if '_' not in attributes:
                if isinstance(getattr(productions,attributes), list):
                    if hasattr(getattr(productions,attributes), '__iter__'):
                        for var, facts in enumerate(getattr(productions,attributes)):
                            getattr(productions,attributes)[var] = tuple(facts)

    #A copy of the tupled productions/knowledge is made,
    # as the knowledge is later used to modify the productions,
    # and unmodified versions must exist to be returned.
    productionClone = copy.deepcopy(variableProductionList)

    for knowledge in variableAgentKnowledge:
        for attributes in dir(knowledge):
            if '_' not in attributes:
                if isinstance(getattr(knowledge,attributes), list):
                    if hasattr(getattr(knowledge,attributes), '__iter__'):
                        for var, facts in enumerate(getattr(knowledge,attributes)):
                            getattr(knowledge,attributes)[var] = tuple(facts)


    #This loop constructs the list of legal productions.
    for productions in variableProductionList:
        #Takes for granted the production is not legal
        legal = 0

        #Checks leftsideTru, which is the pre-requ statements that must be there for the production
        for left in productions.leftSideTrue:
            for chunk3 in environment.facts:
                if chunk3.ID == left:
                    legal += 1

        #Checks if a statement that shouldn't exist can be found in environment
        for left in productions.leftSideFalse:
            for chunk3 in environment.facts:
                if chunk3.ID == left:
                    legal -= 1

        if legal == len(productions.leftSideTrue):
            listOfLegalProductions[productions] = 0


    #Consequences of some actions are indirect, so they're checked against a knowledge base.
    # This modifies the productions, making their indirect causes direct.  For example,
    # 'throwBall' causes the ball you've thrown to go flying through the air at your target.
    # The knowledge states that a ball flying through the air at a target will result in the
    # target being sent to jail.

    #Thus, the knowledge would alter any production that caused a ball to go flying through
    # the air to instead immediately cause its target to go to jail.
    # This modification is what allows the agent to think ahead and choose productions that
    # will move it closer to its goal state, even if not immediately.

    #However, the productions remain modified, which is why they were copied earlier into
    # the list 'productionClone'.  Thus, only the ID of the modified production needs to be
    # returned, and the unmodifed copy is what will fire.
    for production in listOfLegalProductions:
        for knowledge in variableAgentKnowledge:
            for addedResult in production.rightSideAdd:
                if addedResult == knowledge.condition[0]:
                    production.rightSideAdd[production.rightSideAdd.index(addedResult)] = knowledge.result[0]
            for deletedResult in production.rightSideDel:
                if deletedResult == knowledge.condition[0]:
                    production.rightSideDel[production.rightSideDel.index(deletedResult)] = knowledge.result[0]


    #The following loop assigns point values to each production in the list of legal productions,
    # as modified by the knowledge base.
    
    #Productions that add to the environment some fact in the agent's ideal goal state
    # are worth +1 point for each such fact added.
    
    #Productions that add to the environment some fact in the enemy's ideal goal state
    # are worth -1 point for each such fact added.
    
    #Productions that remove from the environment some fact in the enemy's ideal goal state
    # are worth +1 point for each such fact added.
    for productions in listOfLegalProductions:
        for right in productions.rightSideAdd:
            for facts in myListOfGoals.facts:
                if right == facts.ID:
                    listOfLegalProductions[productions] +=1
        for right in productions.rightSideDel:
            for facts in myListOfGoals.facts:
                if right == facts.ID:
                    listOfLegalProductions[productions] -=1
            for facts in enemyListOfGoals.facts:
                if right == facts.ID:
                    listOfLegalProductions[productions] +=1
        #For a test, the 11 above lines were ablated and replaced with the code below.
        # Note that, in the replacement, point values are raised and lowered by zero,
        # leaving them actually unchanged.
        
        #The output from the Ablation test is included as a .txt file titled
        # 'ConflictResolution_Ablation_Output.txt'

#        for right in productions.rightSideAdd:
#            for facts in myListOfGoals.facts:
#                if right == facts.ID:
#                    listOfLegalProductions[productions] +=0
#        for right in productions.rightSideDel:
#            for facts in myListOfGoals.facts:
#                if right == facts.ID:
#                    listOfLegalProductions[productions] -=0
#            for facts in enemyListOfGoals.facts:
#                if right == facts.ID:
#                    listOfLegalProductions[productions] +=0
#
#End Ablation


    #This brief loop hard-codes in the knowledge that doing something is
    # always better than doing nothing.  It was somewhat system-specific,
    # so we separated it out from the rest of the point-assignment loop.
    if len(listOfLegalProductions)>1:
        for stuff in listOfLegalProductions:
            if stuff.ID == 'doNothing':
                listOfLegalProductions[stuff] = -1

    #Finally, the ID of the most highly-ranked, knowledge-modified specific production is saved,
    # and then that production is found in the copied list and the unmodified version is returned.
    bestProduction = max(listOfLegalProductions.iteritems(), key=operator.itemgetter(1))[0].ID

    for productions in productionClone:
        if productions.ID == bestProduction:
            return productions
