import logging

import redis
from datetime import datetime, timedelta
import json


class MemCache:
    def __init__(self, redis_url, redis_port, redis_db, redis_password):
        logging.info("redis_url, redis_port, redis_db")
        logging.info(redis_url)
        logging.info(redis_port)
        logging.info(redis_db)

        self.redis_client = redis.Redis(host=redis_url, port=redis_port, db=redis_db, password=redis_password)

    def cache_data(self, key, data, expiry):
        response = self.redis_client.setex(
            key,
            expiry,
            json.dumps(data)
        )
        return response

    def get_from_cache(self, key):
        logging.info("called get_from_cache()")
        value = self.redis_client.get(key)
        logging.info("value")
        logging.info(value)
        if value:
            return json.loads(value.decode('utf-8'))



if __name__ == "__main__":
    cache_url = "host"
    cache_port = 0
    # expiry_minutes = 2
    expiry_seconds = 10
    user_id = 1
    cache_db = 0
    cache_password = "ABC"

    redis_url = f"redis://default:{cache_password}@{cache_url}:6379/0"
    logging.info(redis_url)
    r_url = redis.Redis.from_url(
        url=redis_url,
        decode_responses=True  # Decodes responses to Python strings automatically
    )
    logging.info(f"Connected to Redis via URL: {r_url.ping()}")

    cacheHandler = MemCache(cache_url, cache_port, cache_db, cache_password)
    expire_time = timedelta(seconds=expiry_seconds)

    key = "sample_key"

    data = {
        "user_id": user_id,
        "created_at": datetime.utcnow().isoformat(),
        "last_activity": datetime.utcnow().isoformat(),
        # "expire_time": expire_time
    }

    cacheHandler.cache_data(key, data, expire_time)

    print(cacheHandler.get_from_cache(key))

    x = 1

