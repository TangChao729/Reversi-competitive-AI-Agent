import time
from copy import deepcopy

from Reversi.reversi_model import ReversiGameRule
from template import Agent

class myAgent(Agent):
    def __init__(self, _id):
        super().__init__(_id)
        self.color = None
        self.start_time = None
        self.game_rule = ReversiGameRule(2)
        self.depth = 4
        self.time_limit = 0.9
        self.BOARD_SIZE = 8

    def SelectAction(self, actions, game_state):
        # init
        self.game_rule.agent_colors = game_state.agent_colors
        self.start_time = time.time()
        self.color = game_state.agent_colors
        game_state_copy = deepcopy(game_state)

        if len(actions) == 1:
            return actions[0]

        action, value = self.minimax(game_state_copy, self.id, float('-inf'), float('inf'), 0)
        return action

    def minimax(self, state, agent_id, alpha, beta, depth):

        if depth == self.depth or self.is_game_end(state) or time.time() - self.start_time >= self.time_limit:
            return None, - self.evaluation(state, agent_id)

        action_list = self.get_action_list(state, agent_id)
        best_action = None

        # If the self.id equal to the current agent id - max
        if agent_id == self.id:
            max_value = float('-inf')
            for action in action_list:

                new_state = self.execute_action(state, action, agent_id)
                _act, value = self.minimax(new_state, 1 - agent_id, alpha, beta, depth + 1)

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
                new_state = self.execute_action(state, action, agent_id)
                _act, value = self.minimax(new_state, 1 - agent_id, alpha, beta, depth + 1)

                if value < min_value:
                    min_value = value
                    best_action = action

                beta = min(beta, value)

                if beta <= alpha:
                    return best_action, min_value

            return best_action, min_value

    def evaluation(self, game_state, agent_id):
        score = 0
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if game_state.board[i][j] == self.color[agent_id]:
                    score += 1
                elif game_state.board[i][j] == self.color[1 - agent_id]:
                    score -= 1
        return score

    def is_game_end(self, state):
        return self.get_action_list(state, self.id) == ["Pass"] and self.get_action_list(state, 1 - self.id) == ["Pass"]

    def get_action_list(self, state, agent_id):
        return list(set(self.game_rule.getLegalActions(state, agent_id)))

    def execute_action(self, state, action, agent_id):
        next_state = self.game_rule.generateSuccessor(state, action, agent_id)
        return next_state
