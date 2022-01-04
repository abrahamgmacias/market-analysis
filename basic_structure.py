from pycoingecko import CoinGeckoAPI
from solver import *
import shutil

# -------------------------------------------- NOTES -------------------------------------------- #
# Add initial excel creation if not provided
# Could you use a diff thread for each token?
# ----------------------------------------------------------------------------------------------- #


# ------------------------------------------- Algorithm ------------------------------------------ #
if token_solver == True:
    # Clean the Excel offload file
    if '.xlsx' in excel_offload_file:
        excel_offload_file = excel_offload_file.split('.')[0]        

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
            # Gather token data / create token object / add it to the DB
            description = input('Description: ')
            token = Token(coin, description=description)
            db.add_token(token)

        else:
            # Create existing token object
            token = Token(coingecko_id, ticker, description, exchanges)

        # Get the data from Coingecko - Initial request to test if the API is working
        try:
            token_mcap = token.get_market_cap()

        except Exception:
            print(f"An error has occured. Verify that '{coin}' it is an official coingecko id... \n")

        else:
            # Select token data in dataframe form
            token_percentages = token.get_price_change('price_change_percentage_24h', 'price_change_percentage_7d', 'price_change_percentage_14d', 'price_change_percentage_30d')

            token_df = pd.DataFrame({'ticker': [token.ticker], 
                                     'description': [token.description], 
                                     'exchanges': [token.exchanges], 
                                     'market_cap': [token.get_market_cap()],
                                     'current_price': [token.get_current_price()], 
                                     'trading_volume': [token.get_volume()], 
                                     '24h': [token_percentages['price_change_percentage_24h']],
                                     '7d': [token_percentages['price_change_percentage_7d']], 
                                     '14d': [token_percentages['price_change_percentage_14d']], 
                                     '30d': [token_percentages['price_change_percentage_30d']]})
                
            # Add token data to the corresponding tables
            main_table.add_line(token_df)

            # Add wallet assets to wallet dataframe
            if include_wallet == True:
                if coin in wallet_assets:
                    current_quantity = float(wallet_assets[coin]*token_df['current_price'])
                    wallet_balance += current_quantity
                    wallet_df = pd.DataFrame({'assets': [coin],
                                             'quantity': [wallet_assets[coin]],
                                             'equivalence': [current_quantity],
                                             'total_usd': [wallet_balance]})

                    wallet_table.add_line(wallet_df)

            print(f"{coin} added...\n")

    # Create Excel file access / populate Excel sheet
    excel = Excelifier(f'{excel_offload_file}.xlsx', main_table, overwrite_sheets=False)

    # Add a wallet table to the Excel file
    if include_wallet == True:
        excel.add_new_table(wallet_table)

    # Move assets to sheet / save file
    excel.move_to_excel()
    excel.save_file()

    print('Table done. Check Excel...')

else:
    print('Enable token solver...')