# Wordle_Solvers

Apply auto solvers to solve the Wordle game
- `words.txt`: 2308 Wordle words from [Silicon Valley Daily](https://svdaily.com/2022/04/15/all-of-the-words-used-in-ny-times-wordle-game/ )
- `game.py`: A rough version of Wordle. Able to play manually
- `test.py`: Test all the solvers and provide an overview
- `solvers.py`: Includes **Handlers** and **Solvers**. Able to manually test the selected solver

## Handlers
- `NormalHandler`: ability to remove words that not match the feedback from the word list.
- `PositionHandler`: **Assume that you are allow to select any letters not in the word list**. Additional ability to assign the most frequent letters to the green positions (where the letter is correct)

## Solvers
| Solver | Average Attempts (NormalHandler) | (PositionHandler) | Time Consumption | Description |
| ------ | -------------------------------- | ----------------- | ---------------- | ----------- |
| `BayesianSolver` | 3.6050 | 3.5998 | Very high | Apply Bayesian search to find the word with highest entropy |
| `GreedySolver` | 3.8281 | 3.6548 | Low | A letter-frequency heuristic solver |
| `GreedierSolver` | 3.7990 | 3.6262 | Low | A better letter-frequency heuristic solver |
| `RandomSolver` | ~4.1 | - | | Randomly select a word from the word list |
| `FixedSolver` | 3.9835 | - | | Select the word that in the middle of the word list. A better standard of evaluation than `RandomSolver` |

### Note that `BayesianSolver` with `NormalHandler` is the only LEGAL heuristic solver in the table above

## Graphs
### With NormalHandler
<img src="https://github.com/user-attachments/assets/be05f61d-addd-41cc-a20c-9d5f3448d108" alt="Figure_1" width="800"/>

### With PositionHandler
<img src="https://github.com/user-attachments/assets/d2270ae9-5ec0-4930-8a4d-258972c6cb88" alt="Figure_1" width="800"/>

### BayesianSolver + NormalHandler vs BayesianSolver + PositionHandler
*Considering that Wordle allows only 6 attempts, PositionHandler is likely better than NormalHandler*

<img src="https://github.com/user-attachments/assets/99c86906-404d-4d8a-8bb0-8798d4ca0008" alt="Figure_1" width="500"/>

### GreedySolver + PositionHandler vs GreedierSolver + PositionHandler
*GreedierSolver is overall slightly better than GreedySolver*

<img src="https://github.com/user-attachments/assets/cd513b02-cefe-4b41-ada6-4beeeb4d8f93" alt="Figure_1" width="500"/>

## Prerequisites (for visualization)
- tqdm 
- matplotlib

## To-Do
- [ ] Apply MCTS
