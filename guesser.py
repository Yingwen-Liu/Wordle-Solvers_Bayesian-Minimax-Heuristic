import tkinter as tk
from solvers import *

# --- Constants ---
SOLVERS = [BayesianSolver, MinimaxSolver, HeuristicSolver, RandomSolver, FixedSolver]
HANDLERS = [Handler, PositionHandler]

SOLVER_NAMES = [s.__name__ for s in SOLVERS]
HANDLER_NAMES = [h.__name__ for h in HANDLERS]

WORDS = load_words()
WORD_LEN = len(WORDS[0])

COLOR_MAP = {'green': 1, 'yellow': 0, 'white': -1}
COLOR_CYCLE = {
    'green': ('yellow', 'black'),
    'yellow': ('white', 'black'),
    'white': ('green', 'white'),
}

# --- Global variables ---
AGENT = None
ATTEMPT = None

# --- Functions ---
def start_game():
    """Starts or resets the game"""
    global AGENT, ATTEMPT
    ATTEMPT = 0

    selected_repr = f"{SELECTED_SOLVER.get()} {SELECTED_HANDLER.get()} {"All" if SEARCH_ALL.get() else ''}"
    if AGENT is None or AGENT.__repr__() != selected_repr:
        solver_class = SOLVERS[SOLVER_NAMES.index(SELECTED_SOLVER.get())]
        handler_class = HANDLERS[HANDLER_NAMES.index(SELECTED_HANDLER.get())]

        AGENT = create(solver_class, handler_class, SEARCH_ALL)(WORDS)

        START_BUTTON.config(text="New Game")
        SUBMIT_BUTTON.config(text="> Submit Feedback <")
    else:
        AGENT.reset()

    init_feedback()
    make_guess()

def make_guess():
    """Makes a guess and updates the UI"""
    # Update attempts
    global ATTEMPT
    ATTEMPT += 1
    RESULT_LABEL.config(text=f"Attempt {ATTEMPT}")

    # Make guess
    try:
        guess = AGENT.make_guess()
    except IndexError:
        RESULT_LABEL.config(text="Error: No guess available")
        return

    init_feedback(guess)

def submit_feedback():
    """Processes user feedback and updates the solver"""
    if AGENT is None:
        RESULT_LABEL.config(text="Warning: Press Start Game first")
        return

    feedback = [COLOR_MAP[button.cget("bg")] for button in FEEDBACK_BUTTONS]

    # Handle the case where Wordle is solved
    if feedback == [1] * WORD_LEN:
        global ATTEMPT
        RESULT_LABEL.config(text=f"Solved in {ATTEMPT} attempts!")
        ATTEMPT = 0
        return
    
    guess = "".join(button.cget("text") for button in FEEDBACK_BUTTONS)
    AGENT.filter_words(guess, feedback)
    make_guess()

def init_feedback(guess=" " * WORD_LEN):
    """Initialize the feedback buttons' text and color"""
    for i, button in enumerate(FEEDBACK_BUTTONS):
        button.config(text=guess[i], bg='green', fg='white')

def change_color(i):
    """Cycles through feedback colors on button click."""
    next_color, next_text_color = COLOR_CYCLE[FEEDBACK_BUTTONS[i].cget("bg")]
    FEEDBACK_BUTTONS[i].config(bg=next_color, fg=next_text_color)


# --- GUI Setup ---
root = tk.Tk()
root.title("Wordle Solver")

# Solver Selection
SELECTED_SOLVER = tk.StringVar(value=SOLVERS[0].__name__)
tk.Label(root, text="Select a Solver: \t\t  ").pack(padx=10)
tk.OptionMenu(root, SELECTED_SOLVER, *SOLVER_NAMES).pack()

# Handler Selection
SELECTED_HANDLER = tk.StringVar(value=HANDLERS[0].__name__)
tk.Label(root, text="Select a Handler:\t\t  ").pack(padx=10, pady=(5, 0))
tk.OptionMenu(root, SELECTED_HANDLER, *HANDLER_NAMES).pack()

# Search All Checkbox
SEARCH_ALL = tk.IntVar(value=1)
tk.Checkbutton(root, text="Search All Words", variable=SEARCH_ALL).pack()

# Start Game Button
START_BUTTON = tk.Button(root, text="> Start Game <", command=start_game)
START_BUTTON.pack(pady=10)

# Feedback Buttons
color_frame = tk.Frame(root)
color_frame.pack()

FEEDBACK_BUTTONS = []
for i in range(WORD_LEN):
    button = tk.Button(
        color_frame, text=" ", width=3, height=1, bg='green',
        font=15, fg="white", command=lambda i=i: change_color(i))
    button.pack(side=tk.LEFT, padx=1)
    FEEDBACK_BUTTONS.append(button)

# Submit Button
SUBMIT_BUTTON = tk.Button(root, text="Submit Feedback", command=submit_feedback)
SUBMIT_BUTTON.pack(pady=10)

# Result Label
RESULT_LABEL = tk.Label(root, text="")
RESULT_LABEL.pack()

root.mainloop()