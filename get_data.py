from binance.client import Client
import requests
import json
import pandas as pd
import time
from CONFIG import *

client = Client(API_KEY, SECRET_KEY)

class get_data:

	def __init__(self, interval):
		self.interval = interval

	def get_symbols(self):
		info = client.futures_exchange_info()
		symbol_list_future = []
		symbol_list = []
		final_symbol_list = []
		symbol_list_text = SYMBOL_LIST_TEXT # some input already provided
		info = client.futures_exchange_info()
		all_info = client.get_exchange_info()
		for sym in info['symbols']:
			symbol_list_future.append(sym['symbol'])
		for sym in all_info['symbols']:
			if 'USDT' in sym['symbol']:
				symbol_list.append(sym['symbol'])
		for sym in symbol_list_future:
			if sym not in symbol_list:
				symbol_list.append(sym)
		for sym in symbol_list_text:
			if sym not in symbol_list:
				symbol_list.append(sym)
		for sym in symbol_list:
			if sym[-4 :] == 'USDT':
				final_symbol_list.append(sym)

		return(final_symbol_list) # getting unique symbols


	def get_volume_data(self, symbol_list):
		volume_dic = {}
		for symbol in symbol_list:
			volume_dic[symbol] = []
		for symbol in symbol_list:
			url = PRICE + 'symbol=' + symbol + '&interval=' + self.interval + '&limit=1'
			time.sleep(0.01)
			price = requests.get(url)
			price = json.loads(price.content)
			if type(price) == list and float(price[0][5])*float(price[0][4]) >= 100000000:
				volume_dic[symbol].append(float(price[0][5]))
				volume_dic[symbol].append(float(price[0][5])*float(price[0][4]))
			else:
				volume_dic.pop(symbol)	
		return(volume_dic)


	def get_oi_data(self, volume_dic):
		oi_dic = {}
		symbol_list = list(volume_dic.keys())
		for symbol in symbol_list:
			oi_dic[symbol] = 'a'
		for symbol in symbol_list: 
			url = OPEN_INTEREST + 'symbol='+ symbol +'&period=' + self.interval + '&limit=2'
			time.sleep(0.01)
			open_interest = requests.get(url)
			open_interest = json.loads(open_interest.content) # getting the data
			if len(open_interest) == 2:
				oi_dic[symbol] = float(open_interest[0]['sumOpenInterestValue'])
					 
			else: # if empty we remove symbol from the dictionary
				oi_dic.pop(symbol)
		return(oi_dic)


'''
data_obj = get_data('1d')
symbol_list = data_obj.get_symbols()
vol = data_obj.get_volume_data(symbol_list)

print(vol)
oi = data_obj.get_oi_data(symbol_list)
print('*'*100)
print(oi)
'''