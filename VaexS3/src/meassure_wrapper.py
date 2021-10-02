from pathlib import Path
import os
import time
import traceback

import vaex


def meassure(func):
    """
    Decorator to wrap the function to measure and report the results
    """

    def wrapper():

        file_size = os.environ.get("FILE_SIZE", "m")
        file_path = f"/data/{file_size}.csv"

        print("Reading dataset")
        df = vaex.from_csv(
            file_path, convert=True, chunk_size=5_000_000, copy_index=False)
        size = round(Path(file_path).stat().st_size / 1024 / 1024 / 1024, 3)
        print("Transferring")
        startTime = time.time()

        try:
            func(df)
        except Exception:
            print(traceback.format_exc())
            print(f"====> Transfer failed for the file whose size is {size}Gb")
        else:
            endTime = time.time()

            print(f"====> Transfered {size}Gb in"
                  f"{round(endTime - startTime, 3)} seconds")

    return wrapper
