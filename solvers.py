import random
import math
from collections import defaultdict, Counter

def load_words(path="Downloads\Wordle_search_tree\words.txt"):
    with open(path, 'r') as f:
        return f.read().splitlines()

def get_feedback(guess, word):
    """Generate Wordle-style feedback for the guess."""
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

class Solver:
    def __init__(self, db):
        self.db = db
        self.words = db.copy()
        self.length = len(db[0])

        self.green_pos = [0] * self.length

        self.is_first_guess = False
    
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
        # Avoid duplicate computation
        if self.is_first_guess:
            self.is_first_guess = False
            return self.init_guess
        
        # If only one or 2 words are left, return the first one
        if len(self.words) <= 2:
            return self.words[0]
        
        ...


class BayesianSolver(Solver):
    def __init__(self, db):
        super().__init__(db)
        self.init_guess = self.make_guess()
        self.is_first_guess = True

    def make_guess(self):
        if self.is_first_guess:
            self.is_first_guess = False
            return self.init_guess
        
        if len(self.words) <= 2:
            return self.words[0]

        # Bayesian selection using precomputed entropy values
        return max(self.words, key=self.compute_information_gain)
    
    def compute_information_gain(self, guess):
        feedback_distribution = defaultdict(int)

        for word in self.words:
            feedback = tuple(get_feedback(guess, word))
            feedback_distribution[feedback] += 1

        # Compute entropy (expected information gain)
        total_words = len(self.words)
        entropy = -sum((count / total_words) * math.log2(count / total_words)
                    for count in feedback_distribution.values() if count > 0)  # Avoid log2(0)

        return entropy


class BayesianEnhanceSolver(BayesianSolver):
    """Bayesian Solver with green position implementation"""
    def make_guess(self):
        if self.is_first_guess:
            self.is_first_guess = False
            return self.init_guess
        
        if len(self.words) <= 2:
            return self.words[0]

        # Bayesian selection using precomputed entropy values
        guess = list(max(self.words, key=self.compute_information_gain))

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


class GreedySolver(Solver):
    """Letter Frequency Heuristic Solver"""
    def __init__(self, db):
        super().__init__(db)
        self.init_guess = self.make_guess()
        self.is_first_guess = True

    def make_guess(self):
        if self.is_first_guess:
            self.is_first_guess = False
            return self.init_guess

        if len(self.words) <= 2:
            return self.words[0]
        
        counts_positions = [None] * self.length
        counts_overall = defaultdict(int)

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
                    counts_overall[key] += value

        # Find maximum values for each key across all dictionaries
        max_values = {key: max(d.get(key, 0) for d in counts_positions if d) for key in counts_overall}
        
        # Construct initial guess
        guess = list(self.words[0])
        used_letters = set()

        # Apply the most frequent letters to the guess
        for i in range(self.length):
            if not self.green_pos[i]:
                for key in counts_positions[i].keys():
                    if counts_positions[i][key] == max_values[key]:
                        guess[i] = key
                        used_letters.add(key)
                        break

        # Handle green positions by selecting high-frequency letters that are not already used
        if any(self.green_pos) == 1:
            for letter in used_letters:
                del counts_overall[letter]
            
            sorted_letters = sorted(counts_overall, key=lambda k: counts_overall[k])

            for i in range(self.length):
                if self.green_pos[i] and sorted_letters:
                    guess[i] = sorted_letters.pop()

        return ''.join(guess)

class GreedierSolver(Solver):
    """Letter Frequency Heuristic Solver"""
    def __init__(self, db):
        super().__init__(db)
        self.init_guess = self.make_guess()
        self.is_first_guess = True

    def make_guess(self):
        if self.is_first_guess:
            self.is_first_guess = False
            return self.init_guess

        if len(self.words) <= 2:
            return self.words[0]
        
        counts_positions = [None] * self.length
        counts_overall = defaultdict(int)

        # Count letter frequency at non green position
        for i in range(self.length):
            if not self.green_pos[i]:
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
                    counts_overall[key] += value

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
        used_letters = set()

        # Apply the most frequent letters to the guess
        for i in range(self.length):
            if not self.green_pos[i] and pointers[i] < len(counts_positions[i]):
                guess[i] = list(counts_positions[i].keys())[pointers[i]]
                used_letters.add(guess[i])

        # Handle green positions by selecting high-frequency letters that are not already used
        if any(self.green_pos) == 1:
            for letter in used_letters:
                del counts_overall[letter]
            
            sorted_letters = sorted(counts_overall, key=lambda k: counts_overall[k])

            for i in range(self.length):
                if self.green_pos[i] and sorted_letters:
                    guess[i] = sorted_letters.pop()

        return ''.join(guess)

class RandomSolver(Solver):
    def make_guess(self):
        return random.choice(self.words)

class FixedSolver(Solver):
    def __init__(self, db, pos=2):
        super().__init__(db)
        self.pos = pos

    def make_guess(self):
        return self.words[len(self.words) // self.pos]


if __name__ == "__main__":
    solver = BayesianEnhanceSolver

    words = load_words()
    agent = solver(words)

    while True:
        answer = random.choice(words)  # Select a random word

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

        print(f"The correct word was: {answer}")

        if input("Press Enter to play again...") == 'q':
            break

        agent.reset()

        print()
