from scheduler.tasks import read

from meassure_wrapper import meassure


@meassure
def transfer(df):
    """
    Function that makes the transfer to the worker

    df is passed in the meassure wrapper
    """

    temp_file_path = '/tmp/temp.hdf5'
    df.export_parquet(to='s3://my-s3-bucket/my_data.parquet', fs_options={'access_key': my_key, 'secret_key': my_secret_key})
    task = read.delay(temp_file_path)
    task.wait()


if __name__ == "__main__":
    transfer()
