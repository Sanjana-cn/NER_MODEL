import pymysql

print("🚀 Script started")
print("✅ pymysql imported")

conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="root123",     
    database="resume_ner", 
    port=3306,
    connect_timeout=5,
    cursorclass=pymysql.cursors.DictCursor
)

print("✅ MySQL connected successfully")

conn.close()
print("🔒 Connection closed")
