#!/usr/bin/env python3
from pycoingecko import CoinGeckoAPI
from resources import *

cg = CoinGeckoAPI()

# Modify the database class
class DataBaseMod(DataBase):
    def __init__(self, db_data, main_table):
        super().__init__(db_data, main_table)

    def add_token(self, token):
        if self.main_table_length == None:
            self.main_table_length = (
                len(self.get_all_table_data(self.main_table)) + 1
                )
        else:
            self.main_table_length += 1

        self.cursor.execute(
            f"INSERT INTO {self.main_table} VALUES ('{token.coingecko_id}', '{token.ticker}', '{token.description}', '{token.exchanges}');"
        )
        self.connection.commit()

    def get_token(self, coingecko_id):
        self.cursor.execute(
            f"SELECT * FROM {self.main_table} WHERE coingecko_id = '{coingecko_id}';"
        )
        token_data = self.cursor.fetchall()
        if len(token_data) == 0:
            return None
        else:
            return token_data[0]    


# Initialize database
db_data = {'db_host': 'localhost', 'db_name': 'crypto', 'db_user': 'postgres', 'db_pass': 'password'}
database = DataBaseMod(db_data, 'token_data')


""" # Trial coin add
token = Token('bitcoin', 'btc', 'og token', 'literally everywhere')
database.add_token(token) """
