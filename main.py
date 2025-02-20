import random

def load_words(path="words.txt"):
    with open(path, 'r') as f:
        return f.read().splitlines()

def get_feedback(guess, answer):
    """Generate Wordle-style feedback for the guess."""
    feedback = []
    for g, a in zip(guess, answer):
        if g == a:
            feedback.append("🟩")  # Correct letter & position
        elif g in answer:
            feedback.append("🟨")  # Correct letter, wrong position
        else:
            feedback.append("⬜")  # Wrong letter
    return " ".join(feedback)

def main():
    words = load_words()
    attempts = 6  # Wordle allows 6 guesses
    
    print(f"Welcome to Wordle!")

    while True:
        answer = random.choice(words)  # Select a random word

        for attempt in range(1, attempts + 1):
            while True:
                guess = input(f"Attempt {attempt}/{attempts}: ").strip().upper()

                if len(guess) != 5:
                    print(f"Invalid input. Please enter a 5-letter word.")
                else:
                    break

            if guess == answer:
                print("Congratulations! You guessed the word correctly!")
                break
            
            feedback = get_feedback(guess, answer)
            print(f"Feedback: {feedback}")

        print(f"The correct word was: {answer}\n")

if __name__ == "__main__":
    main()