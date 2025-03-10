import tkinter as tk
from solvers import *

def start_game():
    global AGENT
    global ATTEMPT

    ATTEMPT = 0

    if AGENT.__repr__() != f"{solver_select.get()} + {handler_select.get()}":
        solver_class = SOLVERS[SOLVER_NAMES.index(solver_select.get())]
        handler_class = HANDLERS[HANDLER_NAMES.index(handler_select.get())]

        Solver = create(solver_class, handler_class)
        AGENT = Solver(WORDS)

        start_button.config(text="New Game")
        submit_button.config(text="> Submit Feedback <")
    else:
        AGENT.reset()

    update_feedback([1] * WORD_LEN)
    make_guess()

def make_guess():
    # Update attempts
    global ATTEMPT
    ATTEMPT += 1

    result_label.config(text=f"Attempt {ATTEMPT}")

    # Make guess
    try:
        guess = AGENT.make_guess()
    except IndexError:
        result_label.config(text="Error: No guess available")
        return

    update_feedback([1] * WORD_LEN, guess)

def submit_feedback():
    if not AGENT:
        result_label.config(text="Warning: Press Start Game first")
        return

    feedback = [button['bg'] for button in feedback_buttons]
    feedback = [1 if color == 'green' else 0 if color == 'yellow' else -1 for color in feedback]

    if feedback == [1] * WORD_LEN:
        global ATTEMPT
        result_label.config(text=f"Solved in {ATTEMPT} attempts!")

        ATTEMPT = 0
        return
    
    guess = "".join(button.cget("text") for button in feedback_buttons)
    AGENT.filter_words(guess, feedback)
    make_guess()

def update_feedback(feedback, guess=""):
    for i, button in enumerate(feedback_buttons):
        button.config(text=guess[i] if i < len(guess) else " ")  # Show guess letter
        if feedback[i] == 1:
            button.config(bg='green', fg="white")
        elif feedback[i] == 0:
            button.config(bg='yellow')
        else:
            button.config(bg='red')

def change_color(i):
    # Change the color of the button and update feedback
    current_color = feedback_buttons[i]['bg']
    if current_color == 'green':
        feedback_buttons[i].config(bg='yellow', fg="black")
    elif current_color == 'yellow':
        feedback_buttons[i].config(bg='red', fg="white")
    else:
        feedback_buttons[i].config(bg='green')

root = tk.Tk()
root.title("Wordle Solver")

# Read-only global variables
SOLVERS = [BayesianSolver, MinimaxSolver, HeuristicSolver, RandomSolver, FixedSolver]
HANDLERS = [Handler, PositionHandler]

SOLVER_NAMES = [s.__name__ for s in SOLVERS]
HANDLER_NAMES = [h.__name__ for h in HANDLERS]

WORDS = load_words()
WORD_LEN = len(WORDS[0])

# Global variables
AGENT = None
ATTEMPT = 0

# TK
solver_select = tk.StringVar(value=SOLVERS[0].__name__)
handler_select = tk.StringVar(value=HANDLERS[0].__name__)

tk.Label(root, text="Select a Solver: \t\t\t").pack(padx=10)
tk.OptionMenu(root, solver_select, *map(str, SOLVER_NAMES)).pack()

tk.Label(root, text="Select a Handler:\t\t\t").pack(padx=10, pady=(5, 0))
tk.OptionMenu(root, handler_select, *map(str, HANDLER_NAMES)).pack()

start_button = tk.Button(root, text="> Start Game <", command=start_game)
start_button.pack(pady=10)

# Create a Frame to group the color buttons together
color_frame = tk.Frame(root)
color_frame.pack()

feedback_buttons = []
for i in range(WORD_LEN):
    button = tk.Button(
        color_frame,
        text=" ",
        width=3,
        height=1,
        bg='green',
        font=("Arial", 15),
        fg="white",
        command=lambda i=i: change_color(i))
    button.pack(side=tk.LEFT, padx=1)
    feedback_buttons.append(button)

submit_button = tk.Button(root, text="Submit Feedback", command=submit_feedback)
submit_button.pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()