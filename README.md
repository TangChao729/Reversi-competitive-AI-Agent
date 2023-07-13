# Competitive AI - A reversi AI agent

## Table of content
1. [Home and Introduction]()
2. [Problem Analysis](https://github.com/TangChao729/Reversi_AI/blob/main/Wiki/Problem-Analysis.md)

    2.1 [Method 1 - Breadth First Search](https://github.com/TangChao729/Reversi_AI/blob/main/Wiki/2.1-Method-1---Breadth-First-Search.md)

    2.2 [Method 2 - Minimax](https://github.com/TangChao729/Reversi_AI/blob/main/Wiki/2.2-AI-Method-2---Minimax.md)

    2.3 [Method 3 - Monte Carlo Tree Search](https://github.com/TangChao729/Reversi_AI/blob/main/Wiki/2.3-Method-3---Monte-Carlo-Tree-Search.md)

    2.4 [Method 4 - Monte Carlo Tree Search Plus Minimax](https://github.com/TangChao729/Reversi_AI/blob/main/Wiki/2.4-Method-4---Monte-Carlo-Tree-Search-Plus-Minimax.md)
3. [Evolution and Experiments](https://github.com/TangChao729/Reversi_AI/blob/main/Wiki/4.-Conclusions-and-Reflections.md)
4. [Conclusions and Reflections]()

## Introduction
The purpose of this project is to implement the AI agent for reversi game by using the AI-Technical learned from the COMP90054. After analysing the challenges of the reversi game and comparing the different AI-Technical, the team determined to implement the AI agent for reversi game by using the BFS, MCTS and Minimax. Our final approach is to combine the MCTS and the Minimax to further improve the performance in the Tournament.

In this Wiki, the detailed implementation process and the following aspects will be discussed:
- The challenges that may encountered during the implementation and the reason of decision made about the AI-Technical.
- The detailed information about the agent, including the motivation, implement detail, problem solving, evaluation, advantage, disadvantage, and future improvement.
- Compare the performance of different implemented agents.
- Conclusion and reflection about this project.

## Youtube presentation


[![](https://github.com/COMP90054-2022S2/comp90054-a3-reversi-ai/blob/Wiki/wiki-template/images/video_cover_page.png)](https://youtu.be/4B0l5Tt9rnE)

## Team Members

Our team member:

* Student 1's Taylor Tang - taylor.tang@student.unimelb.edu.au - 1323782
* Student 2's Siqi Zhong - siqzhong@student.unimelb.edu.au - 1306166
* Student 3's Ziyuan Chen - ziyuanc2@student.unimelb.edu.au - 1262190
