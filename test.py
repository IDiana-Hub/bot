import pymongo
import dbconect as db
import json
import pprint
pprint.pprint(db.collection.find_one({"adress":"vfvf"}))
