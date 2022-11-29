import sqlite3


conn = sqlite3.connect('slova.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS words(
   User_id INT,
   Word_ENG TEXT,
   Word_RU TEXT,
   True_straick INT);
""")

cur.execute("""CREATE TABLE IF NOT EXISTS users(
   TG_id INT,
   State TEXT,
   Current_word INT);
""")

conn.commit()
conn.close() #закрываем соединение с базой данных

