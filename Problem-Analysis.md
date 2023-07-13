# Analysis of the problem

The aim of this project is to create a AI agent for the reversi game. Before choosing the AI technical and designing an AI agent for reversi, we need to know the challenges and the problem we would face in the development process to help us make the decision on the AI-technical.

## 1. Challenge
- ###  Hard to identify evaluation function

The first challenge is hard to design a good evaluation function(heuristic function) to correctly evaluate the board situation in terms of which side (either black or white) has more advantage over the other. A traditional and naive evaluation is to count and compare the black and white pieces amount.However, as per the game rule, during the game process, one player could turn his opponent's pieces into hims. Therefore, with the naive evaluation method, it cannot truly reflect the board situation when there are move available.

A demo goes here

![](https://github.com/COMP90054-2022S2/comp90054-a3-reversi-ai/blob/Wiki/wiki-template/images/turnover.gif)

More aspects need to be considered in the evaluation function, such as stability and mobility. Stability refers to pieces that cannot be over turned by the other player. For example, a piece at the corner position (0, 0), (0, 7), (7, 0), (7, 7). Other stabilized pieces could be pieces on the edge of the board when the edge is full. These pieces can act like an anchor piece and become game winning situation if managed properly. Mobility refers to a player's number of available moves in his round. If a player has no move to make, the game rule forcefully let this player's opponent to keep playing. This makes the first player in a bad position. Intuitively, more mobility is not always good to one player. During the starting stage (total moves less than 20), a player with low mobility often means it takes more advantage as he can overturn more opponent's pieces in one round.

Therefore, evaluation function in this AI agent implementation is complex and crucial. How to properly manage the evaluation is the key component to make our next move.

- ### Hard to predict the opponent's action

Another major challenge when design our AI agent is to predict opponent's move. This involves game theory in a way that if we could correctly predict my opponent's move, we can then act accordingly to choose our next best-move. By doing so, we could also disregard the moves that the opponent will not make, to decrease the computational power needed.

However, during the game process it is extremely difficult and even unrealistic to predict opponent's move. Hence, we need to choose a balance point in between exploitation (thinking further) and exploration (thinking wider) in order to be prepared for opponent's move.

- ### The limitation of the act time

[Analysts](http://fragrieu.free.fr/SearchingForSolutions.pdf) have estimated the number of legal positions in Reversi is at most 10^28, and it has a game-tree complexity of approximately 10^58. 

It is NP-complete to exhaustively compute all possible solutions and act accordingly. In this given game rule, the initial set-up time limit is 15s and the remaining acting time is limited to 1 second. How to find a proper move within only 1 second the other main problems need to be solved in the implementation.

- ### Implementation time is limited
There are only about one month to implement our agent. Therefore, the implementation difficulty is also a important criteria to be considered.

## 2. Criteria for technical choosing
1. The technical should not be a time-consuming to find the next action.
2. The technical should be achievable and can be implemented within the one month.
3. Since there are about 10^28 legal game state of the reversi game, the technical should have the generalizable to perform well over the different game state.
4. The technical should require the less domain knowledge of the reversi game since we are not reversi expert.

## 3. Offense & Defense

During the game process of a reversi game, the definitions of defense and offense are not quite clear when compared to other games such as chess. Each move a player made has to over turn at least one opponent's piece (unless there is no move to make), and each move a player made could expose his own pieces in danger. 

As mentioned in the above section, mobility (both maximize-mobility and minimize-mobility) can be used as a valid game strategy as defense or offense action depends on the stage of a game. Similarly, max-stability can act as both a defense and a offense strategy. Therefore, when designing the AI agent, both defense (in terms of minimize the risks to us) and offence (in terms of maximize the opportunity for us) should be considered simultaneously. There is no clear separation to distinguish the next move to be offensive of defensive.

## 4. Comparison of Different Technical

| Name                          | Computation Time | Performance                                     | Implementation Difficulty                                                     | Generalizability               | Domain Knowledge Requirement |
|-------------------------------|------------------|-------------------------------------------------|-------------------------------------------------------------------------------|--------------------------------|------------------------------|
| Blind Search(BFS)             | High             | Good if it can search to the end state          | Easy to implement                                                             | High                           | Low                          |
| Heuristic Search(AStar)       | Medium           | Good if the heuristic function is good          | Hard due to hard to identified a excellent heuristic function                 | High                           | High                         |
| Monte Carlo Tree Search (UCT) | High             | Good if computational power is strong           | Medium to implement                                                           | High                           | Low - Medium                 | 
| Goal Recognition techniques   | Short            | Good if opponent player move as expected        | Hard due to high requirement of the domain knowledge                          | Low                            | High                         |
| Minimax                       | Short            | Good if the opponent player also play optimally | Medium to implement                                                           | High                           | High                         |
 | Neunal Network                | Short            | Depending on the parameters and input dataset   | Hard due to the pre-training time is too long and lack of relevant databases. | Depend on the training process | Low                          |      

## 5. Final decision on technical

According to the above analysis, we decided to implement the agent by using the BFS first since the BFS is easy to be implemented and doesn't require any domain knowledge of the reversi, which is a good start. In addition, MCTS with UCT and Minimax are also be implemented since they can provide the good performance within the time limit, require less domain knowledge and not hard to implement. The detailed information of these three agents are shown in the next section.