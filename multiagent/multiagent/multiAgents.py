# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #Nếu gặp ma trong khoảng cách 2 ô, giảm điểm xuống rất thấp để tránh va phải ma
        for ghostState in newGhostStates:
            if manhattanDistance(newPos, ghostState.getPosition()) < 2:
                return -999999
        
        #Ưu tiên hướng đến viên đậu ở gần nhất
        foodList = newFood.asList()
        foodCount = len(foodList)
        if foodCount == 0:
            return 1000000     #Nếu bước đi tiếp theo làm cho foodList rỗng(ăn hết đậu) thì ưu tiên thật cao để ăn nốt
        minFoodDist = min([manhattanDistance(newPos, food) for food in foodList])   #Khoảng cách đến viên đậu gần nhất
        
        #Hạn chế đứng yên
        if action == Directions.STOP:
            return -100000

        #Kết hợp với điểm số mặc định của game
        return successorGameState.getScore() + (1.0 / minFoodDist)

def scoreEvaluationFunction(currentGameState: GameState):
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
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #agentIndex - "định danh" của agent trong game, depth - độ sâu(mỗi lần giả định tất cả các agent đi được 1 lượt = 1 tầng độ sâu)
        def value(state, agentIndex, depth):
            #Dừng
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            #Nếu lượt tiếp theo là Pacman(agentIndex = 0)
            if agentIndex == 0:
                return maxValue(state, agentIndex, depth)
            #Nếu lượt tiếp theo là ma(agentIndex > 0)
            else:
                return minValue(state, agentIndex, depth)

        def maxValue(state, agentIndex, depth):
            v = -float('inf')
            #Giả định bước đi
            legalActions = state.getLegalActions(agentIndex)

            #Tại mỗi node của Pacman, lấy max
            for action in legalActions:
                successor = state.generateSuccessor(agentIndex, action)
                v = max(v, value(successor, 1, depth))

            return v

        def minValue(state, agentIndex, depth):
            v = float('inf')
            legalActions = state.getLegalActions(agentIndex)
            numAgents = state.getNumAgents()    #Tổng số agent, nhằm kiểm tra khi nào hết một tầng độ sâu

            #Tại mỗi node của ma, lấy min
            for action in legalActions:
                successor = state.generateSuccessor(agentIndex, action)
                #Nếu là lượt của con ma cuối cùng
                if agentIndex == numAgents - 1:
                    v = min(v, value(successor, 0, depth - 1))  #Chuyển sang tầng độ sâu tiếp theo, lượt tiếp theo là của Pacman
                else:
                    v = min(v, value(successor, agentIndex + 1, depth)) #Chưa chuyển sang tầng độ sâu dưới, lượt tiêp theo là của ma

            return v
        
        bestAction = None           #Nước đi tốt nhất đối với Pacman
        maxScore = -float('inf')    #Trạng thái tốt nhất đối với Pacman

        for action in gameState.getLegalActions(0):
            #Đánh giá trạng thái(dựa trên mức độ có lợi cho Pacman)
            score = value(gameState.generateSuccessor(0, action), 1, self.depth)
            #Nếu có một trạng thái tốt hơn cho pacman
            if score > maxScore:
                maxScore = score
                bestAction = action
        
        return bestAction

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #Alpha and Beta for prunning algorithm
        alpha = -float('inf')
        beta = float('inf')

        def value(state, agentIndex, depth, alpha, beta):
            #Dừng
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            #Nếu lượt tiếp theo là Pacman(agentIndex = 0)
            if agentIndex == 0:
                return maxValue(state, agentIndex, depth, alpha, beta)
            #Nếu lượt tiếp theo là ma(agentIndex > 0)
            else:
                return minValue(state, agentIndex, depth, alpha, beta)
            
        def maxValue(state, agentIndex, depth, alpha, beta):
            v = -float('inf')
            legalActions = state.getLegalActions(agentIndex)

            #Tại mỗi node của Pacman, lấy max
            for action in legalActions:
                successor = state.generateSuccessor(agentIndex, action)
                v = max(v, value(successor, 1, depth, alpha, beta))

                #Thuật toán cắt tỉa
                if v > beta:
                    return v            #Nhánh có alpha > beta sẽ bị cắt, trả về giá trị cuối không bị cắt tỉa
                alpha = max(alpha, v)   #Lấy giá trị alpha là lớn nhất cho tầng Max

            return v
        
        def minValue(state, agentIndex, depth, alpha, beta):
            v = float('inf')
            legalActions = state.getLegalActions(agentIndex)
            numAgents = state.getNumAgents()

            #Tại mỗi node của ma, lấy min
            for action in legalActions:
                successor = state.generateSuccessor(agentIndex, action)
                #Nếu là lượt của con ma cuối cùng
                if agentIndex == numAgents - 1:
                    v = min(v, value(successor, 0, depth - 1, alpha, beta))             #Chuyển sang tầng độ sâu tiếp theo, lượt tiếp theo là của Pacman
                else:
                    v = min(v, value(successor, agentIndex + 1, depth, alpha, beta))    #Chưa chuyển sang tầng độ sâu dưới, lượt tiêp theo là của ma

                #Thuật toán cắt tỉa
                if v < alpha:
                    return v            #Nhánh có alpha > beta sẽ bị cắt, trả về giá trị cuối không bị cắt tỉa
                beta = min(beta, v)

            return v
        
        bestAction = None
        v = -float('inf')

        for action in gameState.getLegalActions(0):
            #Đánh giá trạng thái(dựa trên mức độ có lợi cho Pacman)
            score = value(gameState.generateSuccessor(0, action), 1, self.depth, alpha, beta)
            #Nếu có một trạng thái tốt hơn cho pacman
            if score > v:
                v = score

                bestAction = action
            #Cập nhật alpha:
            if v > beta:
                return bestAction
            alpha = max(alpha, v)
        
        return bestAction

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def value(state, agentIndex, depth):
            #Dừng
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            #Nếu lượt tiếp theo là Pacman(agentIndex = 0)
            if agentIndex == 0:
                return maxValue(state, agentIndex, depth)
            #Nếu lượt tiếp theo là ma(agentIndex > 0)
            else:
                return expectValue(state, agentIndex, depth)
        
        def maxValue(state, agentIndex, depth):
            v = -float('inf')
            #Giả định bước đi
            legalActions = state.getLegalActions(agentIndex)

            #Tại mỗi node của Pacman, lấy max
            for action in legalActions:
                successor = state.generateSuccessor(agentIndex, action)
                v = max(v, value(successor, 1, depth))

            return v
        
        def expectValue(state, agentIndex, depth):
            v = 0
            legalActions = state.getLegalActions(agentIndex)
            numAgents = state.getNumAgents()    #Tổng số agent, nhằm kiểm tra khi nào hết một tầng độ sâu

            #Tại mỗi node của ma, lấy tổng
            for action in legalActions:
                successor = state.generateSuccessor(agentIndex, action)
                #Nếu là lượt của con ma cuối cùng
                if agentIndex == numAgents - 1:
                    v += value(successor, 0, depth - 1)                 #Chuyển sang tầng độ sâu tiếp theo, lượt tiếp theo là của Pacman
                else:
                    v += value(successor, agentIndex + 1, depth)        #Chưa chuyển sang tầng độ sâu dưới, lượt tiêp theo là của ma

            return v / len(legalActions)        #Trả về trung bình
        
        bestAction = None           #Nước đi tốt nhất đối với Pacman
        maxScore = -float('inf')    #Trạng thái tốt nhất đối với Pacman

        for action in gameState.getLegalActions(0):
            #Đánh giá trạng thái(dựa trên mức độ có lợi cho Pacman)
            score = value(gameState.generateSuccessor(0, action), 1, self.depth)
            #Nếu có một trạng thái tốt hơn cho pacman
            if score > maxScore:
                maxScore = score
                bestAction = action
        
        return bestAction

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    newCapsules = currentGameState.getCapsules()    #Xác định vị trí capsule

    #Đánh giá nước đi giả định của Pacman
    score = currentGameState.getScore()

    #Trạng thái về thức ăn trên sân
    foodList = newFood.asList()
    numFoodLeft = len(foodList)

    #1. Ưu tiên ăn hết đậu
    score -= 4 * numFoodLeft        #Nếu nước đi làm giảm lượng đậu, hình phạt sẽ nhẹ hơn

    if numFoodLeft > 0:
        minFoodDist = min([manhattanDistance(newPos, food) for food in foodList])
        # Thưởng nếu tiến lại gần viên đậu gần nhất
        score += 2.0 / minFoodDist

    #2. Xử lý khi gặp ma
    for i in range(len(newGhostStates)):
        ghost = newGhostStates[i]
        scaredTime = newScaredTimes[i]
        dist = manhattanDistance(newPos, ghost.getPosition())

        #Nếu ma đang sợ: Càng gần càng tốt
        if scaredTime > 0:    
            if dist > 0:
                score += 100.0 / dist
            else:
                score += 500.0 # Ăn được ma
        
        #Nếu ma bình thường: Không lại gần trong khoảng cách 2 ô
        else:
            if dist < 2:
                score -= 1000.0
        
    #3. Ưu tiên ăn capsule để bắt ma
    score -= 20 * len(newCapsules)          #Nếu nước đi tiến lại gần capsule, hình phạt sẽ nhẹ hơn

    return score
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
