from flask import Flask, flash
import boto3, botocore
from config import S3_KEY, S3_SECRET, S3_BUCKET, S3_LOCATION


s3 = boto3.client(
   "s3",
   aws_access_key_id=S3_KEY,
   aws_secret_access_key=S3_SECRET
)


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file_to_s3(file, bucket_name, acl="public-read"):
    
    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        flash(f"Something Happened: ", e)
        return e

    print ("File uploaded")
    # return "{}{}".format(app.config["S3_LOCATION"], file.filename) | app.config doesn't contain S3_LOCATION
    return "{}{}".format(S3_LOCATION , file.filename)
