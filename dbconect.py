import pymongo
import os
import subprocess
conn_str = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
db = client["bot"]
collOrder = db["order"]
collClient = db["client"]
collFOrder = db["Forder"]

# def start():
#     cmd = '"C:\Program Files\MongoDB\Server\5.0\bin\mongod.exe" - -dbpath = "c:\data\db"'
#     unknown_dir = subprocess.Popen(cmd)
#     print("cmd`ran with exit code %d" % unknown_dir)