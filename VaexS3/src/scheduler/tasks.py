import os

import sh

from celery import Celery
from dotenv import load_dotenv

import scheduler.celeryconfig

import vaex

app = Celery('example')

app.config_from_object(scheduler.celeryconfig)


@app.task
def read(temp_files):

    load_dotenv()

    bucket_id = os.getenv("AWS_S3_BUCKET_ID")
    received_temp_path = "../tmp/received"

    rebuilt_temp_file = "sample_received.hdf5"
    rebuilt_temp_file_path = f"{received_temp_path}/{rebuilt_temp_file}"

    # Get splited files from s3

    processes = []
    for file in temp_files:
        processes.append(
            sh.aws(
                "s3api",
                "get-object",
                "--bucket",
                bucket_id,
                "--key",
                file,
                f"{received_temp_path}/{file}",
                _bg=True)
            )

    for process in processes:
        process.wait()

    temp_files_path = [f"{received_temp_path}/{f}" for f in temp_files]
    sh.cat(*temp_files_path, _out=f"{received_temp_path}/{rebuilt_temp_file}")

    df = vaex.open(rebuilt_temp_file_path)
