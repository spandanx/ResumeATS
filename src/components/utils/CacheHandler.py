import redis
from datetime import datetime, timedelta
import json
from src.components.memory_cache.MemCache import MemCache
from src.components.db_cache.DBCache import DBCache

# from components.memory_cache.MemCache import MemCache
# from components.db_cache.DBCache import DBCache

class CacheHandler:
    def __init__(self, redis_url, redis_port, redis_db, redis_password,
                 db_username, db_password, db_hostname, db_database, db_keyspace, db_port):
        self.mem_cache = MemCache(redis_url=redis_url, redis_port=redis_port, redis_db=redis_db, redis_password=redis_password)
        self.db_cache = DBCache(username=db_username, password=db_password, hostname=db_hostname,
                                database=db_database, keyspace=db_keyspace, port=db_port)

    def cache_data(self, key, data, expiry, username):
        insert_data = {
            "key": key,
            "data": data,
            "username": username
        }
        db_insery_response = self.db_cache.insert_record(insert_data)
        response = self.mem_cache.cache_data(key, data, expiry)
        return response

    def get_from_cache(self, key, username, expiry):
        cached_data = self.mem_cache.get_from_cache(key)
        if cached_data is None:
            db_response = self.db_cache.get_record(key)
            if db_response is not None:
                cached_db_data = db_response["data"]

                # Insert to the cache
                db_insery_response = self.mem_cache.cache_data(key, cached_db_data, expiry)
                return cached_db_data
        return cached_data



if __name__ == "__main__":

    cache_url = ""
    cache_port = 6379
    # expiry_minutes = 2
    expiry_seconds = 30
    user_id = 112
    cache_db = 0
    cache_password = ""

    cacheHandler = CacheHandler(cache_url, cache_port, cache_db, cache_password)

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

