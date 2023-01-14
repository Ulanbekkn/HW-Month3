from config import bot
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboard.client_kb import start_markup

async def start_handler(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=f"Welcome my master {message.from_user.first_name}",
                           reply_markup=start_markup)

async def info_handler(message: types.Message):
    await bot.send_message(message.chat.id, f"Нету инфы(")

async def quiz(message: types.Message):
    markup = InlineKeyboardMarkup()
    call_quiz_1 = InlineKeyboardButton("quiz 1", callback_data="call_quiz_1")
    call_quiz_2 = InlineKeyboardButton("quiz 2", callback_data="call_quiz_2")
    call_quiz_3 = InlineKeyboardButton("quiz 3", callback_data="call_quiz_3")
    markup.add(call_quiz_1, call_quiz_2, call_quiz_3)
    photo = open("Media/aa.jpg", "rb")
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    await bot.send_message(chat_id=message.chat.id, text=f"Выберите quiz", reply_markup=markup)
    photo.close()

async def mem_1(message: types.Message):
    photo = open("Media/hoh.jpg", "rb")
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    photo.close()

async def dice_game(message: types.Message):
    username = f"@{message.from_user.username}" \
        if message.from_user.username is not None else message.from_user.first_name
    await message.answer(f"Ваш ход {username}:")
    your = await bot.send_dice(chat_id=message.chat.id, emoji="🎲")
    await message.answer(f"Мой ход:")
    my = await bot.send_dice(chat_id=message.chat.id, emoji="🎲")
    if your.dice.value == my.dice.value:
        await message.answer(f"Вывод: У нас ничья")
    elif your.dice.value > my.dice.value:
        await message.answer(f"Вывод: Вы выиграли! Поздравляю!")
    elif my.dice.value > your.dice.value:
        await message.answer(f"Вывод: Я вас уделал. Вы проиграли!")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])
    dp.register_message_handler(quiz, commands=["quiz"])
    dp.register_message_handler(mem_1, commands=["mem"])
    dp.register_message_handler(info_handler, commands=["info"])
    dp.register_message_handler(dice_game, commands=["dice"])



