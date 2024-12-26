import tkinter as tk
from tkinter import ttk
import re


def process_input():
    left_input = left_text.get("1.0", tk.END).strip()
    right_input = right_text.get("1.0", tk.END).strip()

    # 빈 줄 제거
    right_lines = [line for line in right_input.split('\n') if line.strip()]

    results = []
    current_table = ""
    column_number = 1

    left_lines = left_input.split('\n')
    print(left_lines)

    for line in right_lines:
        if "이름" in line or "----" in line:
            if current_table:
                column_number = 1
            continue

        if any(table in line for table in left_lines):
            current_table = line.split()[1]
            continue

        parts = line.split()
        if len(parts) >= 3:
            column_name = parts[0]
            data_type = parts[-1]
            length = ""

            if "VARCHAR2" in data_type or "NUMBER" in data_type:
                match = re.search(r'\((\d+(?:,\d+)?)\)', data_type)
                if match:
                    length = match.group(1)
                    data_type = data_type.split('(')[0]
            elif "DATE" in data_type:
                length = "7"

            results.append(f"{current_table}\t{column_name}\t{column_number}\t{data_type}\t{length}")
            print(current_table)
            column_number += 1

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "\n".join(results))


# GUI 설정
root = tk.Tk()
root.title("테이블 구조 분석기")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# 왼쪽 입력 박스 (DESC 테이블 목록)
left_label = ttk.Label(frame, text="DESC 테이블 목록:")
left_label.grid(row=0, column=0, sticky=tk.W, pady=5)
left_text = tk.Text(frame, width=30, height=20)
left_text.grid(row=1, column=0, pady=5)

# 오른쪽 입력 박스 (DESC 스크립트 실행 결과)
right_label = ttk.Label(frame, text="DESC 스크립트 실행 결과:")
right_label.grid(row=0, column=1, sticky=tk.W, pady=5)
right_text = tk.Text(frame, width=50, height=20)
right_text.grid(row=1, column=1, pady=5)

# 처리 버튼
process_button = ttk.Button(frame, text="분석", command=process_input)
process_button.grid(row=2, column=0, columnspan=2, pady=10)

# 출력 박스
output_label = ttk.Label(frame, text="분석 결과:")
output_label.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
output_text = tk.Text(frame, width=100, height=30, wrap="none")
output_text.grid(row=4, column=0, columnspan=2, pady=5)

# 스크롤바 추가
output_scroll = ttk.Scrollbar(frame, orient="vertical", command=output_text.yview)
output_text.configure(yscrollcommand=output_scroll.set)
output_scroll.grid(row=4, column=2, sticky="ns")

# 창 크기 조절 가능하도록 설정
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.rowconfigure(4, weight=1)

root.mainloop()
