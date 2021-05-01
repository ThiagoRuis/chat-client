import requests
import csv
from typing import Dict

def stock_info(stock_code:str) -> Dict:
    endpoint = f'https://stooq.com/q/l/?s={stock_code}&f=sd2t2ohlcv&h&e=csv'

    with requests.Session() as s:
        stock_file_str = s.get(endpoint).content.decode('utf-8')
        lines = stock_file_str.splitlines()
        stock_data = list(csv.DictReader(lines))
    
    return stock_data[0] #TODO: get the latest info if more lines come from endpoint
