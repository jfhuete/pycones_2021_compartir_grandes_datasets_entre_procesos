from celery import Celery
import scheduler.celeryconfig

import vaex

app = Celery('example')

app.config_from_object(scheduler.celeryconfig)


@app.task
def read(temp_file_path):
    print("Reading df using Vaex hdf5")
    df = vaex.open(temp_file_path)
