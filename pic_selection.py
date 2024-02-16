import os
import random
import sqlite3

folder_path = './images'
all_files = os.listdir(folder_path)
database_path = 'used_pictures.db'

conn = sqlite3.connect(database_path)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS used_pictures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT UNIQUE
    )
''')
conn.commit()

all_files = [file for file in os.listdir(folder_path) if file.lower()]

cursor.execute('SELECT filename FROM used_pictures')
used_files = [row[0] for row in cursor.fetchall()]
print(used_files)
remaining_files = [file for file in all_files if file not in used_files]

if remaining_files:
    selected_file = random.choice(remaining_files)
    print(f"Selected file: {selected_file}")
    cursor.execute('INSERT INTO used_pictures (filename) VALUES (?)', (selected_file,))
    conn.commit()
else:
    cursor.execute('DELETE FROM used_pictures')
    conn.commit()

conn.close()

