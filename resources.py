from urllib import request
from urllib.request import Request, urlopen
from numpy import empty
from pycoingecko import CoinGeckoAPI
from openpyxl import load_workbook
from datetime import date
import pandas as pd
import psycopg2


class DataBase:
    def __init__(self, db_data, main_table):
        self.connection = self.feed_db_data(db_data)
        self.cursor = self.connection.cursor()
        self.main_table = main_table

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


class DataBaseMod(DataBase):
    def __init__(self, db_data, main_table):
        super().__init__(db_data, main_table)

    def add_token(self, token):
        # Access token data
        token_data = token.get_token_data()

        # Add token SQL function 
        self.cursor.execute(
            f"INSERT INTO {self.main_table} VALUES ('{token_data['id']}', '{token_data['ticker']}', '{token_data['description']}', '{token_data['exchanges']}');"
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


cg = CoinGeckoAPI()
class Token():
    def __init__(self, coingecko_id, ticker, description, exchanges):
        self.coingecko_id = coingecko_id
        self.description = description
        self.exchanges = exchanges
        self.ticker = ticker
        self.currency = 'usd'

    def set_currency(self, new_currency):
        self.currency = new_currency

    def get_price(self, imarket_cap=False, i24hr_vol=False, i24hr_change=False):
        # Try w/ diff currency
        self.req_token_data = cg.get_price(ids=self.coingecko_id, vs_currencies=self.currency, include_market_cap=imarket_cap, include_24hr_vol=i24hr_vol, include_24hr_change=i24hr_change)

    def get_data(self, *args, dataframe=False):
        try: 
            token_data = self.__dict__ | self.req_token_data[self.coingecko_id]
        except Exception:
            token_data = self.__dict__
        else:
            token_data.pop('req_token_data')

        if args is empty:
            requested_data = {}
            for arg in args:
                requested_data[arg] = token_data[arg]
        else:
            requested_data = token_data

        if dataframe == True:
            return pd.DataFrame([requested_data])
        return requested_data

    def get_currency(self):
        return self.currency


class Excelifier():
    def __init__(self, file_name, main_dataframe, overwrite_sheets=False):
        # Load or overwrite workbook
        if overwrite_sheets == False:
            self.book = load_workbook(file_name)
            self.writer = pd.ExcelWriter(file_name, engine='openpyxl')
            self.writer.book = self.book
            self.writer.sheets = dict((ws.title, ws) for ws in self.book.worksheets)
        else:
            self.writer = pd.ExcelWriter(file_name, engine='xlsxwriter')   

        # Create main data frame
        self.dfs = {'main': main_dataframe}

    def add_new_table(self, table_object):
        self.dfs[table_object.name] = table_object

    def save_file(self):
        self.writer.save()

    def move_to_excel(self, table=None, sheet_title=None):
        if sheet_title == None:
            title = date.today().strftime("%m-%d")

        for table in self.dfs.values():
            table.df.to_excel(self.writer, sheet_name=title, startrow=table.coordinates[0], startcol=table.coordinates[1], header=True, index=False)
            self.worksheet = self.writer.sheets[title]


class Table():
    def __init__(self, name, position_coordinates, structure=None):
        self.name = name
        self.position_coordinates = position_coordinates
        self.df = structure

    def get_table_data(self): 
        return self.__dict__

    def get_table(self):
        return self.df

    def add_line(self, line_to_add):
        self.df = pd.concat([self.df, line_to_add])