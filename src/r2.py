import os
import io
import boto3
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

s3 = boto3.client(
    service_name ="s3",
    endpoint_url = os.environ.get("R2_BUCKET_URL"),
    aws_access_key_id = os.environ.get("R2_ACCESS_KEY_ID"),
    aws_secret_access_key = os.environ.get("R2_SECRET_ACCESS_KEY"),
    region_name="auto"
    )

s3.upload_fileobj(io.BytesIO(b"file_content"), os.environ.get("R2_BUCKET_NAME"), "test")

object_information = s3.head_object(Bucket=os.environ.get("R2_BUCKET_NAME"), Key="test")

print(object_information)