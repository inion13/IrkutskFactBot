import logging
import random
import os
import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

from irkutskfacts import facts

logging.basicConfig(level=logging.INFO)

load_dotenv()
router = Router()

# Инициализация бота и диспетчера
# bot_token = os.getenv('TOKEN')
bot = Bot(token='6779571947:AAETLvAdgJnVBY2JfpksuNXsPGzYupDLWLs')
dp = Dispatcher()

start_button = InlineKeyboardButton(text="Начать", callback_data="start")
stop_button = InlineKeyboardButton(text="Остановить", callback_data="stop")
fact_button = InlineKeyboardButton(text="Покажи мне факт", callback_data="fact")
start_keyboard = InlineKeyboardMarkup(inline_keyboard=[[start_button]])
stop_fact_keyboard = InlineKeyboardMarkup(inline_keyboard=[[stop_button, fact_button]])


@router.message(Command(commands=['start']))
async def start(message: Message):
    await message.answer("Привет! Я могу рассказать тебе интересные факты о городе Иркутске. Хочешь послушать?",
                         reply_markup=stop_fact_keyboard)


@router.message(Command(commands=['stop']))
async def stop(message: Message):
    await message.answer("Хорошо, если захочешь почитать еще интересные факты, просто напиши мне!",
                         reply_markup=start_keyboard)


@router.message(Command(commands=['fact']))
async def send_fact(message: Message):
    fact = random.choice(facts)
    await message.answer(fact, reply_markup=stop_fact_keyboard)


@router.callback_query()
async def handle_callback_query(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    command = callback_query.data
    if command == "start":
        await start(callback_query.message)
    elif command == "stop":
        await stop(callback_query.message)
    elif command == "fact":
        await send_fact(callback_query.message)


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
