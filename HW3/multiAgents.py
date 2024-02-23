from util import manhattanDistance
from game import Directions
import random, util
from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.
    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.
        getAction chooses among the best options according to the evaluation function.
        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legal_moves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_idx = random.choice(best_indices) # Pick randomly among the best

        return legal_moves[chosen_idx]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.
        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.
    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.
    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.
    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    '''
    Your minimax agent (Part 1)
    '''
    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.
        Here are some method calls that might be useful when implementing minimax.
        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1
        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action
        gameState.getNumAgents():
        Returns the total number of agents in the game
        gameState.isWin():
        Returns whether or not the game state is a winning state
        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)

        def countmax(depth, gameState, index_agent):
            '''
            depth = the depth this state is in
            gameState = the state that is going to be execute
            index_agent = the index of the agent (pacman = 0, ghosts = 1~(num_agents-1))
            bestscore is either min/max score in ghost/pacman
            bestmove only matters when it comes to pacman(index_agent=0)
            countmax returns the bestscore and bestmove
            '''
            num_agents = gameState.getNumAgents() # number of agents 
            legal_moves = gameState.getLegalActions(index_agent) # legal moves of the executing state
            if not len(legal_moves): # no legal_moves = done with game at the state (win or lose)
                return self.evaluationFunction(gameState), "0" # return the points
            '''
            in each condition, scores means the scores of all childstates
            take all possible childstates from legalmove and count the min/max of it
            '''
            if depth == 1 and index_agent == num_agents-1:
                '''
                depth = 1 and index = num_agents-1 means it is the terminal state
                it is also the leaf process of the recursion function call
                simply uses the evaluationFunction to calculate the scores since it's the terminal tate
                return best_score, which is the minimum score of all posible scores
                '''
                scores = []
                for action in legal_moves:
                    GameState = gameState.getNextState(index_agent, action)
                    scores.append(self.evaluationFunction(GameState))
                best_score = min(scores)
                best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
                chosen_idx = random.choice(best_indices) # pick randomly among the best
                return best_score, legal_moves[chosen_idx]
            
            elif index_agent == 0:
                '''
                index_agent = 0 means it is the time when pacman(max_player)'s time
                countmax(depth, Gamestate, 1) is used because the ghost with index 1 starts
                return best_score (max score of scores) 
                and bestMove (which matters because the original get_action function relies on it)
                '''
                scores = []
                for action in legal_moves:
                    GameState = gameState.getNextState(0, action)
                    scores.append(countmax(depth, GameState, 1))
                best_score = max(scores)[0]
                best_indices = [index for index in range(len(scores)) if scores[index][0] == best_score]
                chosen_idx = random.choice(best_indices) # pick randomly among the best
                return best_score, legal_moves[chosen_idx]
            
            elif index_agent == num_agents-1:
                '''
                index_agent = num_agents-1 but depth ≠ 1 means the childstate is pacman in the next depth
                thus, countmax(depth-1, Gamestate, 0) is used 
                instead of countmax(depth, Gamestate, index_agent+1)
                return best_score, which is the minimum of scores.
                '''
                scores=[]
                for action in legal_moves:
                    GameState = gameState.getNextState(index_agent,action)
                    scores.append(countmax(depth-1, GameState, 0))
                best_score = min(scores)[0]
                best_indices = [index for index in range(len(scores)) if scores[index][0] == best_score]
                chosen_idx = random.choice(best_indices) # pick randomly among the best
                return best_score, legal_moves[chosen_idx]
            else:
                '''
                those 0 < index_agent < num_agent-1 (no matter the depth) would be execute here
                countmax(depth, Gamestate, index_agent+1) is used since there is no need to change depth
                and the next agent to be executed is index_agent+1
                '''
                scores=[]
                for action in legal_moves:
                    GameState = gameState.getNextState(index_agent, action)
                    scores.append(countmax(depth, GameState, index_agent+1))
                best_score = min(scores)[0]
                best_indices = [index for index in range(len(scores)) if scores[index][0] == best_score]
                chosen_idx = random.choice(best_indices) # pick randomly among the best
                return best_score, legal_moves[chosen_idx]

        # take the best move from function countmax recursively
        best_score, bestmove = countmax(self.depth,gameState,0)
        return bestmove
        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """
    
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)

        def countmax(depth, gameState, index_agent, alpha_beta):
            # alpha_beta[0] = alpha
            # alpha_beta[1] = beta
            num_agents = gameState.getNumAgents()
            legal_moves = gameState.getLegalActions(index_agent)
            if not len(legal_moves): # no legal_moves = done with game at the state (win or lose)
                return self.evaluationFunction(gameState),"0" # return the points
            if depth == 1 and index_agent == num_agents-1:
                '''
                this is a min_player, so update beta and prune if best_score(v) is less than alpha
                the updated alpha_beta list will be changed in the function that call this function
                because list is mutable
                '''
                scores = []
                best_score = float("inf")
                for action in legal_moves:
                    GameState = gameState.getNextState(index_agent, action)
                    thisScore = self.evaluationFunction(GameState)
                    scores.append(thisScore)
                    best_score = min(best_score, thisScore)
                    if best_score < alpha_beta[0]:
                        return best_score, action
                    alpha_beta[1] = min(alpha_beta[1], best_score)
                best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
                chosen_idx = random.choice(best_indices) # pick randomly among the best
                return best_score, legal_moves[chosen_idx]

            elif index_agent == 0:
                '''
                this is a max_player, so update alpha and prune if best_score is larger than beta
                the updated alpha_beta list will be changed in the function that call this function
                because list is mutable
                ab is used in order to not chanage the beta's value
                (since this is a max_player, value of beta shouldn't be changed)
                '''
                scores = []
                best_score = -float("inf")
                
                for action in legal_moves:
                    GameState = gameState.getNextState(0, action)
                    ab = [alpha_beta[0], alpha_beta[1]]
                    thisScore = countmax(depth, GameState, 1, ab)
                    scores.append(thisScore)
                    best_score = max(best_score,thisScore[0])
                    if best_score > alpha_beta[1]:
                        return best_score, action
                    ab[0] = max(ab[0], best_score)
                    alpha_beta[0] = ab[0]
                best_indices = [index for index in range(len(scores)) if scores[index][0] == best_score]
                chosen_idx = random.choice(best_indices) # pick randomly among the best
                return best_score,legal_moves[chosen_idx]
            
            elif index_agent == num_agents-1:
                '''
                this is a min_player, so update beta and prune if best_score(v) is less than alpha
                the updated alpha_beta list will be changed in the function that call this function
                because list is mutable
                '''
                scores = []
                best_score = float("inf")
                for action in legal_moves:
                    ab = [alpha_beta[0], alpha_beta[1]]
                    GameState = gameState.getNextState(index_agent, action)
                    thisScore = countmax(depth-1, GameState, 0, ab)
                    scores.append(thisScore)
                    best_score = min(best_score, thisScore[0])
                    if best_score < alpha_beta[0]:
                        return best_score, action
                    ab[1] = min(ab[1], best_score)
                    alpha_beta[1] = ab[1]
                best_indices = [index for index in range(len(scores)) if scores[index][0] == best_score]
                chosen_idx = random.choice(best_indices) # pick randomly among the best
                return best_score,legal_moves[chosen_idx]
            
            else:
                '''
                those 0 < index_agent < num_agent-1 (no matter the depth) would be execute here
                this is a min_player, so update beta and prune if best_score(v) is less than alpha
                the updated alpha_beta list will be changed in the function that call this function,
                because list is mutable
                '''
                scores = []
                best_score = float("inf")
                for action in legal_moves:
                    ab = [alpha_beta[0], alpha_beta[1]]
                    GameState = gameState.getNextState(index_agent, action)
                    thisScore = countmax(depth, GameState, index_agent+1, ab)
                    scores.append(thisScore)
                    best_score = min(best_score, thisScore[0])
                    if best_score < alpha_beta[0]:
                        return best_score, action
                    ab[1] = min(ab[1], best_score)
                    alpha_beta[1] = ab[1]
                best_indices = [index for index in range(len(scores)) if scores[index][0] == best_score]
                chosen_idx = random.choice(best_indices) # pick randomly among the best
                return best_score,legal_moves[chosen_idx]
        #alpha_beta is sent as a parameter, which is new from minimax
        best_score, bestmove = countmax(self.depth, gameState, 0, [-float("inf"), float("inf")])
        return bestmove
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction
        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        
        def countmax(depth, gameState, index_agent):
            num_agents = gameState.getNumAgents()
            legal_moves = gameState.getLegalActions(index_agent)
            if not len(legal_moves): # no legal_moves = done with game at the state (win or lose)
                return self.evaluationFunction(gameState), "0" # return the points
            if depth == 1 and index_agent == num_agents-1:
                scores = []
                for action in legal_moves:
                    GameState = gameState.getNextState(index_agent,action)
                    scores.append(self.evaluationFunction(GameState))
                total = 0
                for value in scores: total += value
                best_score = total/len(scores)
                '''
                instead of finding the minimum of the scores,
                find the average score as the best score
                bestmove is not importent here, 
                so just return legal_moves[0] is okay
                '''
                return best_score, legal_moves[0]
            
            elif index_agent == 0:
                scores = []
                for action in legal_moves:
                    GameState = gameState.getNextState(0, action)
                    scores.append(countmax(depth, GameState, 1))
                best_score = max(scores)[0]
                best_indices = [index for index in range(len(scores)) if scores[index][0] == best_score]
                chosen_idx = random.choice(best_indices) # pick randomly among the best
                '''
                the max_player, which is the pacman, remains the same as minimaxAgent
                '''
                return best_score, legal_moves[chosen_idx]
            
            elif index_agent == num_agents-1:
                scores = []
                for action in legal_moves:
                    GameState = gameState.getNextState(index_agent, action)
                    scores.append(countmax(depth-1, GameState, 0))
                total = 0
                for value in scores:
                    total += value[0]
                best_score = total/len(scores)
                '''
                instead of finding the minimum of the scores,
                find the average score as the best score
                bestmove is not importent here, so just return legal_moves[0] is okay
                '''
                return best_score, legal_moves[0]
            
            else:
                '''
                those 0 < index_agent < num_agent-1 (no matter the depth) would be execute here
                '''
                scores = []
                for action in legal_moves:
                    GameState = gameState.getNextState(index_agent, action)
                    scores.append(countmax(depth, GameState, index_agent+1))
                total = 0
                for value in scores:
                    total += value[0]
                best_score = total/len(scores)
                '''
                instead of finding the minimum of the scores,
                find the average score as the best score
                bestmove is not importent here, so just return legal_moves[0] is okay
                '''
                return best_score,legal_moves[0]
        
        best_score, bestmove = countmax(self.depth, gameState, 0)
        return bestmove
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)
    '''
    take the score, position, food, Ghoststates, from currentGameState
    using the function used in the reflexagent
    '''
    score = currentGameState.getScore()
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scared = [ghostState.scaredTimer for ghostState in ghostStates]

    '''
    count the minGhostDistance using manhattanDistance 
    manhattanDistance is useful since pacman only go top, left, right, or down
    '''
    min_ghost_dist = min([manhattanDistance(pos, state.getPosition()) for state in ghostStates])
    food_dist = [manhattanDistance(pos, food) for food in food.asList()] # count nearest food distances
    nearest_food = 0 if not food_dist else min(food_dist) # nearest food distance
    '''
    algorithm idea:
    1) there is a ghost that is scared and near pacman is 400 points 
       *pacman will chase it because this situation is highly rewarded*
    2) there is a ghost near pacman that is not sacred is 0 points.
    3) no ghost is near pacman and nearestFoodDistance < 1 is 10 points
    4) others are all 5 points
    '''
    for i in range(len(ghostStates)):
        ghost_dist = manhattanDistance(pos, ghostStates[i].getPosition())
        if scared[i] > 0 and ghost_dist < scared[i]:
            return 400 + score
        elif scared[i] <= 0 and ghost_dist < 2:
            return score
    if min_ghost_dist < 2:
        return score
    elif nearest_food < 1:
        return 10 + score
    else:
        return 5 + score

    # End your code (Part 4)

# Abbreviation
better = betterEvaluationFunction