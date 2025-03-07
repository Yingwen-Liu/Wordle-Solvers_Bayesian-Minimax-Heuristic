import random
import math
from collections import defaultdict

def load_words(path="words.txt"):
    with open(path, 'r') as f:
        return f.read().splitlines()

def get_feedback(guess, word):
    """Generate feedback for the guess."""
    feedback = [-1] * len(guess)
    target_counts = {}
    
    # Identify exact matches
    for i, (g, w) in enumerate(zip(guess, word)):
        if g == w:
            feedback[i] = 1
        else:
            target_counts[w] = target_counts.get(w, 0) + 1

    # Identify misplaced letters
    for i, g in enumerate(guess):
        if feedback[i] == -1 and target_counts.get(g, 0) > 0:
            feedback[i] = 0
            target_counts[g] -= 1  # Reduce count to prevent overuse

    return feedback


# Handlers
class NormalHandler:
    def __init__(self, db):
        self.db = db    # read only words database
        self.words = db.copy()
        self.length = len(db[0])    # word length

        self.green_pos = [0] * self.length

        # Prevent duplicate computation on the first guess 
        self.is_first_guess = False
        self.init_guess = self.make_guess()
        self.is_first_guess = True
    
    def reset(self):
        self.words = self.db.copy()
        self.is_first_guess = True

        self.green_pos = [0] * self.length
    
    def filter_words(self, guess, feedback):
        self.words = [word for word in self.words if self.match_feedback(guess, word, feedback)]

        self.green_pos = [1 if feedback[i] == 1 else self.green_pos[i] for i in range(self.length)]
    
    def match_feedback(self, guess, word, feedback):
        # A modified and faster version of get_feedback
        target_counts = defaultdict(int)
        for f, g, w in zip(feedback, guess, word):
            if f == 1:
                if g != w:
                    return False    # Exact match expected but not found
            else:
                target_counts[w] += 1
        
        for f, g, w in zip(feedback, guess, word):
            if f == 0:
                if g == w or target_counts[g] == 0:
                    return False    # Misplaced letter is either correct or overused
                target_counts[g] -= 1
        
        for f, g in zip(feedback, guess):
            if f == -1 and target_counts[g] > 0:
                return False        # Absent letter should not exist in the word
        
        return True
    
    def make_guess(self):
        if self.is_first_guess:
            self.is_first_guess = False
            return self.init_guess

        if len(self.words) <= 2:
            return self.words[0]
        
        # Construct guess
        return ''.join(self.heuristic())

class PositionHandler(NormalHandler):
    """Handle green positions by assigning them with the highest-frequncy letters"""
    def make_guess(self):
        if self.is_first_guess:
            self.is_first_guess = False
            return self.init_guess

        if len(self.words) <= 2:
            return self.words[0]
        
        guess = self.heuristic()
        counts = self.get_counts()

        # Handle green positions by selecting high-frequency letters that are not already used
        if any(self.green_pos) == 1:
            for i in range(self.length):
                if not self.green_pos[i] and guess[i] in counts:
                    del counts[guess[i]]
            
            sorted_letters = sorted(counts, key=lambda k: counts[k])

            for i in range(self.length):
                if self.green_pos[i] and sorted_letters:
                    guess[i] = sorted_letters.pop()

        return ''.join(guess)
    
    def get_counts(self):
        # Count letter frequency at non green position
        counts = defaultdict(int)

        for i in range(self.length):
            if not self.green_pos[i]:
                counts = defaultdict(int)
                for word in self.words:
                    counts[word[i]] += 1
                
                if len(counts) == 1:    # If only one letter remains, mark it as green
                    self.green_pos[i] = 1
                    continue

                # Count the overall letter frenquency at non green position
                for key, value in counts.items():
                    counts[key] += value
        
        return counts


# Solvers
class BayesianSolver:
    def heuristic(self):
        # Bayesian selection using precomputed entropy values
        return list(max(self.words, key=self.compute_information_gain))
    
    def compute_information_gain(self, guess):
        feedback_distribution = defaultdict(int)

        for word in self.words:
            feedback = tuple(get_feedback(guess, word))
            feedback_distribution[feedback] += 1

        # Compute entropy for the guess
        total_words = len(self.words)
        entropy = -sum((count / total_words) * math.log2(count / total_words)
                    for count in feedback_distribution.values() if count > 0)  # Avoid log2(0)

        return entropy

class GreedySolver:
    """Letter Frequency Heuristic Solver"""
    def heuristic(self):
        counts_positions = [None] * self.length
        self.counts_overall = defaultdict(int)

        for i in range(self.length):
            if not self.green_pos[i]:
                # Count letter frequency at non green position
                counts = defaultdict(int)
                for word in self.words:
                    counts[word[i]] += 1
                
                if len(counts) == 1:    # If only one letter remains, mark it as green
                    self.green_pos[i] = 1
                    continue
                
                counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)
                counts_positions[i] = dict(counts)

                # Count the overall letter frenquency at non green position
                for key, value in counts:
                    self.counts_overall[key] += value
        
        return self.construct_guess(counts_positions)
    
    def construct_guess(self, counts_positions):
        # Find maximum values for each key across all dictionaries
        max_values = {key: max(d.get(key, 0) for d in counts_positions if d) for key in self.counts_overall}
        
        # Construct initial guess
        guess = list(self.words[0])

        # Apply the most frequent letters to the guess
        for i in range(self.length):
            if not self.green_pos[i]:
                for key in counts_positions[i].keys():
                    if counts_positions[i][key] == max_values[key]:
                        guess[i] = key
                        break
        
        return guess
    
    def get_counts(self):
        return self.counts_overall

class GreedierSolver(GreedySolver):
    """A better Letter Frequency Heuristic Solver"""
    def construct_guess(self, counts_positions):
        # Resolve conflicts by selecting letters from the most frequent ones
        pointers = [0] * self.length
        while True:
            assignments = {}
            conflict = False

            # For each dictionary, if it has any candidates available, pick the current candidate.
            for i in range(self.length):
                if not self.green_pos[i] and pointers[i] < len(counts_positions[i]):
                    letter = list(counts_positions[i].keys())[pointers[i]]
                    assignments.setdefault(letter, []).append(i)
            
            # Resolve conflicts: if multiple dictionaries choose the same letter.
            for letter, indices in assignments.items():
                if len(indices) > 1:
                    conflict = True
                    # Select the dictionary with the highest value for the candidate letter.
                    best_index = max(indices, key=lambda i: counts_positions[i][letter])
                    for i in indices:
                        if i != best_index:
                            pointers[i] += 1
            if not conflict:
                break

        # Construct initial guess
        guess = list(self.words[0])

        # Apply the most frequent letters to the guess
        for i in range(self.length):
            if not self.green_pos[i] and pointers[i] < len(counts_positions[i]):
                guess[i] = list(counts_positions[i].keys())[pointers[i]]

        return guess

class MCTSolver:
    pass

class RandomSolver:
    def make_guess(self):
        return random.choice(self.words)

class FixedSolver:
    def make_guess(self, pos=2):
        return self.words[len(self.words) // pos]

def create(solver, handler):
    class Solver(solver, handler):
        def __init__(self, db):
            super().__init__(db)

        def __repr__(self):
            return f"{solver.__name__} + {handler.__name__}"
        
    return Solver


if __name__ == "__main__":
    # BayesianSolver, GreedySolver, GreedierSolver, RandomSolver, FixedSolver
    solver_class = BayesianSolver
    # NormalHandler, PositionHandler
    handler_class = PositionHandler
    
    Solver = create(solver_class, handler_class)

    db = load_words()
    agent = Solver(db)

    while True:
        answer = random.choice(db)  # Select a random word from the database
        print(f"The correct word is: {answer}")

        attempt = 1
        while True:
            guess = agent.make_guess()
            print(f"Attempt {attempt}: {guess}")

            if guess == answer:
                break
            
            feedback = get_feedback(guess, answer)
            print(f"Feedback: {feedback}")
            agent.filter_words(guess, feedback)

            attempt += 1

        if input("Press Enter to play again...") == 'q':
            break

        agent.reset()
        print()
