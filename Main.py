import tkinter as tk
from tkinter import filedialog
from collections import Counter
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def calculate_word_percentages(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read().lower()
    except UnicodeDecodeError:
        with open(filename, 'r', encoding='cp1252') as file:
            text = file.read().lower()

    words = re.findall(r'\b\w+\b', text)

    total_words = len(words)

    word_counts = Counter(words)

    word_percentages = {word: (count / total_words) * 100 for word, count in word_counts.items()}

    return word_percentages, total_words


def display_percentages():
    filename = filedialog.askopenfilename(title="Select a Text File", filetypes=[("Text files", "*.txt")])
    if not filename:
        return

    word_percentages, total_words = calculate_word_percentages(filename)

    text_widget.delete(1.0, tk.END)

    for word, percentage in word_percentages.items():
        text_widget.insert(tk.END, f"{word} – {percentage:.2f}%\n")

    for widget in chart_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(word_percentages.keys(), word_percentages.values(), color='skyblue')
    ax.set_xlabel('Words')
    ax.set_ylabel('Percentage (%)')
    ax.set_title(f'Word Percentages in {filename}')
    plt.xticks(rotation=90)

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


root = tk.Tk()
root.title("Word Percentage Calculator")
root.geometry("600x700")

text_widget = tk.Text(root, height=15, width=120, font=("Arial", 20))
text_widget.pack(pady=10)

calculate_button = tk.Button(root, text="Calculate Word Percentages", command=display_percentages, font=("Arial", 20))
calculate_button.pack(pady=10)

chart_frame = tk.Frame(root)
chart_frame.pack(fill=tk.BOTH, expand=True)

root.mainloop()
