from collections import defaultdict
from tqdm import tqdm
from solvers import *
from decision_tree import TreeDB

def test_solver(agent, tree):
    """
    Test all solvers by looping through a subset of words from the database.
    Measures the average number of attempts needed to guess the correct word.
    """
    progress_bar = tqdm(agent.db, desc=f"Testing {agent}")
    result = defaultdict(int)
    avg_attempt = 0

    if agent.__repr__() != "RandomSolver":
        make_guess = tree.get_node
    else:
        # RandomSolver doesn't use the decision tree
        make_guess = agent.make_guess

    for i, answer in enumerate(progress_bar, start=1):
        attempt = 1

        feedback = None
        while True:
            # Make a guess and get feedback
            guess = make_guess(agent.make_guess, feedback)
            
            if guess == answer:
                break
            
            feedback = get_feedback(guess, answer)
            agent.filter_words(guess, feedback)

            attempt += 1
        
        # Store the result in the database
        result[attempt] += 1
        avg_attempt += attempt

        agent.reset()

        progress_bar.set_postfix(avg=f"{avg_attempt / i:.4f}")
    
    tree.close()
    return result
    
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # Solvers: Bayesian, Minimax, Heuristic, Random, Fixed
    # (solver, search_all)
    solvers = [
        (Bayesian, True),
        #(Bayesian, False),
        (Minimax, True),
        #(Minimax, False),
        #(Heuristic, True),
        (Heuristic, False),
        #(Random, False),
        (Fixed, False),
    ]

    results = []
    words = load_words()
    
    for solver, search_all in solvers:
        agent = solver(words, search_all)
        tree = TreeDB(agent.__repr__())

        result = test_solver(agent, tree)

        # Plot the results
        x, y = zip(*sorted(result.items()))
        print(f"y: {y}")
        plt.plot(x, y, label=agent, marker='o')
    
    plt.xlabel("Attempts")
    plt.ylabel("Frequency")

    plt.legend()
    plt.show()

