import sqlite3 as sql


def take_item(id):
    connection = sql.connect('db.sqlite3')
    query = connection.cursor()
