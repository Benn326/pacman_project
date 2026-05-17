# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    from util import Stack
    stack = Stack() #Stack chứa các đỉnh
    visited = set() #Danh sách đỉnh mở rộng
    startState = problem.getStartState()
    stack.push((startState,[])) #Đưa ô đầu tiên vào stack

    while not stack.isEmpty():
        "Rút phần tử trong stack ra"
        currentState, actions = stack.pop()

        #Nếu ô vừa lấy ra khỏi stack là đích thì kết thúc trò chơi, trả về danh sách bước đi
        if problem.isGoalState(currentState):
            return actions
        
        if currentState not in visited:
            #Thêm ô đang xét vào danh sách
            visited.add(currentState)

            #Mở rộng bằng cách thêm đỉnh vào stack
            successors = problem.getSuccessors(currentState)
            for nextState, action, cost in successors:
                #Tránh quay lại một đỉnh(vị trí) đã được mở rộng từ trước
                if nextState not in visited:
                    newActions = actions + [action]         #Thêm action vào chuỗi các bước đi
                    stack.push((nextState, newActions))     #Thêm vị trí mới và bước đi tương ứng vào stack

    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue

    PQ = PriorityQueue()    #Priority Queue chứa các đỉnh
    visited = set()         #Danh sách đỉnh mở rộng
    startState = problem.getStartState()
    PQ.push((startState, [], 0), 0 + heuristic(startState, problem))    #Vẫn giữ lại 0 + heuristic(startState, problem) cho đúng bản chất A*

    while not PQ.isEmpty():
        #Rút phần tử ở đầu Priority Queue ra
        currentState, actions, currentCost = PQ.pop()

        #Nếu vị trí vừa lấy ra khỏi stack là đích thì kết thúc trò chơi, trả về danh sách bước đi
        if problem.isGoalState(currentState):
            return actions
        
        if currentState not in visited:
            #Thêm ô đang xét vào danh sách
            visited.add(currentState)

            for nextState, action, stepCost in problem.getSuccessors(currentState):
                #g(next) = g(n) + cost of step betwwen n and next
                newCost = currentCost + stepCost

                #f(next) = g(next) + h(next)
                f = newCost + heuristic(nextState, problem)

                newActions = actions + [action]                     #Thêm action vào chuỗi các bước đi
                PQ.push((nextState, newActions, newCost), f)        #Thêm vị trí mới và bước đi tương ứng vào Priority Queue

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
