import sqlite3


conn = sqlite3.connect('status.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS stat(
   User_id INT,
   Word_ENG TEXT,
   Word_RU TEXT);
""")


conn.commit()
conn.close()