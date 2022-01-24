from get_data import get_data
import pandas as pd
import plotly.express as px
import streamlit as st 
import pandas as pd
from CONFIG import *

# filter vol minimum 100 milion binance 10 milion for ftx


st.set_page_config(page_title = 'Assets with OI VOL Ratio and VOL Filter', layout = 'wide')
limit = st.sidebar.text_input('Enter How Many Top Assets You Want to Get(please enter some interger value!!!)')
button = st.sidebar.button('Click the button to get the Required Plot')

if button and limit != '':
	limit = int(limit)
	data_object = get_data('1d')
	symbol_list = data_object.get_symbols()
	vol_dict = data_object.get_volume_data(symbol_list)
	oi_dict = data_object.get_oi_data(vol_dict)
	oi_vol_ratio_dict = {}
	for key in symbol_list:
		if key in vol_dict.keys() and key in oi_dict.keys():
			oi_vol_ratio_dict[key] = 0
	for key in oi_vol_ratio_dict.keys():
		try:
			ratio = oi_dict[key]/vol_dict[key][1]
			oi_vol_ratio_dict[key] = ratio
		except ZeroDivisionError as e:
			oi_vol_ratio_dict.pop(key)
	oi_vol_df = pd.DataFrame({'Symbol': oi_vol_ratio_dict.keys(), 'Value': oi_vol_ratio_dict.values()})
	vol_df = pd.DataFrame({'Symbol': vol_dict.keys(), 'Value': vol_dict.values()})
	oi_vol_df.sort_values('Value', axis = 0, ascending = False, inplace = True)
	vol_df.sort_values('Value', axis = 0, ascending = False, inplace = True)
	vol_sym_list = []
	vol_list = []
	oi_vol_sym_list = []
	oi_vol_list = []
	for sym in oi_vol_df['Symbol']:
		oi_vol_sym_list.append(sym)
	for vol in oi_vol_df['Value']:
		oi_vol_list.append(vol)
	for sym in vol_df['Symbol']:
		vol_sym_list.append(sym)
	for val in vol_df['Value']:
		vol_list.append(val[0])
	final_limit = min(limit, len(oi_vol_list), len(vol_list))
	rank_list = [i+1 for i in range(final_limit)]
	final_df = pd.DataFrame({'Rank': rank_list, 'OI/VOL Symbol': oi_vol_sym_list[:final_limit], 'OI/VOL Ratio':oi_vol_list[:final_limit], 'Vol Symbol': vol_sym_list[:final_limit], 'Volume': vol_list[:final_limit]})
	fig = px.scatter(final_df, x = 'OI/VOL Ratio', y = 'Vol Symbol', size = 'OI/VOL Ratio', color = 'OI/VOL Symbol', hover_data = ['Rank', 'Volume'], size_max = 90)
	fig.update_yaxes(title_text = 'Retail Fomo')
	fig.update_xaxes(title_text = 'Whale accumulation')
	fig.update_layout(title = 'OI VOL RATIO with VOL RANK', width = 1200, height = 600, template='plotly_dark')
	st.plotly_chart(fig)
	st.download_button('Click Here to Download the Plot', fig.to_html(), 'OI VOL RATIO with VOL RANK' + '.html')
else:
	st.write('Click on the Button on the Sidebar to Get Your Required Plot')
