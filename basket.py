def print(MENU):
    text = ""
    cost = 0
    for i in range(len(MENU)):
        if MENU[i].GetN()>0:
            text += f"{MENU[i].GetName()} x{MENU[i].GetN()}  {MENU[i].GetPrice()}грн  /del{i}\n"
            cost += MENU[i].GetPrice() * MENU[i].GetN()
    text += f"Вартість: {cost} грн"
    return text

def print(MENU, oder):
    text = f"{oder['adres']}\n {oder['fone']}\n"
    cost = 0
    for i in range(len(MENU)):
        if MENU[i].GetN() > 0:
            text += f"{MENU[i].GetName()} x{MENU[i].GetN()}  {MENU[i].GetPrice()}грн\n"
            cost += MENU[i].GetPrice() * MENU[i].GetN()
    text += f"Вартість: {cost} грн"
    return text

def close(MENU):
    cBasket = []
    for i in range(len(MENU)):
        if MENU[i].GetN() > 0:
            cBasket.append(MENU[i].print())
    return cBasket