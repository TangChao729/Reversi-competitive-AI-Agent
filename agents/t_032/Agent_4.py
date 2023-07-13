import math
from template import Agent
import random
import time
from Reversi.reversi_model import ReversiGameRule
from copy import deepcopy

#  python general_game_runner.py -a agents.t_032.new_MCTS,agents.t_032.ziyuan -m 10 -q
# python general_game_runner.py -a agents.t_032.new_MCTS,agents.t_032.myTeam -t -p


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

        self.position_weight = [
            [80, -25, 10, 5, 5, 10, -25, 80],
            [-25, -45, 1, 1, 1, 1, -45, -25],
            [10, 1, 3, 2, 2, 3, 1, 10],
            [5, 1, 2, 1, 1, 2, 1, 5],
            [5, 1, 2, 1, 1, 2, 1, 5],
            [10, 1, 3, 2, 2, 3, 1, 10],
            [-25, -45, 1, 1, 1, 1, -45, -25],
            [80, -25, 10, 5, 5, 10, -25, 80]
        ]

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
        root = TreeNode(None, None, self.id)
        while time.time() - self.start_time < self.time_limit:
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

    def MiniMax(self, state, agent_id, alpha, beta, depth):

        if depth == 3 or self.GameEnd(state) or time.time() - self.start_time >= self.time_limit:
            return None, - self.CalculateWeight(state, agent_id)

        action_list = self.GetActionList(state, agent_id)
        best_action = None

        # If the self.id equal to the current agent id - max
        if agent_id == self.id:
            max_value = float('-inf')
            for action in action_list:

                new_state = self.ExecuteAction(state, action, agent_id)
                _act, value = self.MiniMax(new_state, 1 - agent_id, alpha, beta, depth + 1)

                if value > max_value:
                    max_value = value
                    best_action = action

                alpha = max(alpha, value)

                if beta <= alpha:
                    return best_action, max_value

            return best_action, max_value

        # If self.id not equal to the current agent id - min
        elif agent_id != self.id:
            min_value = float('inf')
            for action in action_list:
                new_state = self.ExecuteAction(state, action, agent_id)
                _act, value = self.MiniMax(new_state, 1 - agent_id, alpha, beta, depth + 1)

                if value < min_value:
                    min_value = value
                    best_action = action

                beta = min(beta, value)

                if beta <= alpha:
                    return best_action, min_value

            return best_action, min_value

    def CalculateWeight(self, game_state, agent_id):
        score = 0
        for i in range(len(self.position_weight)):
            for j in range(len(self.position_weight)):
                if game_state.board[i][j] == self.color[agent_id]:
                    score = score + self.position_weight[i][j]
                elif game_state.board[i][j] == self.color[1 - agent_id]:
                    score = score - self.position_weight[i][j]
        return score

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

        # Find whether the current action option contain the corner
        corner_location = {(0, 0), (0, 7), (7, 0), (7, 7)}
        corner_actions = list(set(actions).intersection(corner_location))

        # If there is corner action and move <= 20, directly return the corner action
        if self.selection_times <= 20 and len(corner_actions) > 0:
            return random.choice(corner_actions)

        # If number of move <= 10, using minimax
        elif self.selection_times <= 10:
            action, value = self.MiniMax(game_state_copy, self.id, float('-inf'), float('inf'), 0)
            return action

        # If number of move > 10 and there is no the corner options, using MCTS
        else:
            return self.MCTS(game_state_copy)

