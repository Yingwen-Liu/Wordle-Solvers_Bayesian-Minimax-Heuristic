import random
from collections import Counter

def load_words(path="Downloads\Wordle_search_tree\words.txt"):
    import os

    with open(path, 'r') as f:
        return f.read().splitlines()

def get_feedback(guess, answer):
    """Generate Wordle-style feedback for the guess."""
    feedback = [-1] * len(guess)
    answer_counts = Counter(answer)
    
    # First pass: Check for exact matches
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            feedback[i] = 1
            answer_counts[g] -= 1
    
    # Second pass: Check for misplaced letters
    for i, g in enumerate(guess):
        if feedback[i] == -1 and answer_counts[g] > 0:
            feedback[i] = 0
            answer_counts[g] -= 1
    
    return feedback

class Solver:
    def __init__(self, words):
        self.words = words
        self.guessed_answer = [0, 0, 0, 0, 0]
    
    def filter_words(self, guess, feedback):
        self.words = [word for word in self.words if self.match_feedback(guess, word, feedback)]

    def match_feedback(self, guess, word, feedback):
        word_counts = Counter(word)
        
        # Verify exact matches
        for i, (g, f) in enumerate(zip(guess, feedback)):
            if f == 1 and word[i] != g:
                return False
            elif f == -1 and g in word:
                return False
        
        # Verify misplaced letters
        for i, (g, f) in enumerate(zip(guess, feedback)):
            if f == 0:
                if g not in word or word[i] == g or word_counts[g] <= 0:
                    return False
                word_counts[g] -= 1
                
        return True
    
    def make_guess(self):
        """Choose the best next guess by balancing frequency and letter diversity."""
        if not self.words:
            return None
        if len(self.words) == 1:  # If only one word is left, return it immediately
            return self.words[0]
        
        # Calculate letter frequency across remaining words
        letter_frequencies = Counter("".join(self.words))
        
        # Prioritize words that introduce the most unique letters
        def word_score(word):
            unique_letters = set(word)
            frequency_score = sum(letter_frequencies[letter] for letter in unique_letters)
            diversity_score = len(unique_letters)  # More unique letters = better exploration
            return frequency_score + diversity_score * 2  # Weight diversity higher

        return max(self.words, key=word_score)

def main():
    words = load_words()
    attempts = 6  # Wordle allows 6 guesses

    while True:
        #answer = random.choice(words)  # Select a random word
        answer = "SHAPE"
        solver = Solver(words)

        for attempt in range(1, attempts + 1):
            guess = solver.make_guess()
            print(f"Attempt {attempt}/{attempts}: {guess}")

            if guess == answer:
                print("Congratulations! You guessed the word correctly!")
                break
            
            feedback = get_feedback(guess, answer)
            print(f"Feedback: {feedback}")
            solver.filter_words(guess, feedback)

        print(f"The correct word was: {answer}")

        if input("Press Enter to play again...\n") == 'q':
            break

if __name__ == "__main__":
    main()
