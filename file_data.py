import pandas as pd
from resources import *

file_data = {   'watchlist':  set(["ethereum",
                                   "bitcoin",
                                   "zelcash"]),

                'main_table_data': {
                                    'main_table': Table('main', (1, 1)),
                                   },

                'wallet_data':  {
                                'wallet_table': Table('wallet', (1, 11)),
                                'wallet_balance': 0,
                                'wallet_assets': {
                                                  "ethereum": 24,
                                                  "bitcoin": 3
                                                 }
                                },

                'offload_file': 'market_analysis.xlsx',

                'switches': {
                             'token_solver': True,
                             'include_wallet': True,
                             'file_copy': False
                            }
}