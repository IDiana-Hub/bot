from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.mongo import MongoStorage
import dbconect as db
import json
from Dish import Dish
import datetime
import keyboard
import basket

class OrderFood(StatesGroup):
    waiting_for_adress = State()
    waiting_for_fone_namber = State()
    corect=State()
    waiting_for_corect=State()

with open("menu.json", "r", encoding='utf-8') as read_file:
    init = json.load(read_file)
    read_file.close()
MENU = [Dish(dish) for dish in init["menu"]]
# Объект бота
bot = Bot(token=init["token"])
#Диспетчер для бота
#db.start()
storage = MongoStorage(host='localhost', port=27017, db_name='bot', db_collection='state')
dp = Dispatcher(bot, storage = storage)
# Включаем логирование, чтобы не пропустить важные сообщения
#logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.answer("Вас вітає ХХ, готові зробити замовлення?", reply_markup=keyboard.Start())

@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    row_id = int(message.text[4:])
    MENU[row_id].OfBasket()
    await message.answer("Видалено з кошика")

@dp.message_handler(lambda message: message.text == "Меню")
async def menu1(message: types.Message):
    await message.answer("Оберіть розділ", reply_markup=keyboard.Menu())

@dp.message_handler(lambda message: message.text == "Переглянути кошик")
async def lookbasket(message: types.Message):
    await message.answer(basket.print(MENU), reply_markup = keyboard.Basket())

@dp.message_handler(lambda message: message.text == "Піца" or message.text == "Чай")
async def menu(message: types.Message):
    section = "pizza" if message.text == "Піца" else "tea"
    await message.answer(message.text, reply_markup = keyboard.Back())
    photo = open(section+'.jpg', 'rb')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    await message.answer("Замовити", reply_markup=keyboard.menu(MENU, section))

@dp.message_handler(lambda message: message.text == "Оформити замовлення", state="*")
async def oder_start(message: types.Message, state: FSMContext):
    user = db.collClient.find_one({"userID": message.from_user.id})
    if user != None:
        await message.answer("Знайдено ваш профіль. Використовувати існуючі дані?")
        await OrderFood.corect.set()
    else:
        await message.answer("Введіть ваш адрес")
        await OrderFood.waiting_for_adress.set()

@dp.message_handler(state=OrderFood.waiting_for_adress)
async def oder_adres(message: types.Message, state: FSMContext):
    await state.update_data(adress=message.text.lower())
    await message.answer("Введіть номер телефону")
    await OrderFood.next()

@dp.message_handler(state=OrderFood.waiting_for_fone_namber)
async def oder_fone_namder(message: types.Message, state: FSMContext):
    await state.update_data(fone=message.text.lower())
    await message.answer("Ваші дані збережені")
    await OrderFood.next()

@dp.message_handler(state=OrderFood.corect)
async def oder_creat(message: types.Message, state: FSMContext):
    time = datetime.datetime.now()
    user = db.collClient.find_one({"userID": message.from_user.id})
    if user != None:
        user_data = {'adress': user.get('adress'), 'fone': user.get('fone')}
    else:
        user_data = await state.get_data()
        newUser = {
            "userID": message.from_user.id,
            "name": message.from_user.full_name,
            "adress": user_data['adress'],
            "fone": user_data['fone']
        }
        db.collClient.insert_one(newUser)
    Basket = basket.close(MENU)
    oder = {
        "time": time,
        "username": message.from_user.username,
        "name": message.from_user.full_name,
        "adress": user_data['adress'],
        "fone": user_data['fone'],
        "basket": Basket
    }
    await state.update_data(oder=oder)
    await message.answer(basket.print(MENU, oder), reply_markup=keyboard.Corect())
    await OrderFood.next()

@dp.message_handler(lambda message: message.text == "Так, все правильно", state=OrderFood.waiting_for_corect)
async def ok(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    db.collection.insert_one(user_data['oder'])
    await state.finish()
    await message.answer("Ваше замовлення прийнято", reply_markup=keyboard.Start())

@dp.message_handler(lambda message: message.text == "Змінити замовлення", state=OrderFood.waiting_for_corect)
async def changeBasket(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(basket.print(MENU), reply_markup=keyboard.Basket())

@dp.message_handler(lambda message: message.text == "Змінити мої дані", state=OrderFood.waiting_for_corect)
async def changeData(message: types.Message, state: FSMContext):
    db.collClient.delete_one({"userID": message.from_user.id})
    await oder_start(message, state)

@dp.callback_query_handler(Text(startswith="addOder_"))
async def add(callback: types.CallbackQuery):
    i = int(callback.data.split('_')[1])
    MENU[i].ToBasket()
    await callback.answer("Додано до кошика")

@dp.callback_query_handler()
async def exo(message: types.Message):
    await message.reply(message.text)

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
    # await dp.storage.close()
    # await dp.storage.wait_closed()
