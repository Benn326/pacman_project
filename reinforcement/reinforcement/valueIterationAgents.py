# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"

        #Lan truyền thuận
        for i in range(self.iterations):
            # Tạo một bản sao để lưu trữ giá trị mới
            newValues = self.values.copy()
            states = self.mdp.getStates()
            
            for state in states:
                #Không cần tính toán giá trị hay tìm hành động tối ưu ở vị trí kết thúc
                if self.mdp.isTerminal(state):
                    continue
                
                #Tìm giá trị Q-value lớn nhất trong các hành động có thể
                Actions = self.mdp.getPossibleActions(state)
                if Actions:
                    #V(k+1)(s) = max_qValue
                    newValues[state] = max([self.computeQValueFromValues(state, action) for action in Actions])
                    
            #Cập nhật lại bảng giá trị chính sau khi đã tính xong toàn bộ state cho vị trí vừa rồi
            self.values = newValues        


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"

        qValue = 0      
        transitions = self.mdp.getTransitionStatesAndProbs(state, action)
        
        for nextState, prob in transitions:
            reward = self.mdp.getReward(state, action, nextState)
            #qValue = xác suất thực hiện action * (phần thưởng + chiết khấu * Vk(s'))
            qValue += prob * (reward + (self.discount * self.values[nextState]))
            
        return qValue
    
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        #Ở ô kết thúc
        if self.mdp.isTerminal(state):
            return None
        
        actions = self.mdp.getPossibleActions(state)
        bestAction = None
        maxQValue = float('-inf')
        
        #Chọn nước đi có qValue cao nhất để thực hiện
        for action in actions:
            qValue = self.computeQValueFromValues(state, action)
            if qValue > maxQValue:
                maxQValue = qValue
                bestAction = action
                
        return bestAction
    
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


class PrioritizedSweepingValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

        states = self.mdp.getStates()

        #Tìm tiền nhiệm của tất cả các trạng thái
        predecessors = {s: set() for s in states}
        for s in states:
            if not self.mdp.isTerminal(s):
                for action in self.mdp.getPossibleActions(s):
                    for nextState, prob in self.mdp.getTransitionStatesAndProbs(s, action):
                        if prob > 0:
                            predecessors[nextState].add(s)

        #Khởi tạo Priority Queue (state, -diff) (ưu tiên hơn cho state có diff lớn)
        PQ = util.PriorityQueue()
        for s in states:
            if not self.mdp.isTerminal(s):
                #diff = |V(s) - max Q(s, a)|
                maxQ = max([self.getQValue(s, action) for action in self.mdp.getPossibleActions(s)])
                diff = abs(self.values[s] - maxQ)
                PQ.push(s, -diff)

        #Lan truyền ngược
        for i in range(self.iterations):
            if PQ.isEmpty():
                break
            
            s = PQ.pop()

            #Cập nhật giá trị cho s
            if not self.mdp.isTerminal(s):
                self.values[s] = max([self.computeQValueFromValues(s, a) for a in self.mdp.getPossibleActions(s)])

            #Kiểm tra các tiền nhiệm của s
            for p in predecessors[s]:
                maxQ_p = max([self.computeQValueFromValues(p, a) for a in self.mdp.getPossibleActions(p)])
                diff = abs(self.values[p] - maxQ_p)

                #Cập nhật nếu ưu tiên mới cao hơn
                if diff > self.theta:
                    PQ.update(p, -diff)
