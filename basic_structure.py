from pycoingecko import CoinGeckoAPI
from resources import *
from solver import *
import shutil

# -------------------------------------------- NOTES -------------------------------------------- #
# User must have a db that fulfills the reqs 
# ----------------------------------------------------------------------------------------------- #


# ------------------------------------------- Algorithm ------------------------------------------ #
if token_solver == True:
    # Clean the Excel offload file
    if '.xlsx' in excel_offload_file:
        excel_offload_file = (lambda file_name: file_name.split('.'))(excel_offload_file)[0] 

    # Create an Excel file copy
    shutil.copyfile(f"{excel_offload_file}.xlsx", f"{excel_offload_file} - Copy.xlsx")

    # Initialize Database 
    db = DataBaseMod(db_data, 'token_data')

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
                # Maybe it could be a different error rather than coin id... 
                print(f"Couldn't find {coin}. Verify that it is an official coingecko id... \n")

            else:
                # Select token data in dataframe form
                currency = token.get_currency()
                token_df = token.get_data('ticker', 'description', 'exchanges', f'{currency}', f'{currency}_market_cap', f'{currency}_24h_vol', f'{currency}_24_change', dataframe=True)
                
                # Add token data to the corresponding tables
                main_table.add_line(token_df)

                # Add wallet assets to wallet dataframe
                if include_wallet == True:
                    if coin in wallet_assets:
                        equivalent_quantity = float(wallet_assets[coin]*token_df['usd'])
                        total_wallet_value += float(equivalent_quantity)
                        wallet_line = pd.DataFrame({'assets': [coin], 'quantity': [wallet_assets[coin]], 'equivalence': [equivalent_quantity], 'total_usd': [total_wallet_value]})
                        wallet_table.add_line(wallet_line)

                print(f"{coin} added...\n")

    # Create Excel file access / populate Excel sheet
    excel = Excelifier(f'{excel_offload_file}.xlsx', main_table, overwrite_sheets=True)

    # Add a wallet table to the Excel file
    if include_wallet == True:
        excel.add_new_table(wallet_table)

    # Move assets to sheet / save file
    excel.move_to_excel()
    excel.save_file()

    print('Table done. Check Excel...')

else:
    print('Enable token solver...')