# Wordle_Solvers

Apply auto solvers to solve the Wordle game
- `game.py`: A rough version of Wordle. Able to play manually
- `test.py`: Test all the solvers and provide an overview
- `solvers.py`: Able to manually test the selected solver

## Solvers
| Solver | Average Attempts (PositionHandler) | (NormalHandler) | Time Consumption | Description |
| ------ | ---------------------------------- | --------------- | ---------------- | ----------- |
| `GreedySolver` | 3.6548 | 3.8281 | Low | A letter-frequency heuristic solver |
| `GreedierSolver` | 3.6262 | 3.7990 | Low | A better letter-frequency heuristic solver |
| `BayesianSolver` | 3.5998 | 3.6050 | Very high | Apply Bayesian search to find the word with highest entropy |
| `RandomSolver` | ~4.1 | - | | Randomly select a word from the word list |
| `FixedSolver` | 3.9835 | - | | Select the word that in the middle of the word list. A better standard of evaluation than `RandomSolver` |

![Figure_1](https://github.com/user-attachments/assets/d2270ae9-5ec0-4930-8a4d-258972c6cb88)
## Handlers
- `NormalHandler`: ability to remove words that not match the feedback from the word list.
- `PositionHandler`: additional ability to assign the most frequent letter to the green positions (where the letter is correct)

### GreedySolver + PositionHandler vs GreedierSolver + PositionHandler
![GreedyVSGreedier](https://github.com/user-attachments/assets/cd513b02-cefe-4b41-ada6-4beeeb4d8f93)

![Figure_1](https://github.com/user-attachments/assets/be05f61d-addd-41cc-a20c-9d5f3448d108)

### BayesianSolver + NormalHandler vs BayesianSolver + PositionHandler
![Figure_1](https://github.com/user-attachments/assets/99c86906-404d-4d8a-8bb0-8798d4ca0008)

Considering that Wordle allows only 6 attempts, PositionHandler is likely better than NormalHandler

## Prerequisites (for visualization)
- tqdm 
- matplotlib

## To-Do
- [ ] Apply MCTS
