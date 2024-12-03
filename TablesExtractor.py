import sys
import re
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
from collections import Counter


def extract_tb_tables(sql):
    pattern = r'\b(TB_\w+|TS_\w+)'
    tables = re.findall(pattern, sql)
    table_counts = Counter(tables)
    result = []
    for table, count in sorted(table_counts.items(), key=lambda x: (-x[1], x[0])):
        result.append(f"{count}: {table}")

    # 테이블 추출후 리스트에 저장
    unique_tables = ["'{}'".format(table) for table in table_counts.keys()]

    # IN 절 구문 추가
    in_clause = "\n\nSELECT * FROM DBA_SEGMENTS WHERE SEGMENT_NAME IN ({})".format(", ".join(unique_tables))
    return '\n'.join(result) + in_clause


class TableExtractorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("여기에 SQL을 붙여넣으세요...")
        layout.addWidget(self.input_text)

        self.process_button = QPushButton('추출')
        self.process_button.clicked.connect(self.process_text)
        layout.addWidget(self.process_button)

        self.output_label = QLabel('결과:')
        layout.addWidget(self.output_label)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

        self.setLayout(layout)
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('테이블 추출하기')
        self.show()

    def process_text(self):
        sql = self.input_text.toPlainText()
        result = extract_tb_tables(sql)
        self.output_text.setText(result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TableExtractorApp()
    sys.exit(app.exec_())