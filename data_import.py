'''
This module imports stock price data
'''

# import libraries
import csv
import pandas as pd
import yfinance as yf
import requests
from datetime import datetime

# Define global variables
ticker_list = ['HMC', 'TKS']
period = '1d'
start = '2000-01-01'
end = str(datetime.now().date())
oil_url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=DCOILWTICO&scale=left&cosd=' + start + '&coed=' + end + '&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Daily&fam=avg&fgst=lin&fgsnd=2009-06-01&line_index=1&transformation=lin&vintage_date=2020-03-16&revision_date=2020-03-16&nd=1986-01-02'
ffr_url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=EFFR&scale=left&cosd=' + start + '&coed=' + end + '&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Daily&fam=avg&fgst=lin&fgsnd=2009-06-01&line_index=1&transformation=lin&vintage_date=2020-03-16&revision_date=2020-03-16&nd=2000-07-03'
interim_folder_path = 'interim_files/'
aux_col_lab = ['Oil_Price', 'FFR']

# Module 1
class Data:
	'''Loads input data'''
	def __init__(self, ticker_list, period, start, end, oil_url, ffr_url, interim_folder_path, aux_col_lab = aux_col_lab):
		# Initiate variables
		self.ticker_list, self.period, self.start, self.end, self.oil_url, self.ffr_url, self.aux_col_lab, self.interim_folder_path = ticker_list, period, start, end, oil_url, ffr_url, aux_col_lab, interim_folder_path
		self.head = None
		self.df_list = []
		self.df_main = pd.DataFrame()
		self.df_aux = pd.DataFrame()
		self.df = pd.DataFrame()

	def main_data_import(self):
		'''Load main data matrices'''
		[self.df_list.append(Aux.load_one_ticker(ticker, period, start, end)) for ticker in self.ticker_list]
		for i in range(len(self.df_list)):
			if i == 0:
				self.df_main = self.df_list[0].add_suffix('_' + self.ticker_list[i])
			else:
				self.df_main = self.df_main.join(self.df_list[i].add_suffix('_' + self.ticker_list[i]))

	def aux_data_import(self):
		self.df_aux = pd.merge(Aux.load_one_series(self.oil_url, self.aux_col_lab[0]), Aux.load_one_series(self.ffr_url, self.aux_col_lab[1]), how = 'inner', on = 'date')

	def merge_data(self):
		'''Merge the main and the aux data matrices together'''
		self.df = pd.merge(self.df_main, self.df_aux, left_index = True, right_index = True)

	def interim_data_export(self):
		'''Export the intermediary dataframe object (merged data) to csv'''
		self.df.to_csv(self.interim_folder_path + 'master_data.csv', index = 'date')

	def exec(self):
		self.main_data_import()
		self.aux_data_import()
		self.merge_data()
		self.interim_data_export()
		print(self.df.head())

# Module 2
class Aux:
	'''Auxiliary module to simplify the core code block'''
	def load_one_ticker(ticker, period, start, end):
		'''Return info about one ticker'''
		# Initiate pointer object
		head = None
		# Import data associated with a ticker
		head = yf.Ticker(ticker)
		# Obtain historical prices of a stock
		df = head.history(period = period, start = start, end = end)
		return df

	def load_one_series(url, column_name):
		'''Load one aux data matrix'''
		# Initiate variables
		row_list = []
		# Download the file and convert the file into a dataframe object
		with requests.get(url, stream = True) as buffer:
			lines = (line.decode('utf-8') for line in buffer.iter_lines())
			for row in csv.reader(lines):
				row_list.append(row)
			df_aux = pd.DataFrame(row_list[1:len(row_list)], columns = row_list[0])
			df_aux.set_index(row_list[0][0], inplace = True)
			df_aux.index.rename(row_list[0][0].lower(), inplace = True)
			df_aux.rename(columns = {df_aux.columns.tolist()[0]:column_name}, inplace = True)
		return df_aux

# Conditional execution lines
if __name__ == '__main__':
	obj = Data(ticker_list, period, start, end, oil_url, ffr_url, interim_folder_path, aux_col_lab)
	obj.exec()
