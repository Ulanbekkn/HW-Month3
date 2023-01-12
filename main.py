from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from decouple import config
import logging

TOKEN = config("TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=f"Welcome my master {message.from_user.first_name}")
    await message.answer(f"How are you?")
    await message.reply(f"This is a reply method")

@dp.message_handler(commands=["quiz"])
async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton("NEXT", callback_data="button_call_1")
    markup.add(button_call_1)

    question = "The best guide?"
    answers = [
        "Sergey",
        "Guljigit",
        "Maks",
        "Aldapsayr",
        "Elon Mask"
    ]
    await bot.send_poll(chat_id=message.from_user.id, question=question, options=answers, is_anonymous=False,
                        type="quiz", correct_option_id=1, explanation="Top guide", open_period=60, reply_markup=markup)

@dp.callback_query_handler(text="button_call_1")
async def quiz_2(call: types.CallbackQuery):
    question = "Answer the question"
    answers = [
        "[1, 2, 3]",
        "[1, 2, 3, 4]",
        "[5, 6, 7]",
        "Error"
    ]
    photo = open("Media/Quick-Answer-Python-Append-to-a-Tuple-1024x482 (1).png", "rb")
    await bot.send_photo(call.from_user.id, photo=photo)
    await bot.send_poll(chat_id=call.from_user.id, question=question, options=answers, is_anonymous=False,
                        type="quiz", correct_option_id=3, explanation="Top guide", open_period=60)

@dp.message_handler(commands=["mem"])
async def mem_1(message: types.Message):
    photo = open("Media/hoh.jpg", "rb")
    await bot.send_photo(chat_id=message.from_user.id, photo=photo)

@dp.message_handler()
async def echo(message: types.Message):
    if message.text.isdigit():
        await message.answer(int(message.text) ** 2)
    else:
        await bot.send_message(chat_id=message.from_user.id, text=message.text)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
