import random
import sqlite3
import pandas as pd

database_path = 'used_pictures.db'

def db_init():
  conn = sqlite3.connect(database_path)
  cursor = conn.cursor()
  cursor.execute('''
      CREATE TABLE IF NOT EXISTS used_pictures (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          filename TEXT UNIQUE
      )
  ''')
  conn.commit()


def filter_dataframe(retrieved_items_df):
  db_init()
  conn = sqlite3.connect(database_path)
  cursor = conn.cursor()
  cursor.execute('SELECT filename FROM used_pictures')
  used_pictures_db = [row[0] for row in cursor.fetchall()]
  used_pictures_df = pd.DataFrame(used_pictures_db, columns=['filename'])
  mask = retrieved_items_df['filename'].isin(used_pictures_df['filename'])
  filter_dataframe = retrieved_items_df[~mask]
  return filter_dataframe

def select_random_baseUrl(filter_dataframe):
  db_init()
  conn = sqlite3.connect(database_path)
  cursor = conn.cursor()
  if filter_dataframe.shape[0] > 0:
    sample = filter_dataframe.sample().iloc[0]
    cursor.execute('INSERT INTO used_pictures (filename) VALUES (?)', (sample.filename,))
  else:
    cursor.execute('DELETE FROM used_pictures')
  conn.commit()
  conn.close()
  return sample.filename, sample.baseUrl


