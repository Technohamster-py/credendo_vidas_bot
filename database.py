import sqlite3 as sql


def take_item(id=0):
    connection = sql.connect('db.sqlite3')
    cursor = connection.cursor()
    query = "SELECT * FROM store_operation"
    response = cursor.execute(query)
    print(response.fetchall())


def put_item(id):
    connection = sql.connect('db.sqlite3')
    query = connection.cursor()


take_item()