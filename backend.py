#!/usr/bin/env python3
import sqlite3


DATABASE = 'database.db'

def create_table():
    ''' Create table if not existing '''

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS films (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT,
                   length INTEGER,
                   year INTEGER)''')
    conn.commit()
    conn.close()


def insert(title, length, year):
    '''Add entry into database.'''

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO films (title, length, year) VALUES (?, ?, ?)", (title.strip(), length, year))
    conn.commit()
    conn.close()


def read():
    '''Query all records.'''

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM films")
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete(id):
    '''Delete a record from database.'''

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("DELETE FROM films WHERE id=?", (id,))
    conn.commit()
    conn.close()


def update(id, title, length, year):
    '''Update a database records.'''

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("UPDATE films SET title=?, length=?, year=? WHERE id=?", (title, length, year, id))
    conn.commit()
    conn.close()


create_table()
