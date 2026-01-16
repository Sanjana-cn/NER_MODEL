# Automated Resume Processing System using NER and Data Analytics

## Abstract
Manual resume screening is time-consuming and inefficient for recruiters.
This project automates resume processing using Named Entity Recognition (NER)
to extract candidate information and build an analytics-ready data pipeline.

---

## Architecture
The system follows a layered pipeline architecture:

- Presentation Layer: Streamlit UI
- Processing Layer: NER Model
- Storage Layer: MySQL, AWS S3, Snowflake
- Analytics Layer: Power BI

---

## Tech Stack
- Python
- Streamlit
- MySQL
- AWS S3
- Snowflake
- Power BI

---

## Data Pipeline / Workflow
1. User uploads resumes via Streamlit UI
2. Resume text is extracted and preprocessed
3. NER model extracts entities:
   - Name
   - Email
   - Phone
   - College
   - CGPA
4. Structured data stored in MySQL
5. Raw and processed files stored in AWS S3
6. Data ingested into Snowflake using Snowpipe
7. Power BI dashboard visualizes insights

---

## Setup Instructions
1. Clone the repository
2. Install dependencies:
# NER_MODEL
