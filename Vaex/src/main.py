from scheduler.tasks import read

from meassure_wrapper import meassure


@meassure
def transfer(df):
    """
    Function that makes the transfer to the worker

    df is passed in the meassure wrapper
    """

    temp_file_path = '/tmp/temp.hdf5'
    df.export_hdf5(temp_file_path)
    task = read.delay(temp_file_path)
    task.wait()


if __name__ == "__main__":
    transfer()
