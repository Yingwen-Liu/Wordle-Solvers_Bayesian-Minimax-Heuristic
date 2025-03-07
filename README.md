# Wordle_Solvers

Apply auto solvers to solve the Wordle game
- `game.py`: A rough version of Wordle. Able to play manually
- `test.py`: Test all the solvers and provide an overview
- `solvers.py`: Able to manually test the selected solver

## Solvers
| Solver | Average Attempts (with PositionHandler) | Time Consumption | Description |
| ------ | ---------------- | ---------------- | ----------- |
| `GreedySolver` | 3.6548 | Fast | A letter-frequency heuristic solver |
| `GreedierSolver` | 3.6262 | Fast | A better letter-frequency heuristic solver |
| `BayesianSolver` | 3.5998 | Very slow | Apply Bayesian search to find the word with highest entropy. May exceed 6 attempts |
| `RandomSolver` | ~4.1 | | Randomly select a word from the word list |
| `FixedSolver` | 3.9835 | | Select the word that in the middle of the word list. A better standard of evaluation than `RandomSolver` |

![Figure_1](https://github.com/user-attachments/assets/d2270ae9-5ec0-4930-8a4d-258972c6cb88)
### GreedySolver + PositionHandler vs GreedierSolver + PositionHandler
![GreedyVSGreedier](https://github.com/user-attachments/assets/cd513b02-cefe-4b41-ada6-4beeeb4d8f93)

### BayesianSolver + NormalHandler vs BayesianSolver + PositionHandler
![BayesianVSEnhance](https://github.com/user-attachments/assets/e0f6c9b3-4ee9-46cd-8eb5-1d4c967b2a81)

Considering that Wordle allows only 6 attempts, BayesianEnhanceSolver is likely better than BayesianSolver

## Prerequisites (for visualization)
- tqdm 
- matplotlib

## To-Do
- [ ] Apply MCTS


