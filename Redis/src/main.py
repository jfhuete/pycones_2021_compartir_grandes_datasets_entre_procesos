import pickle

import redis
from scheduler.tasks import read

from meassure_wrapper import meassure


@meassure
def transfer(df):
    """
    Function that makes the transfer to the worker

    df is passed in the meassure wrapper
    """

    r = redis.StrictRedis(host='redis', port=6379, db=0)
    r.set('df', pickle.dumps(df))
    task = read.delay('df')
    task.wait()


if __name__ == "__main__":
    transfer()
