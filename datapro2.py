import sqlite3
conn=sqlite3.connect("sqdatapro2.db")
cursor=conn.cursor()
#new_column = "month"
#cursor.execute(f"ALTER TABLE bill ADD COLUMN {new_column} DATE")
#cursor.execute('''CREATE TABLE IF NOT EXISTS income (  
#                price REAL)''')

#cursor.execute('''DELETE FROM myOrder''')
#cursor.execute('''ALTER TABLE bill DROP COLUMN date;''')

# ลบตาราง
cursor.execute('DROP TABLE IF EXISTS menu;')

conn.commit()
conn.close()