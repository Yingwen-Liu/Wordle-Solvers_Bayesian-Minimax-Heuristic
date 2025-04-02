# Wordle Solvers

Apply Bayesian/Minimax/Heuristic solvers to solve the Wordle game
- `words.txt`: 2308 Wordle words from [Silicon Valley Daily](https://svdaily.com/2022/04/15/all-of-the-words-used-in-ny-times-wordle-game/ )
- `Tools\game.py`: A rough version of Wordle. Run to play manually
- `solvers.py`: Includes **Handler** and **Solvers**. Run to manually test the selected solver
- `test.py`: Run to test all solvers and generate an overview
- `Tools\test_result.py`: a pre-generated overview for all the solvers

  <img src="https://github.com/user-attachments/assets/ca97416d-edef-4985-a4dc-37eca33f923b" alt="ScreenShot" width="400"/>

- `wordle_solver.py`: source code of the Wordle Solver app

  <img src="https://github.com/user-attachments/assets/6d09be33-12c8-4682-acb4-d7ac95f035f6" alt="ScreenShotApp" width="200"/>

## Releases
Download both `WordleSolver.exe` and `word.txt`. You can update word.txt with the newest Wordle database.

> [Download HERE](https://github.com/Yingwen-Liu/Wordle_Solvers_Bayesian_Minimax_Heuristic/releases)

*Note that Window Defender likes to delete the app :(*

## Handler
- `Handler`: Ability to remove words that not match the feedback from the word list
- `search_all=True`: set the search range as the entire database, not only the filtered words, which means more iterations and much slower execution

## Solvers
| Solver      | Average Attempts (*Filtered) | (*All)         | Time Consumption |
| ----------- | ---------------------------- | -------------- | ---------------- |
| `Bayesian`  | 3.6050                       | 3.5613         | Very high        |
| `Minimax`   | 3.6786                       | 3.6856         | High             |
| `Heuristic` | 3.6626                       | 3.7397         | Very low         |
| `Random`    | ~4.1                         | -              | -                |
| `Fixed`     | 3.9853                       | -              | -                |

*Filtered: search_all=False
*All: search_all=True*
*In general, the time consumption of Filtered < All

### Description
- `Bayesian`: Apply Bayesian search to find the word with highest entropy
- `Minimax`: Maximize the minimum gain. Solve in fewest steps
- `Heuristic`: Make guess based on the most frequently word
- `Random`: Randomly select a word from the word list
- `Fixed`: Select the word that in the middle of the word list. A better standard of evaluation than `Random` Solver

## Graphs (from `test_result.py`)
### All (search_all=True)
<img src="https://github.com/user-attachments/assets/23a1e179-8dae-4a68-8e75-e2a50746bb78" alt="All" width="800"/>

### Filtered (search_all=False)
<img src="https://github.com/user-attachments/assets/90d4517a-29bf-42e5-ab7b-27aa35c4f8af" alt="Normal" width="800"/>

### Bayesian Solvers
<img src="https://github.com/user-attachments/assets/d368e4ed-6a0a-4f92-9e4b-8b5c9cf975ff" alt="Bayesian" width="500"/>

### Minimax Solvers
<img src="https://github.com/user-attachments/assets/2434f789-b165-4558-b6eb-8d786bd66eb8" alt="Minimax" width="500"/>

### Heuristic Solvers
<img src="https://github.com/user-attachments/assets/0638b18a-7afe-4fab-9c69-0293f7788939" alt="Heuristic" width="500"/>

## Prerequisites
- tqdm
- matplotlib
- Tkinter
- sqlite

## To-Do
- [x] Update graphs in README
- [x] Apply decision tree
