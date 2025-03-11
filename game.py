import random

def load_words(path="words.txt"):
    with open(path, 'r') as f:
        return f.read().splitlines()

def get_feedback(guess, word):
    """Generate Wordle-style feedback for the guess."""
    feedback = ["⬜"] * len(guess)
    counts = {}
    
    # Identify exact matches
    for i, (g, w) in enumerate(zip(guess, word)):
        if g == w:
            feedback[i] = "🟩"
        else:
            counts[w] = counts.get(w, 0) + 1

    # Identify misplaced letters
    for i, g in enumerate(guess):
        if feedback[i] == "⬜" and counts.get(g, 0) > 0:
            feedback[i] = "🟨"
            counts[g] -= 1  # Reduce count to prevent overuse

    return ''.join(feedback)

def main():
    words = load_words()
    attempts = 6  # Wordle allows 6 guesses
    
    print(f"Welcome to Wordle!")

    while True:
        answer = random.choice(words)  # Select a random word

        for attempt in range(1, attempts + 1):
            while True:
                guess = input(f"Attempt {attempt}/{attempts}: ").strip().upper()

                if len(guess) == 5:
                    break
                if guess.lower() == 'q':
                    raise Exception("Game quitted.")
                print(f"Invalid input. Please enter a 5-letter word.")

            if guess == answer:
                print("Congratulations! You guessed the word correctly!")
                break
            
            feedback = get_feedback(guess, answer)
            print(f"Feedback: {feedback}")

        print(f"The correct word was: {answer}\n")

if __name__ == "__main__":
    main()
