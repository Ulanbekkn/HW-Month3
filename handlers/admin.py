from config import ADMINS, bot
from aiogram import types, Dispatcher

async def ban(message: types.Message):
    if message.chat.type != "private":
        username = f"@{message.from_user.username}"\
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

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(ban, commands=["ban"], commands_prefix="!/")
    dp.register_message_handler(pin, commands=["pin"], commands_prefix=["!"])
