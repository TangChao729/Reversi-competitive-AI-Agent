import math
from template import Agent
import random
import time
from Reversi.reversi_model import ReversiGameRule
from copy import deepcopy

#  python general_game_runner.py -a agents.t_032.new_MCTS,agents.t_032.ziyuan -m 10 -q
# python general_game_runner.py -a agents.t_032.git_new,agents.t_032.git_change -t -p


class TreeNode():
    """
    This class is used to store the node of MCTS
    """
    def __init__(self, parent, current, color):
        self.parent = parent
        self.reward = 0      # reward
        self.visit = 0      # visit
        self.color = color
        self.current = current
        self.child = dict()


class myAgent(Agent):
    def __init__(self, _id):
        super().__init__(_id)
        self.color = None
        self.selection_times = 0
        self.game_rule = ReversiGameRule(2)
        self.start_time = None
        self.time_limit = 0.9

        self.hard_code = [
            [(0, 0), (7, 0), (0, 7), (7, 7)],
            [(2, 2), (2, 3), (2, 4), (2, 5), (3, 2), (3, 5), (4, 2), (4, 5), (5, 2), (5, 3), (5, 4), (5, 5)],
            [(0, 2), (0, 3), (0, 4), (0, 5), (2, 0), (3, 0), (4, 0), (5, 0), (7, 2), (7, 3), (7, 4), (7, 5), (2, 7),
             (3, 7), (4, 7), (5, 7)],
            [(2, 1), (3, 1), (4, 1), (5, 1), (1, 2), (1, 3), (1, 4), (1, 5), (6, 2), (6, 3), (6, 4), (6, 5), (2, 6),
             (3, 6), (4, 6), (5, 6)],
            [(0, 1), (7, 1), (0, 6), (7, 6), (1, 0), (6, 0), (1, 7), (6, 7),(1, 1), (6, 1), (1, 6), (6, 6)]
        ]

    def GetActionList(self, state, agent_id):
        return list(set(self.game_rule.getLegalActions(state, agent_id)))

    def ExecuteAction(self, state, action, agent_id):
        next_state = self.game_rule.generateSuccessor(state, action, agent_id)
        return next_state

    def GameEnd(self, state):
        return self.GetActionList(state, self.id) == ["Pass"] and self.GetActionList(state, 1 - self.id) == ["Pass"]

    def CalculateReward(self, state):
        my_score = self.game_rule.calScore(state, self.id)
        opponent_score = self.game_rule.calScore(state, 1 - self.id)
        if my_score > opponent_score:
            return self.id, my_score - opponent_score
        elif opponent_score > my_score:
            return 1 - self.id, opponent_score - my_score
        else:
            return 2, 0

    def DetermineAction(self, action_list):
        if len(action_list) == 1:
            return action_list[0]

        for move_list in self.hard_code:
            random.shuffle(move_list)
            for move in move_list:
                if move in action_list:
                    return move

    def Select(self, node, state):
        # Handle timeout
        if time.time() - self.start_time >= self.time_limit:
            return False

        # If there is no child for the current node, choose this node
        if len(node.child) == 0:
            return node, state
        else:
            # Init
            best_score = float("-inf")
            best_move = None

            for k in node.child.keys():
                # If the current child is not visited, choose this child node
                if node.child[k].visit == 0:
                    best_move = k
                    break
                # If the current child is visited, choose a child node based on the UCT formula
                else:
                    child_visit = node.child[k].visit
                    score = (node.child[k].reward / child_visit) + 2 * math.sqrt(2 * math.log(node.visit) / child_visit)
                    if score > best_score:
                        best_score = score
                        best_move = k

            state = self.ExecuteAction(state, best_move, node.color)
            return self.Select(node.child[best_move], state)

    def Expand(self, node, state):
        # Expand the child node
        for move in self.GetActionList(state, node.color):
            node.child[move] = TreeNode(node, move, 1 - node.color)

    def Simulation(self, node, state):
        # Change the color first
        if node.color == self.id:
            current_color = 1 - self.id
        else:
            current_color = self.id

        # Simulate until the game end
        while not self.GameEnd(state):

            # Handle the timeout
            if time.time() - self.start_time >= self.time_limit:
                return False

            # Get the current color and choose an action
            current_color = 1 - current_color
            action_list = self.GetActionList(state, current_color)
            action = self.DetermineAction(action_list)

            # If chosen action is 'Pass', continue
            if action == 'Pass':
                continue
            # If chosen action is not 'Pass', execute the current action
            else:
                state = self.ExecuteAction(state, action, current_color)

        # Calculate the reward and record the winner
        winner, score = self.CalculateReward(state)

        return winner, score

    def BackPropagation(self, node, score):
        if time.time() - self.start_time >= self.time_limit:
            return False
        node.visit += 1
        if node.color == self.id:
            node.reward += score
        else:
            node.reward -= score
        if node.parent is not None:
            self.BackPropagation(node.parent, score)

    def FindSolution(self, root):
        best_n = float("-inf")
        best_move = None

        for k in root.child.keys():
            if root.child[k].visit > 0:
                if (root.child[k].reward / root.child[k].visit) > best_n:
                    best_n = root.child[k].reward / root.child[k].visit
                    best_move = k
        return best_move

    def MCTS(self, game_state):
        count = 0
        root = TreeNode(None, None, self.id)
        while time.time() - self.start_time < self.time_limit:
            count += 1
            deepcopy_board = deepcopy(game_state)

            # Select
            select_ans = self.Select(root, deepcopy_board)
            if select_ans is False:
                return self.FindSolution(root)
            else:
                choice, deepcopy_board = select_ans

            # Expand
            self.Expand(choice, deepcopy_board)

            # Simulation
            simulation_ans = self.Simulation(choice, deepcopy_board)
            if simulation_ans is False:
                return self.FindSolution(root)
            else:
                winner, different = simulation_ans

            # Calculate the reward
            if self.id == 1:
                propagation_score = [different, -different, 0][winner]
            else:
                propagation_score = [-different, different, 0][winner]

            # back propagation
            self.BackPropagation(choice, propagation_score)
        return self.FindSolution(root)

    def SelectAction(self, actions, game_state):
        # The move numbers of current agent on the current board
        self.selection_times += 1

        # init
        self.game_rule.agent_colors = game_state.agent_colors
        self.start_time = time.time()
        self.color = game_state.agent_colors
        game_state_copy = deepcopy(game_state)

        # If there is only 1 action or "pass", directly return this action
        if len(actions) == 1:
            return actions[0]

        return self.MCTS(game_state_copy)


