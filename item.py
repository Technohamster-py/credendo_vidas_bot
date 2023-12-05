import sqlite3 as sql
from datetime import datetime


class Item:
    def __init__(self, id):
        self.id = id
        db_row = self.db_execute(f'SELECT * FROM store_item WHERE {id=}')[0]
        self.name = db_row[1]
        self.position = db_row[2]
        self.size = db_row[3]
        self.material = db_row[4]
        self.status = db_row[5]
        self.last_status_change = db_row[6]
        self.category = self.db_execute(f'SELECT name FROM store_category WHERE id={db_row[7]}')[0][0]
        self.quantity_available = db_row[8]
        self.quantity_total = db_row[9]
        self.photo = db_row[10]

    def __str__(self):
        s = (f"Item: {self.name}\n"
             f"Position: {self.position}\n"
             f"Size: {self.size}\n"
             f"Material: {self.material}\n"
             f"Status: {self.get_string_status()}\n"
             f"Last status change time: {self.last_status_change}\n"
             f"Category: {self.category}\n"
             f"Available: {self.quantity_available}/{self.quantity_total}\n"
             f"Photo filename: {self.photo}")
        return s

    def get_string_status(self):
        if self.status == 1:
            return "На складе"
        elif self.status == 0:
            return "В работе"
        else:
            return "Неизвестен"

    def db_execute(self, query):
        connection = sql.connect('db.sqlite3')
        cursor = connection.cursor()
        return cursor.execute(query).fetchall()

    def update_last_status_change(self, last_name, first_name):
        self.last_status_change = datetime.now().isoformat(sep=" ", timespec='seconds')
        query = ""

    def take_item(self, id=1):
        query = f"SELECT * FROM store_item WHERE {id=}"
        print(self.db_execute(query))

    def put_item(self, id):
        connection = sql.connect('db.sqlite3')
        query = connection.cursor()


item = Item(35)