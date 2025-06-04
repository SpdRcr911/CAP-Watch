import os
import sqlite3
import csv

def csvs_to_sqlite(csv_folder, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for fname in os.listdir(csv_folder):
        if fname.lower().endswith('.csv'):
            table_name = os.path.splitext(fname)[0]
            with open(os.path.join(csv_folder, fname), newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader)
                columns = ', '.join([f'"{h}" TEXT' for h in headers])
                cursor.execute(f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns})')
                for row in reader:
                    placeholders = ', '.join(['?'] * len(row))
                    cursor.execute(f'INSERT INTO "{table_name}" VALUES ({placeholders})', row)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    csvs_to_sqlite(os.path.dirname(os.path.abspath(__file__)), 'capwatch.db')
    print('CSV files imported into capwatch.db')
