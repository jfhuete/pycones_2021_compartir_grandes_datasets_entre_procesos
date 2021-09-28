import os
from celery import Celery
from dotenv import load_dotenv

import scheduler.celeryconfig

import vaex

app = Celery('example')

app.config_from_object(scheduler.celeryconfig)


@app.task
def read(file_prefix):

    load_dotenv()

    bucket_id = os.getenv("AWS_S3_BUCKET_ID")

    print("Reading df using Vaex s3")

    df = vaex.open(f"s3://{bucket_id}/{file_prefix}-**.parquet")
