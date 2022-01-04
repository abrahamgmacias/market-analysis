import pandas as pd
from resources import *

# Coin watchlist
coins_to_analyze = set(["ethereum", "bitcoin", "zelcash", "sentinel", "sienna", "dao-maker"])

# Main table
main_table = Table('main', (1, 1))

# Wallet
wallet_balance = 0
wallet_table = Table('wallet', (1, 12))
wallet_assets = {"ethereum": 24, 'bitcoin': 3}  

# Offload file (Has to be Excel...)
excel_offload_file = 'market_analysis.xlsx'

# Switches
token_solver = True
include_wallet = True
