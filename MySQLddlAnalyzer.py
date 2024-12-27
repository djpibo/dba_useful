import re
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pymysql

def parse_table_script(script):
    # 테이블별로 스키마와 컬럼 정보를 저장
    table_blocks = re.split(r'-- -----------------------------------------------------', script)

    data = []

    for block in table_blocks:
        # 테이블명 추출 (스키마와 테이블 분리)
        table_name_match = re.search(r'CREATE TABLE IF NOT EXISTS `(.*?)`\.`(.*?)`', block)
        if not table_name_match:
            continue  # 테이블 정보가 없는 블록은 건너뜀

        schema_name = table_name_match.group(1)
        table_name = table_name_match.group(2)

        # 컬럼 정보 추출
        column_pattern = re.compile(r'`(\w+)`\s+(\w+(?:\(\d+(?:,\d+)?\))?)\s+(?:CHARACTER SET.*?\s+)?(?:NULL|NOT NULL)?(?:\s+DEFAULT\s+\w+)?(?:\s+COMMENT\s+\'.*?\')?')
        columns = column_pattern.findall(block)

        for column_name, data_type in columns:
            # 데이터 타입과 길이 분리
            type_match = re.match(r'(\w+)\((\d+(?:,\d+)?)\)', data_type)
            if type_match:
                dtype = type_match.group(1)
                length = type_match.group(2)
            else:
                dtype = data_type
                length = ""

            data.append({
                "스키마명": schema_name,
                "테이블명": table_name,
                "컬럼명": column_name,
                "데이터타입": dtype,
                "데이터길이": length
            })

    # 데이터프레임 생성
    df = pd.DataFrame(data)
    return df

def select_file():
    """파일 선택 대화상자를 띄웁니다."""
    root = tk.Tk()
    root.withdraw()  # Tkinter 창 숨기기
    file_path = filedialog.askopenfilename(title="Select SQL File", filetypes=[("SQL Files", "*.sql")])
    return file_path

def save_file(df):
    """결과를 저장할 파일을 선택합니다."""
    root = tk.Tk()
    root.withdraw()  # Tkinter 창 숨기기
    output_path = filedialog.asksaveasfilename(title="Save CSV File", defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if output_path:
        df.to_csv(output_path, index=False, encoding='utf-8')
        messagebox.showinfo("완료", f"결과가 {output_path}에 저장되었습니다.")

def insert_into_mysql(df, host, user, password, database, table):
    # MySQL 연결
    connection = pymysql.connect(
        host='localhost',
        user='meta',
        password='1234',
        database='meta_db'
    )
    cursor = connection.cursor()

    # 테이블 생성 (없을 경우)
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS meta_gopl_info (
        `schema_name` VARCHAR(255),
        `table_name` VARCHAR(255),
        `column_name` VARCHAR(255),
        `data_type_value` VARCHAR(255),
        `data_length_value` VARCHAR(50)
    );
    """
    cursor.execute(create_table_query)

    # 데이터 삽입
    insert_query = f"""
    INSERT INTO meta_gopl_info (`schema_name`, `table_name`, `column_name`, `data_type_value`, `data_length_value`)
    VALUES (%s, %s, %s, %s, %s);
    """
    for _, row in df.iterrows():
        cursor.execute(insert_query, (
            row["스키마명"],
            row["테이블명"],
            row["컬럼명"],
            row["데이터타입"],
            row["데이터길이"]
        ))

    # 변경사항 커밋
    connection.commit()

    # 연결 종료
    cursor.close()
    connection.close()
    print(f"{len(df)}개의 행이 삽입되었습니다.")

if __name__ == "__main__":
    # 파일 선택
    input_file = select_file()
    if not input_file:
        print("파일이 선택되지 않았습니다.")
    else:
        with open(input_file, 'r', encoding='utf-8') as file:
            sql_script = file.read()

        # SQL 스크립트 파싱
        result_df = parse_table_script(sql_script)

        # 결과를 파일로 저장
        save_file(result_df)

        # MySQL 데이터베이스에 삽입
        insert_into_mysql(
            result_df,
            host="localhost",
            user="your_username",
            password="your_password",
            database="your_database",
            table="parsed_table_data"
        )
