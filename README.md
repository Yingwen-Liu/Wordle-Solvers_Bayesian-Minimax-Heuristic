# Wordle_Solvers

Apply auto solvers to solve the Wordle game

## Solvers
| Solver | Average Attempts | Time Consumption | Description |
| ------ | ---------------- | ---------------- | ----------- |
| `GreedySolver` | 3.6548 | 3 | A letter-frequency heuristic solver. Very fast |
| `GreedierSolver` | 3.6262 | 4 (least) | A better letter-frequency heuristic solver. Faster |
| `BayesianSolver` | 3.6050 | 2 | Apply Bayesian search to find the word with highest entropy. Very slow |
| `BayesianEnhanceSolver` | 3.5998 | 1 (most) | Similar to `BayesianSolver` but with heauristic to handle the green positions. Slower |
| `RandomSolver` | ~4 | | Randomly select a word from the word list |
| `FixedSolver` | 3.9835 | | Select the word that in the middle of the word list. A better standard of evaluation than `RandomSolver` |

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


