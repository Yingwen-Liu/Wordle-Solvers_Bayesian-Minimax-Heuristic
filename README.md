# Wordle Solvers

Apply Bayesian/Minimax/Heuristic solvers to solve the Wordle game
- `words.txt`: 2308 Wordle words from [Silicon Valley Daily](https://svdaily.com/2022/04/15/all-of-the-words-used-in-ny-times-wordle-game/ )
- `game.py`: A rough version of Wordle. Able to play manually
- `test.py`: Test all the solvers and provide an overview
- `wordle_solver.py`: source code of the Wordle Solver app.
- `solvers.py`: Includes **Handlers** and **Solvers**. Able to manually test the selected solver

## Releases
Download both `WordleSolver.exe` and `word.txt`. You can update word.txt with the newest Wordle database.

> [Download HERE](https://github.com/Yingwen-Liu/Wordle_Solvers_Bayesian_Minimax_Heuristic/releases)

*Note that Window Defender likes to delete the app :(*

## Handlers
- `Handler`: Ability to remove words that not match the feedback from the word list.
- `PositionHandler`: **ILLEGAL approach. Assume you are allow to select any letters not in the word list**. Ability to assign the most frequent letters to the green positions (where the letter is correct)

## Solvers
| Solver            | Average Attempts (Handler) | (Handler + *All) | (PositionHandler) | Time Consumption |
| ----------------- | -------------------------- | ---------------- | ----------------- | ---------------- |
| `BayesianSolver`  | 3.6050                     |                  | 3.5998            | Very high        |
| `MinimaxSolver`   | 3.6786                     |                  | 3.6726            | High             |
| `HeuristicSolver` | 3.6626                     |                  | 3.6141            | Very low         |
| `RandomSolver`    | ~4.1                       | N/A              | -                 |                  |
| `FixedSolver`     | 3.9835                     | N/A              | 3.9359            |                  |

*All: set the seach range as the entire database, not the filtered words, which means more words need to check

- `BayesianSolver`: Apply Bayesian search to find the word with highest entropy
- `MinimaxSolver`: Maximize the minimum gain. Solve in fewest steps
- `HeuristicSolver`: Make guess based on the most frequently word
- `RandomSolver`: Randomly select a word from the word list
- `FixedSolver`: Select the word that in the middle of the word list. A better standard of evaluation than `RandomSolver`

## Graphs
### With Handler
<img src="https://github.com/user-attachments/assets/0844fd38-8be4-430d-8578-e70e1d1d7fb6" alt="solvers_comparison" width="800"/>

### With PositionHandler
<img src="https://github.com/user-attachments/assets/d0516efd-cf93-4746-8b6a-b3309cf1caa1" alt="solvers_comparison_with_PositionHandler" width="800"/>

### BayesianSolver + Handler vs BayesianSolver + PositionHandler
*Considering that Wordle allows only 6 attempts, PositionHandler is likely better than Handler*

<img src="https://github.com/user-attachments/assets/99c86906-404d-4d8a-8bb0-8798d4ca0008" alt="Handler_vs_PositionHandler" width="500"/>

### MinimaxSolver + Handler vs HeuristicSolver + Handler
*The 2 different algorithm share a similar result, probably due to they are both based on letter frequency*

<img src="https://github.com/user-attachments/assets/80ecad11-dd30-4358-95af-3478a6776fd1" alt="Handler_vs_PositionHandler" width="500"/>

## Prerequisites (for visualization)
- tqdm
- matplotlib
- Tkinter

## To-Do
- [ ] Apply LSTM
