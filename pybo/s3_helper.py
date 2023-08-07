import boto3
from botocore.exceptions import NoCredentialsError
from flask import current_app


def save_to_s3(file, bucket_name):
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=current_app.config['AWS_ACCESS_KEY'],
            aws_secret_access_key=current_app.config['AWS_SECRET_KEY'],
            region_name=current_app.config['AWS_REGION']
        )
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": file.content_type
            }
        )
        return file.filename
    except NoCredentialsError:
        return None
