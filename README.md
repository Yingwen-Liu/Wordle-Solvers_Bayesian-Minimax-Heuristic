# Wordle Solvers

Apply Bayesian/Minimax/Heuristic solvers to solve the Wordle game
- `words.txt`: 2308 Wordle words from [Silicon Valley Daily](https://svdaily.com/2022/04/15/all-of-the-words-used-in-ny-times-wordle-game/ )
- `Tools\game.py`: A rough version of Wordle. Run to play manually
- `solvers.py`: Includes **Handler** and **Solvers**. Run to manually test the selected solver
- `tree.db`: A sqlite database, a tree-like structure to store pre-trained solvers
- `decision_tree.py`: Read and update `tree.db`
- `test.py`: Run to test all solvers and generate an overview
- `Tools\test_result.py`: a pre-generated overview for all the solvers

  <img src="https://github.com/user-attachments/assets/2e477f14-ce7c-46d4-8606-e946492cf0b5" alt="ScreenShot" width="400"/>

- `wordle_solver.py`: source code of the Wordle Solver app

  <img src="https://github.com/user-attachments/assets/31633650-d056-4bad-8a0f-9fae2fce5679" alt="ScreenShotApp" width="200"/>

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
<img src="https://github.com/user-attachments/assets/76d03acf-625f-489a-954b-c671ed363e90" alt="All" width="800"/>

### Filtered (search_all=False)
<img src="https://github.com/user-attachments/assets/cf2841a8-0023-4e7d-aaed-6f485b8d955d" alt="Filtered" width="800"/>

### Bayesian Solvers
<img src="https://github.com/user-attachments/assets/d368e4ed-6a0a-4f92-9e4b-8b5c9cf975ff" alt="Bayesian" width="500"/>

### Minimax Solvers
<img src="https://github.com/user-attachments/assets/4864f342-d4e9-4331-8f89-be9dc29402b5" alt="Minimax" width="500"/>

### Heuristic Solvers
<img src="https://github.com/user-attachments/assets/baa00c92-b8f0-4458-a571-fe5c49d84855" alt="Heuristic" width="500"/>

## Prerequisites
- tqdm
- matplotlib
- Tkinter
- sqlite

## To-Do
- [x] Update graphs in README
- [x] Apply decision tree
