from aiogram import types


def Start():
    keyboard = types.ReplyKeyboardMarkup()
    button1 = types.KeyboardButton(text="Меню")
    keyboard.add(button1)
    button2 = types.KeyboardButton(text="Переглянути кошик")
    keyboard.add(button2)
    return keyboard


def Menu():
    keyboard = types.ReplyKeyboardMarkup()
    button1 = types.KeyboardButton(text="Піца")
    keyboard.add(button1)
    button2 = types.KeyboardButton(text="Чай")
    keyboard.add(button2)
    return keyboard


# def Back():
#     keyboard = types.ReplyKeyboardMarkup()
#     button1 = types.KeyboardButton(text="Меню")
#     keyboard.add(button1)
#     button2 = types.KeyboardButton(text="Переглянути кошик")
#     keyboard.add(button2)
#     return keyboard

def Basket():
    keyboard = types.ReplyKeyboardMarkup()
    button1 = types.KeyboardButton(text="Меню")
    keyboard.add(button1)
    button2 = types.KeyboardButton(text="Оформити замовлення")
    keyboard.add(button2)
    button3 = types.KeyboardButton(text="Переглянути кошик")
    keyboard.add(button3)
    button4 = types.KeyboardButton(text="Очистити кошик")
    keyboard.add(button4)
    return keyboard


def menu(MENU, section):
    keyboard = types.InlineKeyboardMarkup()
    for key in MENU:
        if MENU[key].ifSection(section):
            name = MENU[key].GetName()
            keyboard.add(types.InlineKeyboardButton(text=name, callback_data=f"addOder_{MENU[key].GetId()}"), )
    return keyboard


def Corect():
    keyboard = types.ReplyKeyboardMarkup()
    Button1 = types.KeyboardButton(text='Так, все правильно')
    Button2 = types.KeyboardButton(text='Змінити замовлення')
    Button3 = types.KeyboardButton(text='Змінити мої дані')
    keyboard.add(Button1)
    keyboard.add(Button2)
    keyboard.add(Button3)
    return keyboard
