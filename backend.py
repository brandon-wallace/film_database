#!/usr/bin/env python3
import sqlite3


def create_table():
    ''' Create table if not existing '''

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS films (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT,
                   length INTEGER,
                   year INTEGER)''')
    conn.commit()
    conn.close()


def insert(title, length, year):
    '''Add an entry into database.'''

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO films (title, length, year) VALUES (?, ?, ?)", (title, length, year))
    conn.commit()
    conn.close()


def read():
    '''Query all rows.'''

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM films")
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete(id):
    '''Delete records from database.'''

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM films WHERE id=?", (id,))
    conn.commit()
    conn.close()


def update(id, title, length, year):
    '''Update a database records.'''

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("UPDATE films SET title=?, length=?, year=? WHERE id=?", (title, length, year, id))
    conn.commit()
    conn.close()


create_table()
