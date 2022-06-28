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
    corect = State()
    waiting_for_corect = State()


with open("menu.json", "r", encoding='utf-8') as read_file:
    init = json.load(read_file)
    read_file.close()
MENU = {dish["id"]: Dish(dish) for dish in init["menu"]}
# Объект бота
bot = Bot(token=init["token"])
# Диспетчер для бота
# db.start()
storage = MongoStorage(host='localhost', port=27017, db_name='bot', db_collection='state')
dp = Dispatcher(bot, storage=storage)

def newBasket(id):
    if db.collOrder.find_one({"UserID": id}) == None:
        db.collOrder.insert_one({"UserID": id})


# Включаем логирование, чтобы не пропустить важные сообщения
# logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.answer("Вас вітає ХХ, готові зробити замовлення?", reply_markup=keyboard.Start())


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    row_id = message.text[4:]
    db.collOrder.update_one({"UserID": message.from_user.id}, {'$inc': {row_id: -1}})
    await message.answer("Видалено з кошика")


@dp.message_handler(lambda message: message.text == "Меню")
async def menu1(message: types.Message):
    await message.answer("Оберіть розділ", reply_markup=keyboard.Menu())


@dp.message_handler(lambda message: message.text == "Переглянути кошик")
async def lookbasket(message: types.Message):
    await message.answer(basket.Print(MENU, db.collOrder.find_one({"UserID": message.from_user.id})),
                         reply_markup=keyboard.Basket())

@dp.message_handler(lambda message: message.text == "Очистити кошик")
async def cleanbasket(message: types.Message):
    db.collOrder.delete_one({"UserID": message.from_user.id})
    await message.answer("Ваш кошик очищено", reply_markup=keyboard.Start())


@dp.message_handler(lambda message: message.text in ["Піца", "Чай"])
async def menu(message: types.Message):
    newBasket(message.from_user.id)
    section = "pizza" if message.text == "Піца" else "tea"
    await message.answer(message.text, reply_markup=keyboard.Start())
    photo = open(section + '.jpg', 'rb')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    await message.answer("Замовити", reply_markup=keyboard.menu(MENU, section))


@dp.message_handler(lambda message: message.text == "Оформити замовлення", state="*")
async def oder_start(message: types.Message, state: FSMContext):
    user = db.collClient.find_one({"UserID": message.from_user.id})
    if user != None:
        await message.answer("Знайдено ваш профіль. Введіть коментар до замовлення")
        await OrderFood.corect.set()
    else:
        await message.answer("Введіть ваш адрес")
        await OrderFood.waiting_for_adress.set()


@dp.message_handler(state=OrderFood.waiting_for_adress)
async def oder_adres(message: types.Message, state: FSMContext):
    await state.update_data(adress=message.text.lower())
    await message.answer("Введіть номер телефону", reply_markup=keyboard.contact())
    await OrderFood.next()

@dp.message_handler(content_types=['contact'], state=OrderFood.waiting_for_fone_namber)
async def oder_contact(message: types.Message, state: FSMContext):
    await state.update_data(fone = message.contact.phone_number.lower())
    await message.answer("Введіть коментар до замовлення")
    await OrderFood.next()


@dp.message_handler(state=OrderFood.waiting_for_fone_namber)
async def oder_fone_namder(message: types.Message, state: FSMContext):
    await state.update_data(fone=message.text.lower())
    await message.answer("Введіть коментар до замовлення")
    await OrderFood.next()


@dp.message_handler(state=OrderFood.corect)
async def oder_creat(message: types.Message, state: FSMContext):
    db.collOrder.update_one({"UserID": message.from_user.id}, {'$set': {"coment": message.text}})
    user = db.collClient.find_one({"UserID": message.from_user.id})

    if user == None:
        user_data = await state.get_data()
        newUser = {
            "UserID": message.from_user.id,
            "UserName": message.from_user.username,
            "name": message.from_user.full_name,
            "adress": user_data['adress'],
            "fone": user_data['fone']
        }
        db.collClient.insert_one(newUser)
    Basket = db.collOrder.find_one({"UserID": message.from_user.id})
    await message.answer(basket.Close(MENU, db.collClient.find_one({"UserID": message.from_user.id}),
                                      db.collOrder.find_one({"UserID": message.from_user.id})),
                         reply_markup=keyboard.Corect())
    await OrderFood.next()


@dp.message_handler(lambda message: message.text == "Так, все правильно", state=OrderFood.waiting_for_corect)
async def ok(message: types.Message, state: FSMContext):
    db.collOrder.update_one({"UserID": message.from_user.id}, {'$set': {"time": datetime.datetime.now()}})
    db.collFOrder.insert_one(db.collOrder.find_one_and_delete({"UserID": message.from_user.id}))
    await state.finish()
    await message.answer("Ваше замовлення прийнято", reply_markup=keyboard.Start())


@dp.message_handler(lambda message: message.text == "Змінити замовлення", state=OrderFood.waiting_for_corect)
async def changeBasket(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(basket.Print(MENU, db.collClient.find_one({"UserID": message.from_user.id}),
                                      db.collOrder.find_one({"UserID": message.from_user.id})),
                         reply_markup=keyboard.Basket())


@dp.message_handler(lambda message: message.text == "Змінити мої дані", state=OrderFood.waiting_for_corect)
async def changeData(message: types.Message, state: FSMContext):
    db.collClient.delete_one({"UserID": message.from_user.id})
    await oder_start(message, state)


@dp.callback_query_handler(Text(startswith="addOder_"))
async def add(callback: types.CallbackQuery):
    i = callback.data.split('_')[1]
    db.collOrder.update_one({"UserID": callback.from_user.id}, {'$inc': {i: 1}})
    await callback.answer("Додано до кошика")


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
