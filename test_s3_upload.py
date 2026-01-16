import boto3

s3 = boto3.client("s3")

local_file = "data/exports/resume_data_20251230_074948.csv"
bucket = "resume-ner-bucket"
key = "------"

print("Uploading test file...")

s3.upload_file(local_file, bucket, key)

print("Upload finished")

