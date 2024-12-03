import sys
import re
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel


def process_bind_list_and_sql(bind_list, sql):
    # 바인드 값 추출 및 중복 제거
    bind_pattern = r":(\d+) = '(.*?)'"
    matches = re.findall(bind_pattern, bind_list)

    unique_binds = {}
    bind_map = {}
    new_bind_num = 1

    for num, value in matches:
        if value not in unique_binds:
            unique_binds[value] = str(new_bind_num)
            new_bind_num += 1
        bind_map[num] = unique_binds[value]

    # 바인드 리스트 업데이트 (중복 제거)
    updated_bind_list = []
    for value, num in unique_binds.items():
        updated_bind_list.append(f":{num} = '{value}'")

    # 업데이트된 바인드 리스트를 문자열로 변환
    updated_bind_list = "\n".join(updated_bind_list)

    # SQL 업데이트
    for old_num, new_num in bind_map.items():
        print("old_num : "+old_num)
        print("new_num : "+new_num)
        sql = re.sub(r':' + re.escape(old_num) + r'\b', ':' + new_num, sql)

    # 결과 조합
    return updated_bind_list + "\n\n" + sql


class BindProcessorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        input_layout = QHBoxLayout()

        # 바인드 리스트 입력
        bind_layout = QVBoxLayout()
        bind_layout.addWidget(QLabel('바인드 리스트:'))
        self.bind_input = QTextEdit()
        self.bind_input.setPlaceholderText("여기에 바인드 리스트를 붙여넣으세요...")
        bind_layout.addWidget(self.bind_input)
        input_layout.addLayout(bind_layout)

        # SQL 입력
        sql_layout = QVBoxLayout()
        sql_layout.addWidget(QLabel('SQL:'))
        self.sql_input = QTextEdit()
        self.sql_input.setPlaceholderText("여기에 SQL을 붙여넣으세요...")
        sql_layout.addWidget(self.sql_input)
        input_layout.addLayout(sql_layout)

        main_layout.addLayout(input_layout)

        self.process_button = QPushButton('처리')
        self.process_button.clicked.connect(self.process_text)
        main_layout.addWidget(self.process_button)

        self.output_label = QLabel('결과:')
        main_layout.addWidget(self.output_label)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        main_layout.addWidget(self.output_text)

        self.setLayout(main_layout)
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('바인드 처리기')
        self.show()

    def process_text(self):
        bind_list = self.bind_input.toPlainText()
        sql = self.sql_input.toPlainText()
        result = process_bind_list_and_sql(bind_list, sql)
        self.output_text.setText(result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BindProcessorApp()
    sys.exit(app.exec_())