from Reversi.reversi_model import ReversiGameRule
from template import Agent
import random
import time
from collections import deque

class myAgent(Agent):
    def __init__(self,_id):
        super().__init__(_id)
        self.game_rule = ReversiGameRule(2)
        self.time_limit = 0.95
        self.select_time = 0

    def GetActionList(self, state, agent_id):
        return list(set(self.game_rule.getLegalActions(state, agent_id)))

    def ExecuteAction(self, state, action, agent_id):
        next_state = self.game_rule.generateSuccessor(state, action, agent_id)
        next_score = self.game_rule.calScore(next_state, self.id)
        return next_state, next_score

    def GameEnd(self, state):
        return self.GetActionList(state, self.id) == ["Pass"] and self.GetActionList(state, 1 - self.id) == ["Pass"]

    def FilterAction(self, actions):
        outer_corner = {(0, 0), (0, 7), (7, 0), (7, 7)}
        inner_corner = {(1, 1), (1, 6), (6, 1), (6, 6)}

        # Find whether the candidate actions contains the outer corner
        sub_actions = list(set(actions).intersection(outer_corner))
        if len(sub_actions) > 0:
            actions = sub_actions

        # Filter out the inner corner from the candidate actions list
        sub_actions = list(set(actions).difference(inner_corner))
        if len(sub_actions) > 0:
            actions = sub_actions
        return actions

    def check_stability(self, game_state, action, start, end):
        sub_optimal = 0
        solution = None
        next_state, next_score = self.ExecuteAction(game_state, action, self.id)
        for i in range(start, end):
            if next_state.board[action[0]][i] != game_state.agent_colors[self.id]:
                return False
        if next_score > sub_optimal:
            sub_optimal = next_score
            solution = action
        return sub_optimal, solution

    def select_stable_action(self, stable_ans, best_optimal):
        best_solution = None
        if stable_ans is not False:
            sub_optimal, sub_solution = stable_ans
            if sub_optimal > best_optimal:
                best_solution = sub_solution
                best_optimal = sub_optimal
        return best_solution, best_optimal

    def find_stable_action(self, game_state, actions):
        best_optimal = float("-inf")
        best_solution = None
        for action in set(actions):
            if action[0] == 0 or action[0] == 7:
                stable_ans = self.check_stability(game_state, action, 0, action[1])
                best_solution, best_optimal = self.select_stable_action(stable_ans, best_optimal)

                stable_ans = self.check_stability(game_state, action, action[1], 8)
                best_solution, best_optimal = self.select_stable_action(stable_ans, best_optimal)

            if action[1] == 0 or action[1] == 7:
                stable_ans = self.check_stability(game_state, action, 0, action[0])
                best_solution, best_optimal = self.select_stable_action(stable_ans, best_optimal)

                stable_ans = self.check_stability(game_state, action, action[0], 8)
                best_solution, best_optimal = self.select_stable_action(stable_ans, best_optimal)

        return best_solution

    def SelectAction(self, actions, game_state):
        self.select_time += 1
        # Init
        start_time = time.time()
        self.game_rule.agent_colors = game_state.agent_colors
        queue = deque([(game_state, [])])
        max_score = 0
        count = 0

        # Random choose
        random_actions = self.FilterAction(actions)
        if len(random_actions) == 1:
            return random_actions[0]
        solution = random.choice(random_actions)

        stable_action = self.find_stable_action(game_state, actions)
        if stable_action is not None:
            return stable_action

        while len(queue) and (time.time() - start_time < self.time_limit):
            state, path = queue.popleft()
            new_actions = self.FilterAction(self.GetActionList(state,self.id))

            for action in new_actions:
                if time.time() - start_time >= self.time_limit:
                    break
                next_path = path + [action]
                next_state, next_score = self.ExecuteAction(state, action, self.id)

                if self.game_rule.gameEnds:
                    count += 1
                if self.game_rule.gameEnds and next_score > max_score:
                    max_score = next_score
                    solution = next_path[0]
                    continue

                opp_action = random.choice(self.GetActionList(next_state, 1- self.id))
                opp_state, opp_score = self.ExecuteAction(next_state, opp_action, 1-self.id)
                queue.append((opp_state, next_path))
        print(self.select_time)
        print(count)
        return solution

