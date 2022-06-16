import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import pymongo
from Dish import Dish
#for aiogram.contrib.fsm_storage.mongo import MongoStorage
# from WMArchive.Storage.MongoIO import MongoStorage
# from WMArchive.Storage.HdfsIO import HdfsStorage
# from apscheduler.schedulers.asyncio import AsyncIOScheduler

class OrderFood(StatesGroup):
    waiting_for_adress = State()
    waiting_for_fone_namber = State()

with open("menu.json", "r", encoding='utf-8') as read_file:
    init = json.load(read_file)
    read_file.close()
MENU = [Dish(dish) for dish in init["menu"]]

# Объект бота
bot = Bot(token=init["token"])
#Диспетчер для бота
conn_str = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
db = client["bot"]
collection = db["Dispatcher"]
dp = Dispatcher(bot, storage = collection)
#dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
#logging.basicConfig(level=logging.INFO)

def printBasket():
    text = ""
    cost = 0
    for i in range(len(MENU)):
        if MENU[i].GetN()>0:
            text += f"{MENU[i].GetName()} x{MENU[i].GetN()}  {MENU[i].GetPrice()}грн  /del{i}\n"
            cost += MENU[i].GetPrice() * MENU[i].GetN()
    text += f"Вартість: {cost} грн"
    return text

def keyboardStart():
    keyboard = types.ReplyKeyboardMarkup()
    button1 = types.KeyboardButton(text="Меню")
    keyboard.add(button1)
    button2 = types.KeyboardButton(text="Переглянути кошик")
    keyboard.add(button2)
    return keyboard
def keyboardMenu():
    keyboard = types.ReplyKeyboardMarkup()
    button1 = types.KeyboardButton(text="Піца")
    keyboard.add(button1)
    button2 = types.KeyboardButton(text="Чай")
    keyboard.add(button2)
    return keyboard
def keyboardBack():
    keyboard = types.ReplyKeyboardMarkup()
    button1 = types.KeyboardButton(text="Меню")
    keyboard.add(button1)
    button2 = types.KeyboardButton(text="Переглянути кошик")
    keyboard.add(button2)
    return keyboard
def keyboardBasket():
    keyboard = types.ReplyKeyboardMarkup()
    button1 = types.KeyboardButton(text="Меню")
    keyboard.add(button1)
    button2 = types.KeyboardButton(text="Оформити замовлення")
    keyboard.add(button2)
    button3 = types.KeyboardButton(text="Переглянути кошик")
    keyboard.add(button3)
    return keyboard
def keyboardContact():
    keyboard = types.ReplyKeyboardMarkup()
    Button1 = types.KeyboardButton(text = 'Отправить свой контакт ☎️', request_contact =True)
    Button2 = types.KeyboardButton(text = 'Отправить свою локацию 🗺️', request_location=True)
    keyboard.add(Button1)
    keyboard.add(Button2)
    return keyboard

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.answer("Вас вітає ХХ, готові зробити замовлення?", reply_markup=keyboardStart())

@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    row_id = int(message.text[4:])
    MENU[row_id].OfBasket()
    await message.answer("Видалено з кошика")

@dp.message_handler(lambda message: message.text == "Меню")
async def menu1(message: types.Message):
    await message.answer("Оберіть розділ", reply_markup=keyboardMenu())

@dp.message_handler(lambda message: message.text == "Переглянути кошик")
async def basket(message: types.Message):
    await message.answer(printBasket(), reply_markup=keyboardBasket())

@dp.message_handler(lambda message: message.text == "Піца" or message.text == "Чай")
async def menu(message: types.Message):
    section = "pizza" if message.text == "Піца" else "tea"
    await message.answer(message.text, reply_markup=keyboardBack())
    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(MENU)):
        if MENU[i].ifSection(section):
            name = MENU[i].GetName()
            keyboard.add(types.InlineKeyboardButton(text=name, callback_data=f"addOder_{i}"),)
    photo = open(section+'.jpg', 'rb')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    await message.answer("Замовити", reply_markup=keyboard)

# def register_handlers_food(dp: Dispatcher):
#     dp.register_message_handler(oder_adress, Text="Оформити замовлення", state="*")
#     dp.register_message_handler(oder_fone_namder, state=OrderFood.waiting_for_adress)
#     dp.register_message_handler(oder, state=OrderFood.waiting_for_fone_namber)

@dp.message_handler(lambda message: message.text == "Оформити замовлення", state="*")
async def oder_adress(message: types.Message, state: FSMContext):
    await message.answer("Введіть ваш адрес")
    await OrderFood.waiting_for_adress.set()

@dp.message_handler(state=OrderFood.waiting_for_adress)
async def oder_fone_namder(message: types.Message, state: FSMContext):
    await state.update_data(adress=message.text.lower())
    await message.answer("Введіть номер телефону")
    await OrderFood.next()

@dp.message_handler(state=OrderFood.waiting_for_fone_namber)
async def oder(message: types.Message, state: FSMContext):
    await state.update_data(fone=message.text.lower())
    user_data = await state.get_data()
    oders = f"{message.from_user.username}, {message.from_user.full_name}\n" \
            f"адрес  {user_data['adress']}\n" \
            f"номер телефона {user_data['fone']}\n"
    oders += printBasket()
    await message.answer(oders)
    await state.finish()

@dp.callback_query_handler(Text(startswith="addOder_"))
async def add(callback: types.CallbackQuery):
    i = int(callback.data.split('_')[1])
    MENU[i].ToBasket()
    await callback.answer("Додано до кошика")

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
    # await dp.storage.close()
    # await dp.storage.wait_closed()
