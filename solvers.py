import random
import math
import collections

def load_words(path="Downloads\Wordle_search_tree\words.txt"):
    import os

    with open(path, 'r') as f:
        return f.read().splitlines()

def get_feedback(guess, answer):
    """Generate Wordle-style feedback for the guess."""
    feedback = [-1] * len(guess)
    answer_counts = collections.Counter(answer)
    
    # Identify exact matches
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            feedback[i] = 1
            answer_counts[g] -= 1  # Reduce count since it's used

    # Identify misplaced letters
    for i, g in enumerate(guess):
        if feedback[i] == -1 and answer_counts[g] > 0:
            feedback[i] = 0
            answer_counts[g] -= 1  # Reduce count to prevent overuse

    return feedback

class Solver:
    def __init__(self, words):
        self.words = words
        self.length = len(words[0])
        self.green_pos = [0] * self.length
    
    def filter_words(self, guess, feedback):
        self.words = [word for word in self.words if self.match_feedback(guess, word, feedback)]
        self.green_pos = [1 if feedback[i] == 1 else self.green_pos[i] for i in range(self.length)]

    def match_feedback(self, guess, word, feedback):
        word_counts = collections.Counter(word)

        for g, c, f in zip(guess, word, feedback):
            # Exact match
            if f == 1 and c != g:
                return False
            # Letter should not exist in the word
            elif f == -1 and g in word:
                return False
            # Misplaced letter
            elif f == 0:
                if g not in word or c == g or word_counts[g] <= 0:
                    return False
                word_counts[g] -= 1

        return True

class BayesianSolver(Solver):
    def compute_information_gain(self, guess):
        feedback_distribution = collections.defaultdict(int)

        for word in self.words:
            feedback = tuple(get_feedback(guess, word))  # Convert list to tuple for dict key
            feedback_distribution[feedback] += 1

        # Compute entropy (expected information gain)
        total_words = len(self.words)
        entropy = -sum((count / total_words) * math.log2(count / total_words)
                    for count in feedback_distribution.values() if count > 0)  # Avoid log2(0)

        return entropy

    def make_guess(self):
        # If only one or 2 words are left, return the first one
        if len(self.words) <= 2:
            return self.words[0]

        # Bayesian selection using precomputed entropy values
        best_guess = max(self.words, key=self.compute_information_gain)
        return best_guess

class MLESolver(Solver):
    def compute_mle_score(self, word, letter_probs):
        """Compute Maximum Likelihood Estimation (MLE) score for a given word."""
        score = 0.0
        seen_letters = set()
        
        for i, char in enumerate(word):
            if char in seen_letters:
                continue  # Avoid over-counting duplicate letters in the word
            if char in letter_probs[i]:
                score += math.log(letter_probs[i][char])  # Log-probability for stability
            seen_letters.add(char)
        
        return score

    def make_guess(self):
        """Make the best guess based on MLE."""
        if len(self.words) <= 2:
            return self.words[0]

        # Compute letter probabilities at each position
        letter_probs = [{} for _ in range(self.length)]
        total_words = len(self.words)

        for word in self.words:
            for i, char in enumerate(word):
                letter_probs[i][char] = letter_probs[i].get(char, 0) + 1

        # Convert counts to probabilities
        for i in range(self.length):
            for char in letter_probs[i]:
                letter_probs[i][char] /= total_words

        # Choose the word with the highest likelihood score
        best_guess = max(self.words, key=lambda word: self.compute_mle_score(word, letter_probs))
        return best_guess

class GreedySolver(Solver):
    def make_guess(self):
        if len(self.words) <= 2:
            return self.words[0]
        
        counts_list = [{} for _ in range(self.length)]
        # Count letter frequency at each position
        for i in range(self.length):
            if self.green_pos[i]:
                continue
            for w in self.words:
                counts_list[i][w[i]] = counts_list[i].get(w[i], 0) + 1

        guess = list(self.words[0])
        guessed_chars = set()
        # Select the most frequent letter at each position
        for i in range(self.length):
            if counts_list[i]:
                char = max(counts_list[i], key=counts_list[i].get)
                guess[i] = max(counts_list[i], key=counts_list[i].get)
                guessed_chars.add(char)
        
        # Handle green positions by selecting high-frequency letters that are not already used
        if sum(self.green_pos) > 0:
            overall_counts = {}
            for i in range(self.length):
                if not self.green_pos[i]:
                    continue
                for key, value in counts_list[i].items():
                    if key not in guessed_chars:
                        overall_counts[key] = overall_counts.get(key, 0) + value
        
            sorted_counts = sorted(overall_counts.items(), key=lambda x: x[1], reverse=True)
        
            for i in range(self.length):
                if self.green_pos[i] and sorted_counts:
                    guess[i] = sorted_counts.pop()[0]

        return ''.join(guess)

class RandomSolver(Solver):
    def make_guess(self):
        return random.choice(self.words)

def main(solver):
    words = load_words()
    attempts = 6    # Allow 6 guesses

    while True:
        answer = random.choice(words)  # Select a random word
        print(answer)
        agent = solver(words)

        for attempt in range(1, attempts + 1):
            guess = agent.make_guess()
            print(f"Attempt {attempt}/{attempts}: {guess}")

            if guess == answer:
                print("Congratulations! You guessed the word correctly!")
                break
            
            feedback = get_feedback(guess, answer)
            print(f"Feedback: {feedback}")
            agent.filter_words(guess, feedback)

        print(f"The correct word was: {answer}")

        if input("Press Enter to play again...\n") == 'q':
            break

if __name__ == "__main__":
    main(RandomSolver)
