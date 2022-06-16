class Dish:

    def __init__(self, d):
        self.section=d.get('section')
        self.name=d.get('name')
        self.price=d.get('price')
        self.n=d.get('n')
    def GetSection(self):
        return self.section
    def GetName(self):
        return self.name
    def GetPrice(self):
        return self.price
    def GetN(self):
        return self.n

    def ifSection(self, a):
        return self.section == a
    def ToBasket(self):
        self.n+=1
    def OfBasket(self):
        self.n-=1