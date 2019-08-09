import sqlite3

db = sqlite3.connect("./config.db")
cursor = db.cursor()
#cursor.execute('''DROP TABLE conf''')
#cursor.execute('''CREATE TABLE conf(name TEXT PRIMARY KEY, id INTEGER, cur_name TEXT)''')
#cursor.execute('''INSERT INTO conf(name, id, cur_name) VALUES(?, ?, ?)''', ("stop", 0, "NO BUTTON"))
#cursor.execute('''INSERT INTO nums(name, cnt) VALUES(?, ?)''', ("cps", 0))
db.commit()
db.close()