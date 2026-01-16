# =========================
# app.py
# Resume NER → MySQL → CSV → S3 (MULTI FILE)
# =========================

import streamlit as st
import spacy
import re
import pdfplumber
import docx
import pymysql
from export_csv_module import export_mysql_to_csv
from upload_s3_module import upload_csv_to_s3
import snowflake.connector


# -------------------------
# MySQL Config
# -------------------------
MYSQL_HOST = "127.0.0.1"
MYSQL_USER = "root"
MYSQL_PASSWORD = "root123"
MYSQL_DB = "resume_ner"
MYSQL_PORT = 3306

# -------------------------
# Snowflake Config
# -------------------------
SNOWFLAKE_USER = "-------"
SNOWFLAKE_PASSWORD = "------"
SNOWFLAKE_ACCOUNT = "------"
SNOWFLAKE_WAREHOUSE = "------"
SNOWFLAKE_DATABASE = "------"
SNOWFLAKE_SCHEMA = "------"


# -------------------------
# Load spaCy model
# -------------------------
nlp = spacy.load("en_core_web_sm")

st.set_page_config(page_title="Resume NER Pipeline", layout="centered")
st.title("Resume NER System (Multiple Upload)")

# -------------------------
# File uploader (MULTIPLE)
# -------------------------
uploaded_files = st.file_uploader(
    "Upload Resumes (TXT / PDF / DOCX)",
    type=["txt", "pdf", "docx"],
    accept_multiple_files=True
)

# -------------------------
# File readers
# -------------------------
def read_txt(file):
    return file.read().decode("utf-8", errors="ignore")

def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return text

def read_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# -------------------------
# Regex extractors
# -------------------------
def extract_email(text):
    match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    return match.group() if match else ""

def extract_phone(text):
    match = re.search(r"\b\d{10}\b", text)
    return match.group() if match else ""

def extract_cgpa(text):
    match = re.search(r"\b\d\.\d{1,2}\b", text)
    return match.group() if match else ""

# -------------------------
# NER Logic
# -------------------------
def extract_entities(text):
    doc = nlp(text)
    name = ""
    profile = ""

    for ent in doc.ents:
        if ent.label_ == "PERSON" and not name:
            name = ent.text
        elif ent.label_ in ["ORG", "GPE"] and not college:
            college = ent.text

    return {
        "name": name,
        "email": extract_email(text),
        "phone": extract_phone(text),
        "cgpa": extract_cgpa(text),
        "profile": profile
    }

# -------------------------
# MySQL Insert Logic
# -------------------------
def insert_into_mysql(data):
    conn = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        port=MYSQL_PORT
    )

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resume_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            phone VARCHAR(20),
            cgpa VARCHAR(10),
            profile VARCHAR(200),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        INSERT INTO resume_data (name, email, phone, cgpa, college)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data.get("name", ""),
        data.get("email", ""),
        data.get("phone", ""),
        data.get("cgpa", ""),
        data.get("profile", "")
    ))

    conn.commit()
    cursor.close()
    conn.close()

    
def insert_into_snowflake(data):
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resume_data (
            id INTEGER AUTOINCREMENT,
            name STRING,
            email STRING,
            phone STRING,
            cgpa STRING,
            profile STRING,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        INSERT INTO resume_data (name, email, phone, cgpa, college)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data.get("name", ""),
        data.get("email", ""),
        data.get("phone", ""),
        data.get("cgpa", ""),
        data.get("profile", "")
    ))

    conn.commit()
    cursor.close()
    conn.close()


# -------------------------
# MAIN PIPELINE
# -------------------------
if uploaded_files and len(uploaded_files) > 0:

    st.info(f" {len(uploaded_files)} resume(s) uploaded")

    if st.button("Extract & Save ALL → MySQL → CSV → S3", key="multi_pipeline_btn"):

        progress = st.progress(0)
        total_files = len(uploaded_files)

        for index, uploaded_file in enumerate(uploaded_files, start=1):

            file_type = uploaded_file.name.split(".")[-1].lower()

            if file_type == "txt":
                resume_text = read_txt(uploaded_file)
            elif file_type == "pdf":
                resume_text = read_pdf(uploaded_file)
            else:
                resume_text = read_docx(uploaded_file)

            entities = extract_entities(resume_text)

            insert_into_mysql(entities)
            insert_into_snowflake(entities)


            st.write(f" Processed: **{uploaded_file.name}**")
            st.json(entities)

            progress.progress(index / total_files)

        # Export FULL MySQL table to CSV
        export_mysql_to_csv()

        # Upload CSV to S3 (overwrite / updated file)
        upload_csv_to_s3()

        st.success("All resumes processed & uploaded to S3 successfully!")
