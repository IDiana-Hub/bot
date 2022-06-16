import pymongo
import datetime

# Replace the uri string with your MongoDB deployment's connection string.
conn_str = "mongodb://localhost:27017"

# set a 5-second connection timeout
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
db = client["test"]
colection = db["test"]

time = datetime.datetime.now()

object = {
    "time": time,
    "Name": "Dino",
    "message": "supper"
}
result = colection.insert_one(object)

try:
    print(result)
except Exception:
    print("Unable to connect to the server.")