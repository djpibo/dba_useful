import re
import pymysql
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

def extract_schema_table_column_details(sql_script):
    schema_table_columns = []

    # Valid Oracle data types
    valid_data_types = {
        "CHAR", "VARCHAR", "VARCHAR2", "NUMBER", "DATE", "TIMESTAMP", "CLOB", "BLOB", "RAW", "LONG"
    }

    # Regular expression to match CREATE TABLE statements and extract schema, table, and column definitions
    table_pattern = re.compile(r"CREATE TABLE\s+(\w+)\.(\w+)\s*\((.*?)\);", re.DOTALL)
    column_pattern = re.compile(r"(\w+)\s+(\w+)(\((\d+)(?:,\s*(\d+))?|\s*BYTE)?\)?(?:\s+DEFAULT\s+\S+)?(?:\s+NOT NULL)?", re.DOTALL)

    for match in table_pattern.finditer(sql_script):
        schema_name = match.group(1)
        table_name = match.group(2)
        columns_section = match.group(3)

        # Extract columns
        for column_match in column_pattern.finditer(columns_section):
            column_name = column_match.group(1).upper()  # Convert column name to uppercase
            data_type = column_match.group(2).upper()
            if column_match.group(5):  # Check for scale (e.g., NUMBER(10,1))
                data_length = f"{column_match.group(4)},{column_match.group(5)}"
            else:
                data_length = column_match.group(4) if column_match.group(4) else ""

            if data_type in valid_data_types:  # Include only valid Oracle data types
                schema_table_columns.append({
                    "Schema": schema_name,
                    "Table": table_name,
                    "Column": column_name,
                    "Data Type": data_type,
                    "Data Length": data_length,
                })

    return schema_table_columns

def save_to_file(data):
    root = tk.Tk()
    root.withdraw()
    output_file = filedialog.asksaveasfilename(
        initialfile="offline_meta_info_result.csv",
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")]
    )
    if output_file:
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False, encoding='utf-8')
        messagebox.showinfo("Success", f"Data saved to {output_file}")

def insert_into_mysql(data):
    try:
        connection = pymysql.connect(
            host="localhost",
            user="meta",
            password="1234",
            database="meta_db"
        )
        cursor = connection.cursor()

        insert_query = "INSERT INTO meta_orcl_info (schema_Name, table_name, column_name, data_type_value, data_length_value) VALUES (%s, %s, %s, %s, %s)"

        # Bulk insert instead of single-row insert
        rows = [(row['Schema'], row['Table'], row['Column'], row['Data Type'], row['Data Length']) for row in data]
        cursor.executemany(insert_query, rows)

        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Success", "Data successfully inserted into MySQL database.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def main():
    root = tk.Tk()
    root.withdraw()
    input_file = filedialog.askopenfilename(filetypes=[("SQL Files", "*.sql")])
    if not input_file:
        messagebox.showerror("Error", "No file selected.")
        return

    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        data = extract_schema_table_column_details(sql_script)

        save_to_file(data)
        insert_into_mysql(data)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    main()
