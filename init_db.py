import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS farmers
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              location TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS buyers
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              location TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS crops
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              farmer_id INTEGER,
              crop_name TEXT,
              quantity TEXT,
              expected_price REAL)''')

c.execute('''CREATE TABLE IF NOT EXISTS offers
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              buyer_id INTEGER,
              crop_id INTEGER,
              offered_price REAL,
              status TEXT DEFAULT 'Pending')''')

conn.commit()
conn.close()
