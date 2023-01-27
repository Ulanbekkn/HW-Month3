from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from .generator_id import gen_id
from database.bot_db import sql_command_insert


class FSMAdmin(StatesGroup):
    id = State()
    name = State()
    direction = State()
    age = State()
    group = State()
    submit = State()


async def fsm_start(message: types.Message):
    if message.chat.type == "private":
        await FSMAdmin.id.set()
        await message.answer("ID ментора автоматически записан, продолжим?")
    else:
        await message.answer("Пиши в личку!")


async def load_id(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        async with state.proxy() as data:
            data['id'] = gen_id()
        await FSMAdmin.next()
        await message.answer("Имя ментора")
    else:
        await state.finish()
        await message.answer("Завершение")


async def load_name(message: types.Message, state: FSMContext):
    if message.text.isalpha():
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.answer("Какое направление у ментора")
    else:
        await message.answer("Только буквы")


async def load_direction(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['direction'] = message.text
    await FSMAdmin.next()
    await message.answer("Сколько лет ментору")


async def load_age(message: types.Message, state: FSMContext):
    try:
        if int(message.text) <= 0:
            await message.answer("Только положительные числа!")
        else:
            if 16 < int(message.text) < 50:
                async with state.proxy() as data:
                    data['age'] = message.text
                await FSMAdmin.next()
                await message.answer("Группа ментора")
            else:
                await message.answer("Доступ воспрещен!")
    except ValueError:
        await message.answer("Только числа")


async def load_group(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = message.text
        await message.answer(f"Информация о менторе:\n"
                             f"ID: {data['id']}\n"
                             f"Name: {data['name']}\n"
                             f"Direction: {data['direction']}\n"
                             f"Age: {data['age']}\n"
                             f"Group: {data['group']}")
    await FSMAdmin.next()
    await message.answer("Все правильно?")


async def submit(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        await sql_command_insert(state)
        await state.finish()
        await message.answer("Завершение")
    elif message.text.lower() == "нет":
        await state.finish()
    else:
        await message.answer("Не понял, Да или Нет?")


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer("Canceled")


def register_handlers_state(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, Text(equals='cancel', ignore_case=True), state='*')

    dp.register_message_handler(fsm_start, commands=['reg'])
    dp.register_message_handler(load_id, state=FSMAdmin.id)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_direction, state=FSMAdmin.direction)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    dp.register_message_handler(load_group, state=FSMAdmin.group)
    dp.register_message_handler(submit, state=FSMAdmin.submit)
