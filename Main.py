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

    no_words_displayed = len(word_percentages.items()) if 50 > len(word_percentages.items()) else 50
    sorted_word_percentages = dict(sorted(word_percentages.items(), key=lambda item: item[1], reverse=True)[:no_words_displayed])

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.barh(list(sorted_word_percentages.keys()), list(sorted_word_percentages.values()), color='skyblue')

    ax.set_xlabel('Percentage (%)')
    ax.set_ylabel('Words')
    ax.set_title(f'Top {no_words_displayed} Word Percentages in {filename}')

    for i, (word, percentage) in enumerate(sorted_word_percentages.items()):
        ax.text(percentage + 0.5, i, f'{percentage:.2f}%', va='center', fontweight='bold')

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


root = tk.Tk()
root.title("Word Percentage Calculator")
root.geometry("1920x1080")

text_widget = tk.Text(root, height=15, width=120, font=("Arial", 12))
text_widget.pack(pady=10)

calculate_button = tk.Button(root, text="Calculate Word Percentages", command=display_percentages, font=("Arial", 20))
calculate_button.pack(pady=10)

chart_frame = tk.Frame(root)
chart_frame.pack(fill=tk.BOTH, expand=True)

root.mainloop()
