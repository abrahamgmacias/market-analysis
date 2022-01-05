from pycoingecko import CoinGeckoAPI
from solver_data import *
import xlsxwriter
import shutil

# -------------------------------------------- NOTES -------------------------------------------- #
# Add initial excel creation if not provided
# Could you use a diff thread for each token?
# ----------------------------------------------------------------------------------------------- #


# ------------------------------------------- Algorithm ------------------------------------------ #
if file_data['switches']['token_solver'] == True:
    # Clean the Excel offload file
    if '.xlsx' in file_data['offload_file']:
        excel_offload_file = file_data['offload_file'].split('.')[0]        

    if file_data['switches']['file_copy'] == True:  
        # Create an Excel file copy
        shutil.copyfile(f"{excel_offload_file}.xlsx", f"{excel_offload_file} - Copy.xlsx")

    # Traverse through tokens of interest...
    wallet_set = set(file_data['wallet_data']['wallet_assets'].keys()) 
    for coin in (wallet_set & file_data['watchlist']).union(wallet_set.symmetric_difference(file_data['watchlist'])):
        print(f"Adding {coin}...")

        # Create token object
        token = Token(coin)

        # Get the data from Coingecko - Initial request to test if the API is working
        try:
            token_mcap = token.get_market_cap()

        except Exception:
            print(f"An error has occured. Verify that '{coin}' it is an official coingecko id... \n")

        else:
            # Select token data in dataframe form
            token_percentages = token.get_price_change('price_change_percentage_24h', 'price_change_percentage_7d', 'price_change_percentage_14d', 'price_change_percentage_30d')

            token_df = pd.DataFrame({'ticker': [token.get_ticker()], 
                                     'exchanges': [token.get_exchanges(as_text=True)], 
                                     'market_cap': [token.get_market_cap()],
                                     'current_price': [token.get_current_price()], 
                                     'trading_volume': [token.get_volume()], 
                                     '24h': [token_percentages['price_change_percentage_24h']],
                                     '7d': [token_percentages['price_change_percentage_7d']], 
                                     '14d': [token_percentages['price_change_percentage_14d']], 
                                     '30d': [token_percentages['price_change_percentage_30d']]})
                
            # Add token data to the main table
            file_data['main_table_data']['main_table'].add_line(token_df)

            # Add wallet assets to wallet dataframe
            if file_data['switches']['include_wallet'] == True:
                if coin in file_data['wallet_data']['wallet_assets']: 
                    current_quantity = float(file_data['wallet_data']['wallet_assets'][coin]*token_df['current_price'])
                    file_data['wallet_data']['wallet_balance'] += current_quantity
                    wallet_df = pd.DataFrame({'assets': [coin],
                                             'quantity': [file_data['wallet_data']['wallet_assets'][coin]],
                                             'equivalence': [current_quantity],
                                             'total_usd': [file_data['wallet_data']['wallet_balance']]})

                    file_data['wallet_data']['wallet_table'].add_line(wallet_df)

            print(f"{coin} added...\n")

    # Create Excel file access / populate Excel sheet
    excel = Excelifier(f'{excel_offload_file}.xlsx', file_data['main_table_data']['main_table'], overwrite_sheets=True)

    # Add a wallet table to the Excel file
    if file_data['switches']['include_wallet'] == True:
        excel.add_new_table(file_data['wallet_data']['wallet_table'])

    # Move assets to sheet / save file
    excel.move_to_excel()
    excel.save_file()

    print('Table done. Check Excel...')

else:
    print('Enable token solver...')