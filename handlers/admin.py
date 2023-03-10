from config import ADMINS, bot
from aiogram import types, Dispatcher
from database.bot_db import sql_command_all, sql_command_delete
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def ban(message: types.Message):
    if message.chat.type != "private":
        username = f"@{message.from_user.username}" \
            if message.from_user.username is not None else message.from_user.first_name
        username_2 = f"@{message.reply_to_message.from_user.username}" \
            if message.reply_to_message.from_user.username is not None else message.reply_to_message.from_user.first_name
        if message.from_user.id not in ADMINS:
            await message.answer(f"У вас нет прав администратора")
        elif not message.reply_to_message:
            await message.answer(f"Команда должна быть ответом на сообщение!")
        else:
            await bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            await message.answer(f"Админ {username} выгнал"
                                 f" {username_2} из группы")
    else:
        await message.answer("Только в группах, пиши в группу")


async def pin(message: types.Message):
    if message.chat.type != "private":
        if message.from_user.id not in ADMINS:
            await message.answer(f"У вас нет прав администратора")
        elif not message.reply_to_message:
            await message.answer(f'Команда "pin" должна быть ответом на сообщение!')
        else:
            await bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
    else:
        await message.answer(f"Только в группах. Можно было и здесь сделать, но пусть там только работать будет")


async def delete_data(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer(f"У вас нет прав администратора")
    else:
        users = await sql_command_all()
        for user in users:
            await bot.send_message(message.from_user.id, f"ID: {user[0]}\nName: {user[1]}\n"
                                                         f"Direction: {user[2]}\n Age: {user[3]}\n"
                                                         f"Group: {user[4]}",
                                   reply_markup=InlineKeyboardMarkup().add(
                                       InlineKeyboardButton(f"Delete {user[1]}", callback_data=f"delete {user[0]}")))


async def complete_delete(call: types.CallbackQuery):
    await sql_command_delete(call.data.replace("delete ", ""))
    await call.answer("Удалено", show_alert=True)
    await bot.delete_message(call.from_user.id, call.message.message_id)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(ban, commands=["ban"], commands_prefix="!/")
    dp.register_message_handler(pin, commands=["pin"], commands_prefix=["!"])
    dp.register_message_handler(delete_data, commands=["del"])
    dp.register_callback_query_handler(complete_delete,
                                       lambda call: call.data and call.data.startswith("delete "))
