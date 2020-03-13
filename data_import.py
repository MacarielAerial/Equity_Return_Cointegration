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
ticker_list = ['TSLA', 'PCRFY', 'F']
period = '1d'
start = '2012-1-1'
end = datetime.now().date()
url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=DCOILWTICO&scale=left&cosd=2012-01-01&coed=2020-03-06&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Daily&fam=avg&fgst=lin&fgsnd=2009-06-01&line_index=1&transformation=lin&vintage_date=2020-03-13&revision_date=2020-03-13&nd=1986-01-02'

# Module 1
class Data:
	'''Loads input data'''
	def __init__(self, ticker_list, period, start, end, url, aux_col_lab = 'Oil_Price'):
		# Initiate variables
		self.ticker_list, self.period, self.start, self.end, self.url, self.aux_col_lab = ticker_list, period, start, end, url, aux_col_lab
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
		'''Load aux data matrices'''
		# Initiate variables
		row_list = []
		# Download the file and convert the file into a dataframe object
		with requests.get(self.url, stream = True) as buffer:
			lines = (line.decode('utf-8') for line in buffer.iter_lines())
			for row in csv.reader(lines):
				row_list.append(row)
			self.df_aux = pd.DataFrame(row_list[1:len(row_list)], columns = row_list[0])
			self.df_aux.set_index(row_list[0][0], inplace = True)
			self.df_aux.index.rename(row_list[0][0].lower(), inplace = True)
			self.df_aux.rename(columns = {self.df_aux.columns.tolist()[0]:self.aux_col_lab}, inplace = True)

	def merge_data(self):
		'''Merge the main and the aux data matrices together'''
		self.df = pd.merge(self.df_main, self.df_aux, left_index = True, right_index = True)

	def exec(self):
		self.main_data_import()
		self.aux_data_import()
		self.merge_data()

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

# Conditional execution lines
if __name__ == '__main__':
	obj = Data(ticker_list, period, start, end, url)
	obj.exec()
