from pycoingecko import CoinGeckoAPI
import psycopg2

class DataBase:
    def __init__(self, db_data, main_table):
        self.connection = self.feed_db_data(db_data)
        self.cursor = self.connection.cursor()
        self.main_table = main_table
        self.main_table_length = None

    def feed_db_data(self, db_data):
        return psycopg2.connect(
            dbname=db_data['db_name'], user=db_data['db_user'], password=db_data['db_pass'], host=db_data['db_host']
        )

    def change_main_table(self, table_name):
        self.main_table = table_name

    def get_all_table_data(self, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name};")
        table_data = self.cursor.fetchall()
        return table_data

    def close_dbase(self):
        self.cursor.close()
        self.connection.close()

class Token():
    def __init__(self, coingecko_id, ticker, description, exchanges):
        self.coingecko_id = coingecko_id
        self.ticker = ticker
        self.description = description
        self.exchanges = exchanges
        self.cg = CoinGeckoAPI()
