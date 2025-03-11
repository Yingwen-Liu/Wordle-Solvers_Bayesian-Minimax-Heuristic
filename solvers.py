import random
from math import log2
from collections import defaultdict, Counter

def load_words(path="words.txt"):
    with open(path, 'r') as f:
        return f.read().splitlines()

def get_feedback(guess, word):
    """Generate feedback for the guess"""
    feedback = [-1] * len(guess)
    counts = defaultdict(int)
    
    # Identify exact matches
    for i, (g, w) in enumerate(zip(guess, word)):
        if g == w:
            feedback[i] = 1
        else:
            counts[w] += 1

    # Identify misplaced letters
    for i, g in enumerate(guess):
        if feedback[i] == -1 and counts[g] > 0:
            feedback[i] = 0
            counts[g] -= 1  # Reduce count to prevent overuse

    return feedback


# --- Handlers ---
class Handler:
    """Basic algorithm to start the game and filter the words based on the feedback"""
    def __init__(self, db, search_all):
        self.db = db    # read only words database
        self.words = db.copy()
        self.length = len(db[0])    # word length

        # Set up the search range, the entire database or the filtered words
        if search_all:
            self.search_range = db
        else:
            self.search_range = self.words

        # Track the feedback of the green position
        self.green_pos = [0] * self.length

        # Prevent duplicate computation on the first guess 
        self.is_first_guess = False
        self.init_guess = self.make_guess()     # Store the first guess
        self.is_first_guess = True
    
    def reset(self):
        # Reset the word list after each game
        self.words[:] = self.db.copy()
        self.is_first_guess = True

        self.green_pos = [0] * self.length
    
    def filter_words(self, guess, feedback):
        # Filter the word based on the feedback
        self.words[:] = [word for word in self.words if self.match_feedback(guess, word, feedback)]

        self.green_pos = [guess[i] if feedback[i] == 1 else self.green_pos[i] for i in range(self.length)]
    
    def match_feedback(self, guess, word, feedback):
        # A faster version with early exist strategy of get_feedback(guess, word) == feedback
        counts = defaultdict(int)
        for f, g, w in zip(feedback, guess, word):
            if f == 1:
                if g != w:
                    return False    # Exact match expected but not found
            else:
                counts[w] += 1
        
        for f, g, w in zip(feedback, guess, word):
            if f == 0:
                if g == w or counts[g] == 0:
                    return False    # Misplaced letter is either correct or overused
                counts[g] -= 1
        
        for f, g in zip(feedback, guess):
            if f == -1 and counts[g] > 0:
                return False        # Absent letter should not exist in the word
        
        return True
    
    def make_guess(self):
        if self.is_first_guess:
            self.is_first_guess = False
            return self.init_guess

        if len(self.words) <= 2:
            return self.words[0]
        
        # Construct guess
        return self.construct_guess()

class PositionHandler(Handler):
    """Handle green positions by assigning them with the highest-frequncy letters"""
    def make_guess(self):
        if self.is_first_guess:
            self.is_first_guess = False
            return self.init_guess

        if len(self.words) <= 2:
            return self.words[0]
        
        guess = list(self.construct_guess())
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


# --- Solvers ---
class BayesianSolver:
    """Apply Bayesian search to find the word with highest entropy in the word list"""
    def construct_guess(self):
        # Bayesian selection using precomputed entropy values
        return max(self.search_range, key=self.compute_information_gain)
    
    def compute_information_gain(self, guess):
        feedback_distribution = defaultdict(int)

        for word in self.words:
            feedback = tuple(get_feedback(guess, word))
            feedback_distribution[feedback] += 1

        # Compute entropy for the guess
        total_words = len(self.words)
        entropy = -sum((count / total_words) * log2(count / total_words)
                    for count in feedback_distribution.values() if count > 0)  # Avoid log2(0)

        return entropy

class MinimaxSolver:
    """Maximize the minimum gain"""
    def construct_guess(self):
        # Run minimax to find the best guess
        best_guess = None
        min_worst_case = float('inf')
        
        # Simulate all possible feedback scenarios for this guess
        for guess in self.search_range:
            feedback_groups = defaultdict(list)
            for word in self.words:
                feedback = tuple(get_feedback(guess, word))
                feedback_groups[feedback].append(word)
            
            # Calculate the worst-case scenario for this guess
            worst_case = max(len(group) for group in feedback_groups.values())
            
            # Select the guess with the best worst-case outcome
            if worst_case < min_worst_case:
                min_worst_case = worst_case
                best_guess = guess
        
        return best_guess

class HeuristicSolver:
    """Letter Frequency Heuristic Solver"""
    def construct_guess(self):
        position_letter_frequencies = [None] * self.length
        self.overall_letter_frequencies = Counter()

        for i in range(self.length):
            if self.green_pos[i]:
                continue    # skip green positions to reduce computation

            letter_counts = Counter(word[i] for word in self.words)
                
            if len(letter_counts) == 1:    # If only one letter remains, mark it as green
                self.green_pos[i] = 1
                continue
            
            position_letter_frequencies[i] = letter_counts
            self.overall_letter_frequencies.update(letter_counts)
        
        return max(self.search_range, key=lambda guess: self.compute_frequency(guess, position_letter_frequencies))
        
    def compute_frequency(self, guess, position_letter_frequencies):
        # Compute the frequency of each non-green letter in the word
        frequency = 0
        for i in range(self.length):
            if not self.green_pos[i]:
                frequency += position_letter_frequencies[i][guess[i]]
        
        return frequency
        
    def get_counts(self):
        return self.overall_letter_frequencies 

class RandomSolver:
    """Randonly select a word from the word list"""
    def make_guess(self):
        return random.choice(self.words)

class FixedSolver:
    """Select the word at a fixed position the word list"""
    def construct_guess(self, pos=2):
        return self.words[len(self.words) // pos]

def create(solver, handler, search_all):
    """Create a solver class with handler"""
    class Solver(solver, handler):
        def __init__(self, db):
            super().__init__(db, search_all)

        def __repr__(self):
            return f"{solver.__name__} {handler.__name__} {"All" if search_all else ''}"
        
    return Solver


if __name__ == "__main__":
    # BayesianSolver, MinimaxSolver, HeuristicSolver, RandomSolver, FixedSolver
    solver_class = HeuristicSolver
    # Handler, PositionHandler
    handler_class = Handler
    # Choose to whether search the entire database or not
    search_all = False

    db = load_words()
    agent = create(solver_class, handler_class, search_all)(db)

    print("Current solver:", agent)

    while True:
        answer = random.choice(db)      # Select a random word from the database
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

        if input("Press Enter to play again... "):
            break

        agent.reset()
        print()
