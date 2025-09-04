import redis
from datetime import datetime, timedelta
import json


class MemCache:
    def __init__(self, redis_url, redis_port, redis_db, redis_password):
        self.redis_client = redis.Redis(host=redis_url, port=redis_port, db=redis_db, password=redis_password)

    def cache_data(self, key, data, expiry):
        response = self.redis_client.setex(
            key,
            expiry,
            json.dumps(data)
        )
        return response

    def get_from_cache(self, key):
        value = self.redis_client.get(key)
        # print(value)
        if value:
            return json.loads(value.decode('utf-8'))



if __name__ == "__main__":
    cache_url = ""
    cache_port = 6379
    # expiry_minutes = 2
    expiry_seconds = 30
    user_id = 112
    cache_db = 0
    cache_password = ""

    cacheHandler = MemCache(cache_url, cache_port, cache_db, cache_password)
    expire_time = timedelta(seconds=expiry_seconds)

    session_id = "sample_key"

    data = {
        "user_id": user_id,
        "created_at": datetime.utcnow().isoformat(),
        "last_activity": datetime.utcnow().isoformat(),
        # "expire_time": expire_time
    }

    session_id = "sample_key"
    print(cacheHandler.get_from_cache(session_id))

    x = 1

