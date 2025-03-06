import tkinter as tk
from tkinter import filedialog
from collections import Counter
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Function to calculate word percentages
def calculate_word_percentages(filename):
    with open(filename, 'r') as file:
        text = file.read().lower()  # Read text and convert to lowercase

    # Use regex to split the text into words
    words = re.findall(r'\b\w+\b', text)

    # Calculate the total number of words
    total_words = len(words)

    # Count the occurrences of each word
    word_counts = Counter(words)

    # Calculate percentages
    word_percentages = {word: (count / total_words) * 100 for word, count in word_counts.items()}

    return word_percentages, total_words


# Function to display word percentages in the text and chart
def display_percentages():
    filename = filedialog.askopenfilename(title="Select a Text File", filetypes=[("Text files", "*.txt")])
    if not filename:
        return

    # Calculate the word percentages
    word_percentages, total_words = calculate_word_percentages(filename)

    # Clear the text widget
    text_widget.delete(1.0, tk.END)

    # Display word percentages in the text widget
    for word, percentage in word_percentages.items():
        text_widget.insert(tk.END, f"{word} – {percentage:.2f}%\n")

    # Clear the old plot (if any)
    for widget in chart_frame.winfo_children():
        widget.destroy()

    # Generate the new bar chart
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(word_percentages.keys(), word_percentages.values(), color='skyblue')
    ax.set_xlabel('Words')
    ax.set_ylabel('Percentage (%)')
    ax.set_title(f'Word Percentages in {filename}')
    plt.xticks(rotation=90)

    # Embed the matplotlib figure in tkinter
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


# Set up the main window
root = tk.Tk()
root.title("Word Percentage Calculator")
root.geometry("600x500")

# Set up the text widget for displaying word percentages
text_widget = tk.Text(root, height=15, width=50)
text_widget.pack(pady=10)

# Set up the button to calculate percentages
calculate_button = tk.Button(root, text="Calculate Word Percentages", command=display_percentages)
calculate_button.pack(pady=10)

# Set up the frame for the matplotlib chart
chart_frame = tk.Frame(root)
chart_frame.pack(fill=tk.BOTH, expand=True)

# Run the application
root.mainloop()
