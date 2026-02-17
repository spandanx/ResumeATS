from pymongo import MongoClient

class DBCache:
    def __init__(self, username, password, hostname, database, keyspace, port):
        self.database = self.get_database(username, password, hostname, database, keyspace, port)

    def get_database(self, username, password, hostname, database, keyspace, port):

        CONNECTION_STRING = f"mongodb://{username}:{password}@{hostname}:{port}"

        client = MongoClient(CONNECTION_STRING)

        return client[database][keyspace]

    def get_record(self, key):
        item_details = self.database.find_one({"key": key})
        return item_details

    def insert_record(self, data):
        response = self.database.insert_one(data)
        return response



if __name__ == "__main__":
    username = "ABC"
    password = "ABC"
    hostname = "host"
    port = "100"
    database = "ats_db"
    keyspace = "ats_cache"
    dbCache = DBCache(username, password, hostname, database, keyspace, port)
    # keySpace = dbCache.database["ats_cache"]
    key = "ABC"
    # response = keySpace.find({"key": id})
    # response = keySpace.find_one()
    # response = dbCache.database.find_one({"key": key})
    # response = dbCache.get_record(key=key)
    # print(response)
    data = {
        "key": "ABC",
        "item_name": "Apple",
        "quantity": 3,
        "ingredients": "Fruit"
    }
    # insert_response = dbCache.insert_record(data)
    # print(insert_response)
    response = dbCache.database.find({"key": key})
    for item in response:
        print(item)

    # response = dbCache.get_record(id)
    # print(response)
    x = 1