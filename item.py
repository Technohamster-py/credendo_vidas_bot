import sqlite3 as sql
from datetime import datetime
import logging


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
        if 'INSERT' in query or 'UPDATE' in query:
            try:
                cursor.execute(query)
                connection.commit()
                return True
            except Exception as exception:
                print(exception)
                return False
        else:
            try:
                return cursor.execute(query).fetchall()
            except Exception as exception:
                print(exception)
                return False

    def update_last_status_change(self, action, last_name='Админ', first_name='Админ'):
        max_id = self.db_execute("SELECT id from store_operation")[-1][0]
        self.last_status_change = datetime.now().isoformat(sep=" ", timespec='seconds')
        query = f"INSERT INTO store_operation VALUES ({max_id+1}, '{first_name}', '{last_name}', '{action}', '{self.last_status_change}', '{self.id}');"
        return self.db_execute(query)

    def is_available(self):
        return self.quantity_available > 0

    def take(self, last_name='Админ', first_name='Админ', is_passed=False):
        if self.is_available() or is_passed:
            if not is_passed:
                self.quantity_available -= 1
            if self.quantity_available == 0:
                self.status = 0
            action = 'TAKE'

            if self.update_last_status_change(action, last_name, first_name):
                query = f"UPDATE store_item SET status = {self.status}, quantity_available = {self.quantity_available}, last_status_change = '{self.last_status_change}' WHERE id = {self.id}"
                return self.db_execute(query)
            else:
                return False
        else:
            return -1

    def put(self, last_name='Админ', first_name='Админ'):
        if self.quantity_available == self.quantity_total:
            return -1
        self.quantity_available += 1
        self.status = 1
        action = 'RETURN'
        if self.update_last_status_change(action, last_name, first_name):
            query = f"UPDATE store_item SET status = {self.status}, quantity_available = {self.quantity_available}, last_status_change = '{self.last_status_change}' WHERE id = {self.id}"
            return self.db_execute(query)
        else:
            return False


item = Item(35)
item.put()