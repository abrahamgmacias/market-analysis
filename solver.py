import pandas as pd
from resources import *

# Main and wallet dataframes 
wallet_df = pd.DataFrame({'assets': [], 'quantity': [], 'equivalence': [], 'total_usd': []})
main_df = pd.DataFrame({'ticker': [], 'description': [], 'exchanges': [], 'market_cap': [], 'current_price': [], 'trading_volume': [], '24h': [], '7d': [], '14d': [], '30d': []})

# Database data
db_data = {'db_host': 'localhost', 'db_name': 'crypto', 'db_user': 'postgres', 'db_pass': 'password'}

# Coin watchlist
coins_to_analyze = set(["ethereum", "bitcoin", "zelcash"])

# Main table
main_table = Table('main', (1, 1))

# Wallet
wallet_assets = {"ethereum": 24, 'bitcoin': 3}  
wallet_table = WalletTable('wallet', (1, 12), wallet_df)

# Offload file (Has to be Excel...)
excel_offload_file = 'market_analysis'

# Switches
token_solver = True
include_wallet = True
