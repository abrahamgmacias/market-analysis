from pycoingecko import CoinGeckoAPI
from resources import *
import shutil

# User must have a db that fulfills the reqs 

# Initialize database
db_data = {'db_host': 'localhost', 'db_name': 'crypto', 'db_user': 'postgres', 'db_pass': 'password'}
coins_to_analyze = set(["ethereum", "bitcoin", "zelcash"])
excel_offload_file = 'market_analysis'
wallet_assets = {"ethereum": 24}
token_solver = True

# Main and wallet dataframes 
main_df = pd.DataFrame({'ticker': [], 'description': [], 'exchanges': [], 'current_price': [], 'market_cap': [], 'trading_volume': [], '24h': []})
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

        else:
            # Create existing token object
            token = Token(coingecko_id, ticker, description, exchanges)

            # And get the available data via the Coingecko API
            try:
                token.get_price(imarket_cap=True, i24hr_vol=True, i24hr_change=True)

            except KeyError:
                print(f"Couldn't find {coin}. Verify that it is an official coingecko id... \n")

            else:
                # Select token data in dataframe form
                currency = token.get_currency()
                token_df = token.get_data('ticker', 'description', 'exchanges', f'{currency}', f'{currency}_market_cap', f'{currency}_24h_vol', f'{currency}_24_change', dataframe=True)
                print(token_df)
                
