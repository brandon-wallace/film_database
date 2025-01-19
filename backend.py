#!/usr/bin/env python3
import sqlite3
from contextlib import contextmanager


DATABASE = 'database.db'


@contextmanager
def connect_to_db():
    '''Create connection to database'''

    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        yield conn
    except sqlite3.Error as e:
        raise Exception(f'Database error: {str(e)}')
    finally:
        if conn:
            conn.close()

def create_table():
    ''' Create table if not existing'''

    sql = '''CREATE TABLE IF NOT EXISTS films (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT NOT NULL,
                   length INTEGER NOT NULL,
                   year INTEGER NOT NULL)'''

    with connect_to_db() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()


def insert(title, length, year):
    '''Add database entry'''

    sql = '''INSERT INTO films (title, length, year) VALUES (?, ?, ?)'''

    with connect_to_db() as conn:
        cur = conn.cursor()
        cur.execute(sql, (title.strip(), int(length), int(year)))
        conn.commit()


def read():
    '''Query all records.'''

    sql = '''SELECT * FROM films'''

    with connect_to_db() as conn:
        cur = conn.cursor()
        cur.execute(sql)
        return cur.fetchall()


def delete(id):
    '''Delete a record from database.'''

    if not isinstance(id, (int, str)) or not str(id).isdigit():
        raise ValueError("ID is not valid")

    sql = '''DELETE FROM films WHERE id=?''' 

    with connect_to_db() as conn:
        cur = conn.cursor()
        cur.execute(sql, (int(id),))
        success = cur.rowcount > 0
        conn.commit()
        return success


def update(id, title, length, year):
    '''Update a database records.'''

    sql = '''UPDATE films SET title=?, length=?, year=? WHERE id=?'''

    with connect_to_db() as conn:
        cur = conn.cursor()
        cur.execute(sql, (title.strip(), int(length), int(year), int(id)))
        success = cur.rowcount > 0
        conn.commit()
        return success


create_table()
