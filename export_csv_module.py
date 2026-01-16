# export_csv_module.py
import pymysql
import csv
import os

# -------------------------
# MySQL Config
# -------------------------
MYSQL_HOST = "------"
MYSQL_USER = "------"
MYSQL_PASSWORD = "------"
MYSQL_DB = "------"
MYSQL_PORT = 3306

EXPORT_DIR = "------"
EXPORT_FILE = "------"  # single file always

os.makedirs(EXPORT_DIR, exist_ok=True)
csv_path = os.path.join(EXPORT_DIR, EXPORT_FILE)

def export_mysql_to_csv():
    conn = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        port=MYSQL_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM resume_data")
    rows = cursor.fetchall()

    if not rows:
        print("⚠️ No data found in resume_data table. CSV not created.")
        cursor.close()
        conn.close()
        return

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    cursor.close()
    conn.close()
    print(f"✅ CSV CREATED/UPDATED AT: {csv_path}")
