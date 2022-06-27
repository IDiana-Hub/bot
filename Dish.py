class Dish:

    def __init__(self, d, ):
        self.id = d.get("id")
        self.section = d.get('section')
        self.name = d.get('name')
        self.price = d.get('price')

    def GetSection(self):
        return self.section

    def GetName(self):
        return self.name

    def GetPrice(self):
        return self.price

    def GetId(self):
        return self.id

    def ifSection(self, a):
        return self.section == a

    def print(self, n):
        return f"{self.name} *{n}шт.    {self.price}грн"
