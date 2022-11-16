import sqlite3


conn = sqlite3.connect('slova.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS words(
   User_id INT,
   Word_ENG TEXT,
   Word_RU TEXT);
""")


conn.commit()
conn.close() #закрываем соединение с базой данных
