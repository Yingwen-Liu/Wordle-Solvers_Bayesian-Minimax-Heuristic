# Wordle Solvers

Apply Bayesian/Minimax/Heuristic solvers to solve the Wordle game
- `words.txt`: 2308 Wordle words from [Silicon Valley Daily](https://svdaily.com/2022/04/15/all-of-the-words-used-in-ny-times-wordle-game/ )
- `game.py`: A rough version of Wordle. Able to play manually
- `solvers.py`: Includes **Handlers** and **Solvers**. Able to manually test the selected solver
- `test.py`: Test selected solvers and generate an overview
- `test_result.py`: a pre-generated overview of all the solvers

  <img src="https://github.com/user-attachments/assets/ca97416d-edef-4985-a4dc-37eca33f923b" alt="ScreenShot" width="400"/>

- `wordle_solver.py`: source code of the Wordle Solver app

  <img src="https://github.com/user-attachments/assets/6d09be33-12c8-4682-acb4-d7ac95f035f6" alt="ScreenShotApp" width="200"/>

## Releases
Download both `WordleSolver.exe` and `word.txt`. You can update word.txt with the newest Wordle database.

> [Download HERE](https://github.com/Yingwen-Liu/Wordle_Solvers_Bayesian_Minimax_Heuristic/releases)

*Note that Window Defender likes to delete the app :(*

## Handlers
- `Handler`: Ability to remove words that not match the feedback from the word list.
- `PositionHandler`: **ILLEGAL approach. Assume you are allow to select any letters not in the word list**. Ability to assign the most frequent letters to the green positions (where the letter is correct)
- `search_all=True`: set the search range as the entire database, not only the filtered words, which means more iterations and much slower execution

## Solvers
| Solver            | Average Attempts (Handler) | (Handler *All) | (PositionHandler) | Time Consumption |
| ----------------- | -------------------------- | -------------- | ----------------- | ---------------- |
| `BayesianSolver`  | 3.6050                     | 3.5613         | 3.5998            | Very high        |
| `MinimaxSolver`   | 3.6786                     | 3.6856         | 3.6726            | High             |
| `HeuristicSolver` | 3.6626                     | 3.7397         | 3.6141            | Very low         |
| `RandomSolver`    | ~4.1                       | -              | -                 | -                |
| `FixedSolver`     | 3.9853                     | -              | 3.9359            | -                |

**All: search_all=True*
**In general, the time consumption of Handler *All >> PositionHandler >= Handler

### Description
- `BayesianSolver`: Apply Bayesian search to find the word with highest entropy
- `MinimaxSolver`: Maximize the minimum gain. Solve in fewest steps
- `HeuristicSolver`: Make guess based on the most frequently word
- `RandomSolver`: Randomly select a word from the word list
- `FixedSolver`: Select the word that in the middle of the word list. A better standard of evaluation than `RandomSolver`

## Graphs
### With Handler search_all=True
<img src="https://github.com/user-attachments/assets/23a1e179-8dae-4a68-8e75-e2a50746bb78" alt="All" width="800"/>

### With Handler search_all=False
<img src="https://github.com/user-attachments/assets/90d4517a-29bf-42e5-ab7b-27aa35c4f8af" alt="Normal" width="800"/>

### With PositionHandler
<img src="https://github.com/user-attachments/assets/9984de40-6d3f-4c99-b7fa-271f961474e0" alt="Position" width="800"/>

### BayesianSolvers
<img src="https://github.com/user-attachments/assets/d368e4ed-6a0a-4f92-9e4b-8b5c9cf975ff" alt="Bayesian" width="500"/>

### MinimaxSolvers
<img src="https://github.com/user-attachments/assets/2434f789-b165-4558-b6eb-8d786bd66eb8" alt="Minimax" width="500"/>

### HeuristicSolver
<img src="https://github.com/user-attachments/assets/0638b18a-7afe-4fab-9c69-0293f7788939" alt="Heuristic" width="500"/>

## Prerequisites (for visualization)
- tqdm
- matplotlib
- Tkinter

## To-Do
- [x] Update graphs in README
- [ ] Apply tree search
