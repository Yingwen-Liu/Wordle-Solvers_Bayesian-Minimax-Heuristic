from collections import defaultdict
from tqdm import tqdm
from solvers import *

def test_solver(agent):
    """
    Test all solvers by looping through a subset of words from the database.
    Measures the average number of attempts needed to guess the correct word.
    """
    progress_bar = tqdm(agent.db, desc=f"Testing {agent}")
    result = defaultdict(int)
    avg_attempt = 0

    for i, answer in enumerate(progress_bar, start=1):
        attempt = 1
            
        while True:
            guess = agent.make_guess()
            if guess == answer:
                break
            
            feedback = get_feedback(guess, answer)
            agent.filter_words(guess, feedback)
            attempt += 1
        
        result[attempt] += 1
        avg_attempt += attempt

        agent.reset()
        progress_bar.set_postfix(avg=f"{avg_attempt / i:.4f}")
    
    return result
    
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # BayesianSolver, GreedySolver, GreedierSolver, RandomSolver, FixedSolver
    # NormalHandler, PositionHandler
    solvers = [
        (BayesianSolver, NormalHandler),
        (GreedySolver, NormalHandler),
        (GreedierSolver, NormalHandler),
        (FixedSolver, NormalHandler),
    ]

    solvers = [create(*s) for s in solvers]
    results = []

    words = load_words()
    for solver in solvers:
        agent = solver(words)
        result = test_solver(agent)

        x, y = zip(*sorted(result.items()))
        plt.plot(x, y, label=agent, marker='o')
    
    plt.xlabel("Attempts")
    plt.ylabel("Frequency")

    plt.legend()
    plt.show()

