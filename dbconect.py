import pymongo
import os
import subprocess
conn_str = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
db = client["bot"]
collection = db["oders"]
collClient = db["client"]

# def start():
#     cmd = '"C:\Program Files\MongoDB\Server\5.0\bin\mongod.exe" - -dbpath = "c:\data\db"'
#     unknown_dir = subprocess.Popen(cmd)
#     print("cmd`ran with exit code %d" % unknown_dir)