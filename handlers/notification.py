from aiogram import types, Dispatcher
import asyncio
import aioschedule
from config import bot


async def get_id_user(message: types.Message):
    global chat_id
    chat_id = []
    chat_id.append(message.from_user.id)
    await message.answer("Ok")


async def go_to_geektech():
    for id in chat_id:
        await bot.send_message(id, "Go to Geektech")


async def scheduler():
    aioschedule.every().day.at("17:30").do(go_to_geektech)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


def register_handlers_notification(dp: Dispatcher):
    dp.register_message_handler(get_id_user, lambda word: "напомни" in word.text)
