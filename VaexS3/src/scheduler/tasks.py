import sh

from celery import Celery

import scheduler.celeryconfig

import vaex

app = Celery('example')

app.config_from_object(scheduler.celeryconfig)


@app.task
def read(temp_files):

    bucket_id = "jfhuete-pycones2021"
    received_temp_path = "/tmp/received"

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

    import time
    time.sleep(2)

    temp_files_path = [f"{received_temp_path}/{f}" for f in temp_files]
    sh.cat(*temp_files_path, _out=f"{rebuilt_temp_file_path}")

    df = vaex.open(rebuilt_temp_file_path)
