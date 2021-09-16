import redis
from celery import Celery
import scheduler.celeryconfig

import pickle

app = Celery('example')

app.config_from_object(scheduler.celeryconfig)


@app.task
def read(df_id):
    print("Reading df from Redis")
    r = redis.StrictRedis(host='redis', port=6379, db=0)
    pickle.loads(r.get(df_id))
