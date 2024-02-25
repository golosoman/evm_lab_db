import mysql.connector as conn
from mysql.connector import errorcode
from config import DB_PASSWORD, DB_NAME

import json


class DataBaseHandler:
    def __init__(self, dbName, password):
        self.dbName = dbName
        self.password = password
        self.__openConnection()

    def __openConnection(self):
        try:
            self.cnx = conn.connect(
                host='localhost',
                user='root',
                password=self.password,
                database=self.dbName
            )
            self.cnx.autocommit = True
        except conn.Error as err_:
            if err_.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Неверный логин или пароль")
            elif err_.errno == errorcode.ER_BAD_DB_ERROR:
                self.cnx = conn.connect(
                    host='localhost',
                    user='root',
                    password=self.password
                )
                self.cnx.autocommit = True
                with self.cnx.cursor() as cursor_:
                    cursor_.execute(f"create database if not exists {self.dbName}")
                    cursor_.execute(f"use {self.dbName}")
            else:
                print(err_)
                self.cnx.close()
                raise Exception("Что-то пошло не так...")

    def __closeConnection(self):
        self.cnx.close()

    def __executeQuery(self, query):
        self.cnx.reconnect()
        with self.cnx.cursor(buffered=True) as cursor:
            cursor.execute(query)
            try:
                return cursor.fetchall()
            except TypeError:
                return []

    def execute(self, query):
        return self.__executeQuery(query)

    def add(self, table_name, columns, values):
        self.__executeQuery(
            f"""insert into {table_name} ({','.join(columns) if type(columns) == list and len(columns) > 1 else columns[0] if type(columns) == list else columns}) values ({','.join([f"'{item}'" if type(item) == str else str(item) for item in values]) if type(values) == list else f"'{values}'" if type(values) == str else str(values)});""")

    def update(self, table_name, columns, values, id):
        if type(columns) != list:
            columns = [columns]
        if type(values) != list:
            values = [values]
        if len(columns) == len(values):
            print(
                f"""update {table_name} set {','.join([f"{key}='{item}'" if type(item) == str else f"{key}={item}" for key, item in dict(map(lambda x, y: (x, y), columns, values)).items()])} where id = {id};""")
            self.__executeQuery(
                f"""update {table_name} set {','.join([f"{key}='{item}'" if type(item) == str else f"{key}={item}" for key, item in dict(map(lambda x, y: (x, y), columns, values)).items()])} where id = {id};""")
        else:
            raise ValueError(f"columns length ({len(columns)}) != values length ({len(values)})")

    def loadDump(self):
        if len(self.__executeQuery("show tables")) == 0:
            self.__loadSchema()
            self.__loadData()

    def __loadSchema(self):
        with open("app/sql_schema.json", "r", encoding="utf-8") as file:
            self.__executeQuery(json.load(file)['schema_dump'])

    def __loadData(self):
        with open("app/sql_schema.json", "r", encoding="utf-8") as file:
            self.__executeQuery(json.load(file)['data_dump'])

    def test(self):
        return self.__executeQuery("select * from brands")


if __name__ == "__main__":
    tmp = DataBaseHandler("evm", "")
    tmp.loadDump()

if __name__ == "app.mysqlConnector":
    dbHandler = DataBaseHandler(DB_NAME, DB_PASSWORD)
    dbHandler.loadDump()
