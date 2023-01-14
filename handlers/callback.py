from aiogram import types, Dispatcher
from config import bot

async def quiz_1(call: types.CallbackQuery):
    question = "Answer the question"
    answers = [
        "[1, 2, 3]",
        "[1, 2, 3, 4]",
        "[5, 6, 7]",
        "Error"
    ]
    photo = open("Media/Quick-Answer-Python-Append-to-a-Tuple-1024x482 (1).png", "rb")
    await bot.send_photo(chat_id=call.message.chat.id, photo=photo)
    await bot.send_poll(chat_id=call.message.chat.id, question=question, options=answers, is_anonymous=False,
                        type="quiz", correct_option_id=3, explanation="Top guide", open_period=60)


async def quiz_2(call: types.CallbackQuery):
    question = "Зима не будет?"
    answers = [
        "Нет",
        "Возможно",
        "Будет",
        "Алилуя"
    ]
    photo = open("Media/aoa.jpeg", "rb")
    await bot.send_photo(chat_id=call.message.chat.id, photo=photo)
    await bot.send_poll(chat_id=call.message.chat.id, question=question, options=answers, is_anonymous=False,
                        type="quiz", correct_option_id=2)


async def quiz_3(call: types.CallbackQuery):
    question = "The best guide?"
    answers = [
        "Sergey",
        "Guljigit",
        "Maks",
        "Aldapsayr",
        "Elon Mask"
    ]
    await bot.send_poll(chat_id=call.message.chat.id, question=question, options=answers, is_anonymous=False,
                        type="quiz", correct_option_id=1, explanation="Top guide", open_period=10)




def register_handlers_callback(dp: Dispatcher):
    dp.register_callback_query_handler(quiz_1, text="call_quiz_1")
    dp.register_callback_query_handler(quiz_2, text="call_quiz_2")
    dp.register_callback_query_handler(quiz_3, text="call_quiz_3")
