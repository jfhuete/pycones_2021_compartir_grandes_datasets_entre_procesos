import os
import random

import sh

from scheduler.tasks import read
from meassure_wrapper import meassure


CHUNK_SIZE_MB = 100


@meassure
def transfer(df):
    """
    Function that makes the transfer to the worker

    df is passed in the meassure wrapper
    """

    bucket_id = "jfhuete-pycones2021"
    temp_path = "/tmp"
    file_path = f"{temp_path}/sample.hdf5"
    temp_files_prefix = str(random.getrandbits(32))

    # Export to hdf5
    df.export_hdf5(file_path)

    # Split hdf5 file in smaller files
    sh.split(
        f"-b{CHUNK_SIZE_MB}M",
        file_path,
        f"{temp_path}/{temp_files_prefix}"
    )

    # Upload files to S3
    temp_files = list(
        filter(lambda x: x.find(temp_files_prefix) == 0, os.listdir(temp_path))
    )
    processes = []
    for file in temp_files:
        processes.append(
            sh.aws(
                "s3api",
                "put-object",
                "--bucket",
                bucket_id,
                "--key",
                file,
                "--body",
                f"{temp_path}/{file}",
                _bg=True
            )
        )

    for process in processes:
        process.wait()

    task = read.delay(temp_files)
    task.wait()


if __name__ == "__main__":
    transfer()
