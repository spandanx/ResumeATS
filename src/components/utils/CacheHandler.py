import redis
from datetime import datetime, timedelta
import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Text, Integer, Boolean, UUID
import uuid
from sqlalchemy.orm import Session

# Base = declarative_base()
# class ChatSession(Base):
#     __tablename__ = "chat_session"
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     user_id = Column(String, nullable=False)
#     info = Column(String, nullable=True)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     is_active = Column(Boolean, default=True)

class CacheHandler:
    def __init__(self, redis_url, redis_port, db, password):
        self.redis_client = redis.Redis(host=redis_url, port=redis_port, db=db, password=password)

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

    cache_url = "103.180.212.180"
    cache_port = 6379
    # expiry_minutes = 2
    expiry_seconds = 30
    user_id = 112
    cache_db = 0
    cache_password = "tthP**a9Re"

    #
    #
    # config.read('config.properties')
    # cache_url = config['cache']['url']
    # cache_key = config['cache']['key']
    # cache_port = config['cache']['port']
    # cache_password = config['cache']['password']
    # cache_db = config['cache']['db']

    cacheHandler = CacheHandler(cache_url, cache_port, cache_db, cache_password)

    expire_time = timedelta(seconds=expiry_seconds)

    # redis_client = redis.from_url(redis_url)
    # redis_client = redis.Redis(host=redis_url, port=redis_port, db=0)
    # session_data = {"db_session_id": str(db_session.id)}

    # session_id = f"session:{user_id}:{datetime.utcnow().isoformat()}"
    session_id = "sample_key"

    data = {
        "user_id": user_id,
        "created_at": datetime.utcnow().isoformat(),
        "last_activity": datetime.utcnow().isoformat(),
        # "expire_time": expire_time
    }

    # response = cacheHandler.cache_data(key=session_id, data=data, expiry=expire_time)
    # print("Cached")
    # print(response)

    # redis_client.set(session_id, json.dumps(data))

    session_id = "sample_key"
    print(cacheHandler.get_from_cache(session_id))

    x = 1

