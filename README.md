# Wordle_Solvers

Apply auto solvers to solve the Wordle game

## Solvers
| Solver | Average Attempts | Time Consumption | Description |
| ------ | ---------------- | ---------------- | ----------- |
| `GreedySolver` | 3.6548 | 3 | a letter-frequency heuristic solver, very fast |
| `GreedierSolver` | 3.6262 | 4 | a better letter-frequency heuristic solver, faster |
| `BayesianSolver` | 3.6050 | 2 | bayesian search to find the word with highest entropy |
| `BayesianEnhanceSolver` | 3.5998 | 1 | similar to `BayesianSolver` but with heauristic to handle the green positions |
| `RandomSolver` | ~4 | | randomly select a word from the word list |
| `FixedSolver` | 3.9835 | | select the word that in the middle of the word list. May be better to used as a standard of evaluation than `RandomSolver` |

![Figure_1](https://github.com/user-attachments/assets/589d46bc-2587-4bfc-9a6e-78569014b96e)

### GreedySolver vs GreedierSolver
![GreedyVSGreedier](https://github.com/user-attachments/assets/cd513b02-cefe-4b41-ada6-4beeeb4d8f93)

### BayesianSolver vs BayesianEnhanceSolver
![BayesianVSEnhance](https://github.com/user-attachments/assets/e0f6c9b3-4ee9-46cd-8eb5-1d4c967b2a81)

## Prerequisites (for visualization)
- tqdm 
- matplotlib

## To-Do
- [ ] Apply MCTS


