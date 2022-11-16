from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


import sqlite3
import random

bot = Bot(token="5302161624:AAEybahOADvKeHUEufzo6unoQ51u1VJ4z4Q")
dp = Dispatcher(bot)

all_results=()
state = "fill"
g = 0

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")


@dp.message_handler(commands=['fill'])
async def process_help_command(message: types.Message):
    global state
    state = 'fill'
    await message.reply("отправте сообщение в формате слова:перевод")


@dp.message_handler(commands=['opros'])
async def process_help_command(message: types.Message):
    global state
    global g
    global all_results
    state = 'opros'
    conn = sqlite3.connect('slova.db')
    cur = conn.cursor()
    await message.reply('опрос начинается')
    cur.execute(f"SELECT Word_ENG,Word_RU FROM words WHERE User_id={message.from_user.id};")
    all_results = cur.fetchall()
    random.shuffle(all_results)
    await bot.send_message(message.from_user.id, all_results[g][1])

@dp.message_handler()
async def echo_message(msg: types.Message):
    global state
    conn = sqlite3.connect('slova.db')
    cur = conn.cursor()
    if state == 'fill':
        f = msg.text.split(":")
        cur.execute(f"""INSERT INTO words(User_id,Word_ENG, Word_RU)
    VALUES({msg.from_user.id},'{f[0]}',"{f[1]}");
        """)
        conn.commit()
        conn.close()
        await bot.send_message(msg.from_user.id, "добавили")
    elif state == 'opros':
        global g
        global all_results

        if g == len(all_results) - 1:
            g = 0
            await bot.send_message(msg.from_user.id, "опрос завершен!")
            state = "fill"
        elif all_results[g][0]==msg.text:
            await bot.send_message(msg.from_user.id, "ok!")
            g += 1
            await bot.send_message(msg.from_user.id, all_results[g][1])
        else:
            await bot.send_message(msg.from_user.id, "нет не то пробуй еще")




if __name__ == '__main__':
    executor.start_polling(dp)