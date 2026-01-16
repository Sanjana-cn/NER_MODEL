# upload_s3_module.py
import boto3
import os

AWS_ACCESS_KEY = "------"
AWS_SECRET_KEY = "------"
AWS_REGION = "------"

S3_BUCKET_NAME = ------
S3_FOLDER = "mysql-exports/"
CSV_FOLDER = ------
CSV_FILE = "resume_data_latest.csv"  

def upload_csv_to_s3():
    csv_path = os.path.join(CSV_FOLDER, CSV_FILE)
    if not os.path.exists(csv_path):
        print("CSV file does not exist. Upload skipped.")
        return

    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )

    s3_key = S3_FOLDER + CSV_FILE

    print(f"Uploading {CSV_FILE} to S3...")
    s3.upload_file(csv_path, S3_BUCKET_NAME, s3_key)
    print(f"Uploaded to S3: s3://{S3_BUCKET_NAME}/{s3_key}")
