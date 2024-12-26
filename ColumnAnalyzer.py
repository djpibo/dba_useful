import re
import tkinter as tk
from tkinter import ttk


def process_text(line):
    pattern = r'(\w+)\s+.*\s+(NUMBER\(\d+(?:,\d+)?\))'
    match = re.search(pattern, line)

    if match and 'NUMBER' in line:
        column_name = match.group(1)
        number_type = match.group(2)
        return f"{column_name}, {number_type}"
    else:
        return None

def process_input():
    input_text = input_box.get("1.0", tk.END)
    output_text = process_text(input_text)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, output_text)

# GUI 설정
root = tk.Tk()
root.title("SQL Column Processor")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# 입력 박스
input_label = ttk.Label(frame, text="입력:")
input_label.grid(row=0, column=0, sticky=tk.W, pady=5)
input_box = tk.Text(frame, width=50, height=10)
input_box.grid(row=1, column=0, pady=5)

# 처리 버튼
process_button = ttk.Button(frame, text="처리", command=process_input)
process_button.grid(row=2, column=0, pady=10)

# 출력 박스
output_label = ttk.Label(frame, text="출력:")
output_label.grid(row=3, column=0, sticky=tk.W, pady=5)
output_box = tk.Text(frame, width=50, height=10)
output_box.grid(row=4, column=0, pady=5)

root.mainloop()
