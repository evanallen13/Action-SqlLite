import os
import sqlite3

def create_tables_from_db_files():
    path = "data"
    dir_list = os.listdir(path)

    for file in dir_list:
        if file.endswith(".db"):
            db_path = os.path.join(path, file)
            print(db_path)

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            tables = cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
            ).fetchall()

            for (table_name,) in tables:
                print(f"Table: {table_name}")
                rows = cursor.execute(f"SELECT * FROM {table_name};").fetchall()
                for row in rows:
                    print(row)

            conn.close()

create_tables_from_db_files()



