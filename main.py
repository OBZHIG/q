from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


import sqlite3
import random

bot = Bot(token="5302161624:AAEybahOADvKeHUEufzo6unoQ51u1VJ4z4Q")
dp = Dispatcher(bot)



@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    conn = sqlite3.connect('slova.db')
    cur = conn.cursor()
    cur.execute(f"""INSERT INTO users(TG_id,State,Current_word) 
                VALUES({message.from_user.id},"a",0);""")
    conn.commit()
    await message.reply("Привет!\nНапиши мне что-нибудь!")


@dp.message_handler(commands=['fill'])
async def process_help_command(message: types.Message):


    conn = sqlite3.connect('slova.db')
    cur = conn.cursor()

    cur.execute(f"UPDATE users SET State='fill' where TG_id={message.from_user.id};")
    conn.commit()

    await message.reply("отправте сообщение в формате слова:перевод")


@dp.message_handler(commands=['opros'])
async def process_help_command(message: types.Message):
    conn = sqlite3.connect('slova.db')
    cur = conn.cursor()
    cur.execute(f"SELECT Current_word FROM users WHERE TG_id={message.from_user.id};")
    g = cur.fetchone()[0]
    cur.execute(f"UPDATE users SET State='opros' WHERE TG_id={message.from_user.id};")

    conn.commit()
    await message.reply('опрос начинается')
    cur.execute(f"SELECT Word_ENG,Word_RU FROM words WHERE User_id={message.from_user.id};")
    all_results = cur.fetchall()
    print(all_results)
    await bot.send_message(message.from_user.id, all_results[g][1])
    print(g)
@dp.message_handler()
async def echo_message(msg: types.Message):

    conn = sqlite3.connect('slova.db')
    cur = conn.cursor()
    cur.execute(f"SELECT State FROM users WHERE TG_id={msg.from_user.id};")
    state = cur.fetchone()[0]
    print(state)
    if state == 'fill':
        f = msg.text.split(":")
        cur.execute(f"""INSERT INTO words(User_id,Word_ENG, Word_RU, True_straick)
    VALUES({msg.from_user.id},'{f[0]}',"{f[1]}",0);
        """)
        conn.commit()
        conn.close()
        await bot.send_message(msg.from_user.id, "добавили")
    elif state == 'opros':
        cur.execute(f"SELECT Current_word FROM users WHERE TG_id={msg.from_user.id};")
        g = cur.fetchone()[0]
        cur.execute(f"SELECT Word_ENG,Word_RU FROM words WHERE User_id={msg.from_user.id} AND True_straick < 5;")
        all_results = cur.fetchall()

        if g == len(all_results) -1:

            cur.execute(f"UPDATE users SET Current_word={g} where TG_id={msg.from_user.id};")
            await bot.send_message(msg.from_user.id, "ok!")
            cur.execute(f"SELECT True_straick FROM words WHERE Word_RU='{all_results[g][1]}'")
            t = cur.fetchone()[0] + 1
            cur.execute(f"UPDATE words SET True_straick={t} WHERE Word_RU='{all_results[g][1]}'")
            g = 0
            cur.execute(f"UPDATE users SET Current_word={g} where TG_id={msg.from_user.id};")
            conn.commit()
            await bot.send_message(msg.from_user.id, "опрос завершен!")
            state = "fill"
        elif all_results[g][0]==msg.text:
            await bot.send_message(msg.from_user.id, "ok!")
            cur.execute(f"SELECT True_straick FROM words WHERE Word_RU='{all_results[g][1]}'")
            t=cur.fetchone()[0] + 1
            cur.execute(f"UPDATE words SET True_straick={t} WHERE Word_RU='{all_results[g][1]}'")
            g += 1
            cur.execute(f"UPDATE users SET Current_word={g} where TG_id={msg.from_user.id};")
            conn.commit()

            await bot.send_message(msg.from_user.id, all_results[g][1])
        else:
            await bot.send_message(msg.from_user.id, "нет не то пробуй еще")





if __name__ == '__main__':
    executor.start_polling(dp)