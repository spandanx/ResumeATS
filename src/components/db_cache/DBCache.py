from pymongo import MongoClient

class DBCache:
    def __init__(self, username, password, hostname, database, keyspace, port):
        self.database = self.get_database(username, password, hostname, database, keyspace, port)

    def get_database(self, username, password, hostname, database, keyspace, port):
        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        # CONNECTION_STRING = "mongodb+srv://user:pass@cluster.mongodb.net/myFirstDatabase"
        CONNECTION_STRING = f"mongodb://{username}:{password}@{hostname}:{port}"

        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        client = MongoClient(CONNECTION_STRING)

        # Create the database for our example (we will use the same database throughout the tutorial
        return client[database][keyspace]

    def get_record(self, key):
        item_details = self.database.find_one({"key": key})
        return item_details

    def insert_record(self, data):
        response = self.database.insert_one(data)
        return response



if __name__ == "__main__":
    username = "admin5443"
    password = "p0_L766Poi"
    hostname = "103.180.212.180"
    port = "27017"
    database = "ats_db"
    keyspace = "ats_cache"
    dbCache = DBCache(username, password, hostname, database, keyspace, port)
    # keySpace = dbCache.database["ats_cache"]
    key = "68b90a9f056bc19e78f6e8d7"
    # key = "68b90a9f056bc19e78f6e877uui"
    # response = keySpace.find({"key": id})
    # response = keySpace.find_one()
    # response = dbCache.database.find_one({"key": key})
    # response = dbCache.get_record(key=key)
    # print(response)
    data = {
        "key": "21b80a8f056bd19e78f6e8e5",
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