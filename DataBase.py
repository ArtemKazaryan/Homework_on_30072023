import sqlite3

class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def _get_objects(self, table):
        try:
            self.__cur.execute(f'SELECT * FROM {table}')
            res = self.__cur.fetchall()
            if res:
                return res
        except IOError:
            print('Ошибка чтения данных')
        return []

    def get_menu(self):
        return self._get_objects('menu')

    def get_transacts(self):
        return self._get_objects('transacts')

    # Попытка прописать метод удаления из БД строки по айдишнику
    # def delete_transact(self, transact_id):
    #     try:
    #         self.__cur.execute(f'DELETE FROM transacts WHERE id == "{transact_id}";')
    #         self.__db.commit()
    #     except sqlite3.Error as e:
    #         print('Ошибка удаления!', e)
    #         return False
    #     return True


    def add_transact(self, date, income_expenditure, product, price, quantity):
        try:
            self.__cur.execute('INSERT INTO transacts VALUES(NULL, ?, ?, ?, ?, ?)',
                               (date, income_expenditure, product, price, quantity))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка добавления транзакции в базу данных', e)
            return False
        return True


    def get_transact(self, transact_id):
        try:
            self.__cur.execute(f'SELECT product, transact FROM transacts WHERE id == "{transact_id}"')
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print('Ошибка получения транзакции из базы данных', e)
        return None, None