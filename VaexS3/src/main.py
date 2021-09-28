import os

from dotenv import load_dotenv
from scheduler.tasks import read

from meassure_wrapper import meassure


CHUNK_SIZE_MB = 100


@meassure
def transfer(df, size):
    """
    Function that makes the transfer to the worker

    df is passed in the meassure wrapper
    """

    load_dotenv()

    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_REGION")
    bucket_id = os.getenv("AWS_S3_BUCKET_ID")

    # Chunks
    size_mb = size * 1024
    n_chunks = int((size_mb // CHUNK_SIZE_MB) + 1) \
        if (size_mb % CHUNK_SIZE_MB) != 0 else int(size_mb // CHUNK_SIZE_MB)
    chunk_size = int(df.count()) // n_chunks
    file_prefix = "sample"
    file_path = f"s3://{bucket_id}/{file_prefix}.parquet"

    df.export_many(
        file_path,
        chunk_size=chunk_size,
        fs_options={
            "access_key": access_key,
            "secret_key": secret_access_key,
            "region": region
        }
    )
    task = read.delay(file_prefix)
    task.wait()


if __name__ == "__main__":
    transfer()
