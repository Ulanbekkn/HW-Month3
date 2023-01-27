import random
import sqlite3
from config import bot


def sql_create():
    global db, cursor
    db = sqlite3.connect("bot.sqlite3")
    cursor = db.cursor()

    if db:
        print("База данных подключена!")

    db.execute("""CREATE TABLE IF NOT EXISTS mentors 
                (id INTEGER PRIMARY KEY, 
                name VARCHAR(100), 
                direction VARCHAR(100), 
                age INTEGER, 
                gruppa VARCHAR(100))""")
    db.commit()


async def sql_command_insert(state):
    async with state.proxy() as data:
        cursor.execute("""INSERT INTO mentors(id, name, direction, age, gruppa) 
                        VALUES(?, ?, ?, ?, ?)""", tuple(data.values()))
        db.commit()

async def sql_command_random(message):
    result = cursor.execute("""SELECT * FROM mentors""").fetchall()
    random_user = random.choice(result)
    await bot.send_message(message.from_user.id, f"ID: {random_user[0]}\nName: {random_user[1]}\n"
                                                 f"Direction: {random_user[2]}\n Age: {random_user[3]}\n"
                                                 f"Group: {random_user[4]}")

async def sql_command_all():
    return cursor.execute("""SELECT * FROM mentors""").fetchall()

async def sql_command_delete(user_id):
    cursor.execute("""DELETE FROM mentors WHERE id = ?""", (user_id,))
    db.commit()
