import snowflake.connector

# -----------------------
# Snowflake Connection
# -----------------------
conn = snowflake.connector.connect(
    user="------",
    password="------",
    account="------",
    warehouse="------",
    database="------",
    schema="------"
)

cursor = conn.cursor()

# -----------------------
# Test Query
# -----------------------
cursor.execute("SELECT * FROM resume_data")

for row in cursor.fetchall():
    print(row)

# -----------------------
# Close connection
# -----------------------
cursor.close()
conn.close()

print("✅ Snowflake connected successfully")
