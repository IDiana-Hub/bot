def Print(MENU, order):
    if order == None:
        return "Кошик порожній"
    else:
        text = ""
        cost = 0
        for key in order:
            try:
                int(order[key])
                if order[key] > 0:
                    text += MENU[key].print(order[key]) + f" /del{key}\n"
                    cost += MENU[key].GetPrice() * order[key]
            except:
                print()
        text += f"Вартість: {cost} грн\n"
        return text

def Close(MENU, user, order):
    text = f"{user['name']}\n{user['adress']}\n{user['fone']}\n"
    text += Print(MENU, order)
    text += order["coment"]
    return text