import tkinter as tk
from solvers import *
from decision_tree import TreeDB

# --- Constants ---
SOLVERS = [Bayesian, Minimax, Heuristic, Random, Fixed]
SOLVER_NAMES = [s.__name__ for s in SOLVERS]

WORDS = load_words()
WORD_LEN = len(WORDS[0])

COLOR_MAP = {'green': 1, 'yellow': 0, 'black': -1}
COLOR_CYCLE = {
    'green': ('yellow', 'black'),
    'yellow': ('black', 'white'),
    'black': ('green', 'white'),
}

# --- Global variables ---
agent = None
tree = None
attempt = None
feedback = None

# --- Functions ---
def start_game():
    """Starts or resets the game"""
    global agent, tree, attempt
    attempt = 0

    if agent is None or agent.__repr__() != f"{selected_solver.get()}{"All" if search_all.get() else "Filtered"}":
        Solver = SOLVERS[SOLVER_NAMES.index(selected_solver.get())]

        agent = Solver(WORDS, search_all.get())

        if decision_tree.get():
            tree = TreeDB(agent.__repr__())
        elif tree:
            # Close the decision tree if it was previously opened
            tree.close()
            tree = None

        start_button.config(text="New Game")
        submit_button.config(text="> Submit Feedback <")

    else:
        agent.reset()

    init_feedback()
    make_guess()

def make_guess():
    """Makes a guess and updates the UI"""
    # Update attempts
    global attempt
    attempt += 1
    result_label.config(text=f"Attempt {attempt}")

    # Make guess
    if decision_tree.get() and agent.__repr__() != "RandomSolver":
        guess = tree.get_node(agent.make_guess, feedback)
    else:
        guess = agent.make_guess()

    if not guess:
        result_label.config(text="Error: No guess available")
        return

    init_feedback(guess)

def submit_feedback():
    """Processes user feedback and updates the solver"""
    if agent is None:
        result_label.config(text="Warning: Press Start Game first")
        return

    global feedback
    feedback = [COLOR_MAP[button.cget("bg")] for button in feedback_buttons]

    # Handle the case where Wordle is solved
    if feedback == [1] * WORD_LEN:
        global attempt
        result_label.config(text=f"Solved in {attempt} attempts!")
        attempt = 0
        return
    
    guess = "".join(button.cget("text") for button in feedback_buttons)
    agent.filter_words(guess, feedback)
    make_guess()

def init_feedback(guess=" " * WORD_LEN):
    """Initialize the feedback buttons' text and color"""
    for i, button in enumerate(feedback_buttons):
        button.config(text=guess[i], bg='green', fg='white')

def change_color(i):
    """Cycles through feedback colors on button click."""
    next_color, next_text_color = COLOR_CYCLE[feedback_buttons[i].cget("bg")]
    feedback_buttons[i].config(bg=next_color, fg=next_text_color)


# --- GUI Setup ---
root = tk.Tk()
root.title("Wordle Solver")

# Solver Selection
selected_solver = tk.StringVar(value=SOLVERS[0].__name__)
tk.Label(root, text="Select a Solver:\t\t    ").pack(padx=10)
tk.OptionMenu(root, selected_solver, *SOLVER_NAMES).pack()

# Search All Checkbox
search_all = tk.IntVar(value=1)
tk.Checkbutton(root, text="Search All Words", variable=search_all).pack()

# Decision Tree Checkbox
decision_tree = tk.IntVar(value=1)
tk.Checkbutton(root, text="Pre-Trained Solver", variable=decision_tree).pack()

# Start Game Button
start_button = tk.Button(root, text="> Start Game <", command=start_game)
start_button.pack(pady=8)

# Feedback Buttons
color_frame = tk.Frame(root)
color_frame.pack()

feedback_buttons = []
for i in range(WORD_LEN):
    button = tk.Button(
        color_frame, text=" ", width=3, height=1, bg='green',
        font=15, fg="white", command=lambda i=i: change_color(i))
    button.pack(side=tk.LEFT, padx=1)
    feedback_buttons.append(button)

# Submit Button
submit_button = tk.Button(root, text="Submit Feedback", command=submit_feedback)
submit_button.pack(pady=10)

# Result Label
result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
