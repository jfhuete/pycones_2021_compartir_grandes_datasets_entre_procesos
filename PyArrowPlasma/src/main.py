import numpy as np
import pyarrow as pa
import pyarrow.plasma as plasma
import re


from scheduler.tasks import read

from meassure_wrapper import meassure


@meassure
def transfer(df):
    """
    Function that makes the transfer to the worker

    df is passed in the meassure wrapper
    """

    client = plasma.connect("/tmp/sock/plasma.sock")

    # Convert the Pandas DataFrame into a PyArrow RecordBatch
    record_batch = pa.RecordBatch.from_pandas(df)

    # Create the Plasma object from the PyArrow RecordBatch. Most of the work
    # here is done to determine the size of buffer to request from the object
    # store.
    object_id = plasma.ObjectID(np.random.bytes(20))
    mock_sink = pa.MockOutputStream()
    stream_writer = pa.RecordBatchStreamWriter(mock_sink, record_batch.schema)
    stream_writer.write_batch(record_batch)
    stream_writer.close()
    data_size = mock_sink.size()
    buf = client.create(object_id, data_size)

    # Write the PyArrow RecordBatch to Plasma
    stream = pa.FixedSizeBufferWriter(buf)
    stream_writer = pa.RecordBatchStreamWriter(stream, record_batch.schema)
    stream_writer.write_batch(record_batch)
    stream_writer.close()

    # Seal the Plasma object
    client.seal(object_id)

    object_id_str = re.search('ObjectID\((.*)\)', str(object_id))

    task = read.delay(object_id_str.group(1))
    task.wait()


if __name__ == "__main__":
    transfer()
