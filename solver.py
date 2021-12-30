import pandas as pd
from resources import *

# Main and wallet dataframes 
wallet_df = pd.DataFrame({'assets': [], 'quantity': [], 'equivalence': [], 'total_usd': []})
# wallet_df = pd.DataFrame({'assets': [], 'quantity': [], 'equivalence': [], 'total_usd': [], 'total_mxn': []})
# main_df = pd.DataFrame({'ticker': [], 'description': [], 'exchanges': [], 'current_price': [], 'market_cap': [], 'trading_volume': [], '24h': []})

# Database data
db_data = {'db_host': 'localhost', 'db_name': 'crypto', 'db_user': 'postgres', 'db_pass': 'password'}

# Coin watchlist
coins_to_analyze = set(["ethereum", "bitcoin", "zelcash"])

# Main table
main_table = Table('main', (1, 1))

# Wallet
wallet_assets = {"ethereum": 24, 'bitcoin': 3}  
wallet_table = Table('wallet', (1, 13)) 
total_wallet_value = 0

# Offload file (Has to be Excel...)
excel_offload_file = 'market_analysis'

# Switches
token_solver = True
include_wallet = True
