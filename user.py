import sqlite3 as sql


class User:
    def __init__(self, telegram_id, database='db.sqlite3'):
        self.database = database
        self.telegram_id = telegram_id
        self.user_id = self.get_user_id()
        self.first_name, self.last_name = self.get_user_name_lastname()

    def db_execute(self, query):
        connection = sql.connect(self.database)
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

    def get_user_id(self):
        query = f"SELECT user_id from userprofile_userprofile where telegram_id='{self.telegram_id}'"
        response = self.db_execute(query)
        if response:
            return response[0][0]
        else:
            return response

    def get_user_name_lastname(self):
        query = f"SELECT first_name, last_name FROM auth_user where id={self.user_id}"
        response = self.db_execute(query)
        if response:
            return response[0]
        else:
            return False, False