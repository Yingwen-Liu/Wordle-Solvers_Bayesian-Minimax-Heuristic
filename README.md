# Wordle_Solvers

Apply auto solvers to solve the Wordle game

## Solvers
- `GreedySolver`: a letter-frequency heuristic solver, very fast
- `GreedierSolver`: a better letter-frequency heuristic solver, even faster
- `BayesianSolver`: apply bayesian search to find the word that provides the highest entropy.
- `BayesianEnhanceSolver`: similar to `BayesianSolver`, but with heauristic to handle the green positions (where the letter is in correct position)
- `RandomSolver`: randomly select a word from the word list
- `FixedSolver`: select the word that in the middle of the word list. May be better to used as a standard of evaluation than `RandomSolver`
![Figure_1](https://github.com/user-attachments/assets/589d46bc-2587-4bfc-9a6e-78569014b96e)

### `GreedySolver` vs `GreedierSolver`
![GreedyVSGreedier](https://github.com/user-attachments/assets/cd513b02-cefe-4b41-ada6-4beeeb4d8f93)

### `BayesianSolver` vs `BayesianEnhanceSolver`
![BayesianVSEnhance](https://github.com/user-attachments/assets/e0f6c9b3-4ee9-46cd-8eb5-1d4c967b2a81)

## Prerequisites (for visualization)
- tqdm 
- matplotlib

## To-Do
- [ ] Apply MCTS


