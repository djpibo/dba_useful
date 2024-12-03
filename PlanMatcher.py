import sys
import re
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel

def count_indentation(text):
    lines = text.split('\n')
    result = []
    operation_index = None
    indentations = []

    # First pass: collect all indentation levels
    for line in lines[2:]:  # Skip header and separator
        if '|' in line:
            columns = line.split('|')
            if len(columns) > 2:
                operation = columns[2]  # Assuming Operation is the 3rd column
                indentation = len(operation) - len(operation.lstrip())
                indentations.append(indentation)

    max_depth = max(indentations) if indentations else 0
    depth_map = {depth: max_depth - depth + 1 for depth in set(indentations)}

    # Find the index of the 'Operation' column and add 'Order' column
    for i, line in enumerate(lines):
        if 'Operation' in line:
            headers = line.split('|')
            operation_index = [i for i, header in enumerate(headers) if 'Operation' in header][0]
            headers.insert(operation_index, ' Order ')
            result.append('|'.join(headers))
            # Add separator line for the new column
            separator = lines[i+1].split('|')
            separator.insert(operation_index, '-' * 7)  # 7 dashes for 'Order' column
            result.append('|'.join(separator))
            break

    if operation_index is None:
        return "Operation column not found."

    # Process each line
    for line in lines[i+2:]:  # Skip the header and separator lines
        if '|' not in line:  # Skip lines without pipe separators
            result.append(line)
            continue

        columns = line.split('|')
        if len(columns) <= operation_index:
            result.append(line)
            continue

        operation = columns[operation_index]
        indentation = len(operation) - len(operation.lstrip())
        order = depth_map[indentation]
        # Insert order as a new column
        columns.insert(operation_index, f' {order:5d} ')
        result.append('|'.join(columns))

    return '\n'.join(result)

class IndentationCounterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("여기에 실행 계획을 붙여넣으세요...")
        layout.addWidget(self.input_text)

        self.process_button = QPushButton('들여쓰기 계산')
        self.process_button.clicked.connect(self.process_text)
        layout.addWidget(self.process_button)

        self.output_label = QLabel('결과:')
        layout.addWidget(self.output_label)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

        self.setLayout(layout)
        self.setGeometry(300, 300, 1000, 600)
        self.setWindowTitle('실행 계획 들여쓰기 계산기')
        self.show()

    def process_text(self):
        text = self.input_text.toPlainText()
        result = count_indentation(text)
        self.output_text.setText(result)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = IndentationCounterApp()
    sys.exit(app.exec_())