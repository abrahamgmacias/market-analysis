from pycoingecko import CoinGeckoAPI
from resources import *
import shutil


# Initialize database
db_data = {'db_host': 'localhost', 'db_name': 'crypto', 'db_user': 'postgres', 'db_pass': 'password'}
coins_to_analyze = set(["ethereum", "bitcoin", "zelcash"])
excel_offload_file = 'market_analysis'
wallet_assets = {"ethereum": 24}
token_solver = True

# Main and wallet dataframes 
main_df = pd.DataFrame({'ticker': [], 'description': [], 'exchanges': [], 'current_price': [], 'market_cap': [],
                        'trading_volume': [], '1h': [], '24h': [], '7d': [], '14d': [], '30d': []})
wallet_df = pd.DataFrame({'assets': [], 'quantity': [], 'equivalence': [], 'total_usd': [], 'total_mxn': []})

# Solver
if token_solver == True:
    # Clean the Excel offload file
    if '.xlsx' in excel_offload_file:
        excel_offload_file = (lambda file_name: file_name.split('.'))(excel_offload_file)[0] 

    # Create an Excel file copy
    shutil.copyfile(f"{excel_offload_file}.xlsx", f"{excel_offload_file} - Copy.xlsx")

    # Initialize Database 
    db = DataBaseMod(db_data, 'token_data')

    # Create summary and wallet tables
    main_table = Table('main', main_df, (1, 1))
    wallet_table = Table('wallet', wallet_df, (1, 13)) 

    # Traverse through tokens of interest...
    wallet_set = set(wallet_assets.keys())
    for coin in (wallet_set & coins_to_analyze).union(wallet_set.symmetric_difference(coins_to_analyze)):
        print(f"Adding {coin}...")

        # Check if coin exists in DB
        try:
            coingecko_id, ticker, description, exchanges = db.get_token(coin)

        except Exception:
            def token_data_gatherer():
                ticker = input('Ticker: ')
                description = input('Description: ')
                exchanges = input('Exchanges: ')
                print('')
                return ticker, description, exchanges

            # Gather token data / create token object / add it to the DB
            ticker, description, exchanges = token_data_gatherer()
            token = Token(coin, ticker, description, exchanges)
            db.add_token(token)






















    #     else:
    #         # Create existing token object
    #         token = Token(coingecko_id, ticker, description, exchanges)

    #     # Check if coingecko allows webdriver to navigate
    #     try: 
    #         token.set_bot_status()

    #     except Exception:
    #         print('ABORTED: Website recognizes user as script. Website may be crowded... \n')
    #         break
        
    #     else:
    #         # Scrape data from coingecko.com
    #         try: 
    #             token.scrape_data()

    #         except Exception:
    #             print(f"Couldn't find {coin}. Verify that it is an official coingecko id... \n")

    #         else:
    #             # Select token data in dataframe form
    #             token_df = token.get_data('ticker', 'description', 'exchanges', 'current_price', 'market_cap', 'trading_volume', '1h', '24h', '7d', '14d', '30d', dataframe=True)

    #             # Add token data to the corresponding tables
    #             main_table.add_line(token_df)

    #             print(f"{coin} added...\n")

    # # Create Excel file access / populate Excel sheet
    # excel = Excelifier(f'{file}.xlsx', main_table, overwrite_sheets=True)
    # # excel.add_new_table(wallet_table)

    # # Move assets to sheet / save file
    # excel.move_to_excel()
    # excel.save_file()

    # print('Table done. Check Excel...')
