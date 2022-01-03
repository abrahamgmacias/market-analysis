from urllib.request import Request, urlopen
from pycoingecko import CoinGeckoAPI
from openpyxl import load_workbook
from urllib import request  
from datetime import date
from numpy import empty
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
        # Add token SQL function 
        self.cursor.execute(
            f"INSERT INTO {self.main_table} VALUES ('{token.coingecko_id}', '{token.ticker}', '{token.description}', '{token.get_exchanges(as_text=True)}');"
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
    def __init__(self, coingecko_id, ticker=None, description=None, exchanges=None):
        self.all_token_data = cg.get_coin_by_id(coingecko_id)
        self.market_data = self.all_token_data['market_data']

        # Main attributes
        self.coingecko_id = coingecko_id 
        self.ticker = ticker
        self.description = description
        self.exchanges = exchanges
        self.currency = 'usd'

    def set_currency(self, new_currency):
        self.currency = new_currency
    
    def set_ticker(self):
        self.ticker = self.all_token_data['symbol']

    def set_description(self, description):
        self.description = description

    def set_exchanges(self, num_exchanges):
        if num_exchanges < 1 or type(num_exchanges) != int:
            print(f"'{num_exchanges}' is not a valid input for num_exchanges.")
            return

        ticker_data = self.all_token_data['tickers']
        max_num_exchanges = len(ticker_data)

        if num_exchanges > max_num_exchanges:
            print(f"'{num_exchanges}' exceeds the amount of registered exchanges ({max_num_exchanges})")
            return

        self.exchanges = []
        for market in ticker_data:
            market_name = market['market']['name']

            if market_name not in self.exchanges:
                self.exchanges += [market_name]

            if len(self.exchanges) == num_exchanges:
                break

    def get_all_token_data(self):
        return self.all_token_data
    
    def get_market_data(self):
        return self.market_data

    def get_market_cap(self, vs_currency=None):
        if vs_currency == None:
            vs_currency = self.currency

        return self.market_data['market_cap'][vs_currency]

    def get_price_change(self, *args):
        price_change_attributes = ['price_change_percentage_24h', 'price_change_percentage_7d', 'price_change_percentage_14d', 'price_change_percentage_30d', 
                                   'price_change_percentage_60d', 'price_change_percentage_200d', 'price_change_percentage_1y']
        requested_data = {}

        if len(args) > 0:
            for arg in args:
                try:
                    requested_data[arg] = self.market_data[arg]
                except Exception:
                    print(f'{arg} is not a valid argument. ')

        else:  
            for attr in price_change_attributes:
                requested_data[attr] = self.market_data[attr]

        return requested_data

    def get_market_cap_rank(self):
        return self.market_data['market_cap_rank']

    def get_volume(self, vs_currency=None):
        if vs_currency == None:
            vs_currency = self.currency 

        return self.market_data['total_volume'][vs_currency]

    def get_current_price(self, vs_currency=None):
        if vs_currency == None:
            vs_currency = self.currency 

        return self.market_data['current_price']

    def get_exchanges(self, as_text=False):
        def textify(list):
            final_text, count = "", 1
            for elem in list:
                final_text += str(elem)
                if count != len(list):
                    final_text += " / "
                count += 1
                    
            return final_text

        if as_text == True:
            return textify(self.exchanges)
        else:
            return self.exchanges


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

    def move_to_excel(self, sheet_title=None):
        if sheet_title == None:
            title = date.today().strftime("%m-%d")

        for table in self.dfs.values():
            table.df.to_excel(self.writer, sheet_name=title, startrow=table.position_coordinates[0], startcol=table.position_coordinates[1], header=True, index=False)
            self.worksheet = self.writer.sheets[title]

    def get_tables(self):
        return self.dfs


class Table():
    def __init__(self, name, position_coordinates, structure=None):
        self.name = name
        self.position_coordinates = position_coordinates
        self.df = structure

    def get_table_data(self): 
        return self.__dict__

    def get_table(self):
        return self.df

    def add_line(self, line_to_add, enforce_structure=False):
        if enforce_structure == True:
            if self.df == None:
                print('Feed a structure attribute or add a line to the table class.')
            else:
                for column_1, column_2 in zip(self.df, line_to_add):
                    if column_1 != column_2:
                        print('Table structures differ - cannot add line.')
                        return 

        self.df = pd.concat([self.df, line_to_add])


class WalletTable(Table):
    def __init__(self, name, position_coordinates, structure=None):
        super().__init__(name, position_coordinates, structure)
        self.balance = 0

    def add_calc_line(self, asset, quantity, asset_price):
        equivalent_quantity = float(quantity*asset_price)
        self.balance += equivalent_quantity
        return pd.DataFrame({'assets': [asset], 'quantity': [quantity], 'equivalence': [equivalent_quantity], 'total_usd': [self.balance]})