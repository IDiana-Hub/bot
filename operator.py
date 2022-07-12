import basket
from main import MENU
import dbconect as db

Order = db.collFOrder.find()
Client = db.collClient.find()
for order in Order:
    print(basket.Close(MENU, db.collClient.find_one({"UserID": order.get("UserID")}), order))


print("finih")