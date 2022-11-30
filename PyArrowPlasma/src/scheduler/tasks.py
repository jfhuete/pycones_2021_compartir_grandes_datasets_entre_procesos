from celery import Celery
import scheduler.celeryconfig

import pyarrow as pa
import pyarrow.plasma as plasma

app = Celery('example')

app.config_from_object(scheduler.celeryconfig)


@app.task
def read(object_id_str):
    print("Reading df from Plasma")

    client = plasma.connect("/tmp/sock/plasma.sock")

    # Fetch the Plasma object
    object_id = plasma.ObjectID(bytes.fromhex(object_id_str))
    [data] = client.get_buffers([object_id])  # Get PlasmaBuffer from ObjectID
    buffer = pa.BufferReader(data)

    # Convert object back into an Arrow RecordBatch
    reader = pa.RecordBatchStreamReader(buffer)
    record_batch = reader.read_next_batch()

    record_batch.to_pandas()
