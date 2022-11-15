from config import tokenbot, login_token, chat_id
from yaDirect import yaBalance, yaStat
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Настраиваем логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s / %(levelname)s / %(message)s')

# Инициализация бота
bot = Bot(token=tokenbot)
dp = Dispatcher(bot, storage=MemoryStorage())

# Создание клавиатуры
kb_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(KeyboardButton('Получить информацию'))

# Старт
@dp.message_handler(commands=['start'])
async def mes_start(message: types.Message):
    user_id = str(message.from_user.id)
    await message.answer(f"Привет {user_id}", reply_markup=kb_start)

# Отправление баланса по запросу
@dp.message_handler(regexp='(Получить информацию)')
async def GetInfo(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id in chat_id:
        for item in login_token.items():
            info_balance = yaBalance(item[1], item[0])
            info_stat = yaStat(item[1], item[0])
            await message.answer(f"{info_stat}\nОстаток баланса: {info_balance[1]} {info_balance[2]}", reply_markup=kb_start)

# запускаем лонг поллинг
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)