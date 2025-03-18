import tkinter as tk
from tkinter import filedialog
from collections import Counter
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd


def calculate_number_percentages(filename):
    try:
        df = pd.read_csv(filename, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(filename, encoding='cp1252')

    text = " ".join(df.astype(str).values.flatten()).lower()
    numbers = re.findall(r'\b\d+\b', text)
    total_numbers = len(numbers)
    number_counts = Counter(numbers)
    number_percentages = {num: (count / total_numbers) * 100 for num, count in number_counts.items()}

    return number_percentages, total_numbers


def display_percentages():
    filename = filedialog.askopenfilename(title="Select a CSV File", filetypes=[("CSV files", "*.csv")])
    if not filename:
        return

    number_percentages, total_numbers = calculate_number_percentages(filename)

    text_widget.delete(1.0, tk.END)

    for number, percentage in number_percentages.items():
        text_widget.insert(tk.END, f"{number} – {percentage:.2f}%\n")

    for widget in chart_frame.winfo_children():
        widget.destroy()

    no_numbers_displayed = min(50, len(number_percentages))
    sorted_number_percentages = dict(
        sorted(number_percentages.items(), key=lambda item: item[1], reverse=True)[:no_numbers_displayed])

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(list(sorted_number_percentages.keys()), list(sorted_number_percentages.values()), color='skyblue')
    ax.set_xlabel('Percentage (%)')
    ax.set_ylabel('Numbers')
    ax.set_title(f'Top {no_numbers_displayed} Number Percentages in {filename}')

    for i, (number, percentage) in enumerate(sorted_number_percentages.items()):
        ax.text(percentage + 0.5, i, f'{percentage:.2f}%', va='center', fontweight='bold')

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


root = tk.Tk()
root.title("Numbers frequency")
root.geometry("1920x1080")

text_widget = tk.Text(root, height=15, width=120, font=("Arial", 12))
text_widget.pack(pady=10)

calculate_button = tk.Button(root, text="Process numbers frequency", command=display_percentages, font=("Arial", 20))
calculate_button.pack(pady=10)

chart_frame = tk.Frame(root)
chart_frame.pack(fill=tk.BOTH, expand=True)

root.mainloop()
