'''
This module imports Tesla stock price data
'''

# import libraries
import pandas as pd
import yfinance as yf

# Define global variables
ticker = 'TSLA'
period = '1d'
start = '2012-1-1'
end = '2020-3-9'

class Data:
	'''Loads input data'''
	def __init__(self, ticker, period, start, end):
		# Initiate variables
		self.ticker, self.period, self.start, self.end = ticker, period, start, end	
		self.head = None
		self.df_p = pd.DataFrame()

	def data_import(self):
		# Import data associated with a ticker
		self.head = yf.Ticker(self.ticker)
		# Obtain historical prices of a stock
		self.df_p = self.head.history(period = period, start = start, end = end)

	def exec(self):
		self.data_import()
		print(self.df_p)

if __name__ == '__main__':
	obj = Data(ticker, period, start, end)
	obj.exec()
