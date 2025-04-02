import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Data for plotting
solvers_data = {
    "BayesianAll": {
        "x": (1, 2, 3, 4, 5, 6),
        "y": (1, 47, 1022, 1136, 100, 3)
    },
    "BayesianFiltered": {
        "x": (1, 2, 3, 4, 5, 6, 7, 8),
        "y": (1, 131, 987, 923, 208, 47, 10, 2)
    },
    "MinimaxAll": {
        "x": (1, 2, 3, 4, 5, 6),
        "y": (1, 40, 811, 1293, 160, 4)
    },
    "MinimaxFiltered": {
        "x": (1, 2, 3, 4, 5, 6, 7, 8),
        "y": (1, 122, 877, 1006, 242, 46, 12, 3)
    },
    "HeuristicAll": {
        "x": (1, 2, 3, 4, 5, 6, 7),
        "y": (1, 104, 771, 1113, 271, 37, 12)
    },
    "HeuristicFiltered": {
        "x": (1, 2, 3, 4, 5, 6, 7, 8),
        "y": (1, 145, 865, 990, 254, 40, 11, 3)
    },
    "Fixed": {
        "x": (1, 2, 3, 4, 5, 6, 7, 8, 9),
        "y": (1, 109, 654, 925, 449, 133, 27, 10, 1)
    },
}

# Function to toggle visibility of lines
def toggle_visibility():
    for label, var in checkbox_states.items():
        lines[label].set_visible(var.get())  # Show/hide line based on checkbox state
    
    # Update legend to only show visible lines
    visible_lines = [line for label, line in lines.items() if checkbox_states[label].get()]
    visible_labels = [label for label, var in checkbox_states.items() if var.get()]
    
    ax.legend(visible_lines, visible_labels)
    canvas.draw()  # Update the Matplotlib canvas in Tkinter

# Function to save the graph as an image
def save_image():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("All Files", "*.*")]
    )
    if file_path:
        fig.savefig(file_path, dpi=300)
        print(f"Graph saved as {file_path}")

# Create Tkinter window
root = tk.Tk()
root.title("Solver Comparison")

# Create Matplotlib figure
fig, ax = plt.subplots()

# Plot all solvers initially
lines = {}
for label, data in solvers_data.items():
    line, = ax.plot(data["x"], data["y"], label=label, marker='o', visible=True)
    lines[label] = line

ax.set_xlabel("Attempts")
ax.set_ylabel("Frequency")
ax.set_title("Solver Comparison")
ax.legend()

# Embed Matplotlib figure into Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create checkboxes in Tkinter window
control_frame = tk.Frame(root)
control_frame.pack(side=tk.BOTTOM, fill=tk.X)

checkbox_states = {}
row, col = 0, 0  # Row and column for grid layout
for label in solvers_data.keys():
    checkbox_states[label] = tk.BooleanVar(value=True)  # Default: checked
    chk = tk.Checkbutton(control_frame, text=label, variable=checkbox_states[label], command=toggle_visibility)
    chk.grid(row=row, column=col, padx=10, pady=2, sticky="w")
    
    col += 1
    if col > 2:  # Move to the next row after 3 checkboxes
        col = 0
        row += 1

# Save Image button
tk.Button(root, text="Save Image", command=save_image).pack(pady=10)

# Run Tkinter main loop
root.mainloop()
