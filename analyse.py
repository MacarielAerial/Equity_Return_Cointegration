'''
This script analyses imported data with linear model, cointergration, AR + GARCH (1, 1) and regime switching
'''

# Import libraries
import pandas as pd
import numpy as np
from data_import import Data
from datetime import datetime
import matplotlib.pyplot as plt
import statsmodels.tsa.api as smt
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from arch import arch_model

# Configurations
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Define global variables
ticker_list = ['HMC', 'TKS']
period = '1d'
start = '2000-01-01'
end = str(datetime.now().date())
oil_url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=DCOILWTICO&scale=left&cosd=' + start + '&coed=' + end + '&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Daily&fam=avg&fgst=lin&fgsnd=2009-06-01&line_index=1&transformation=lin&vintage_date=2020-03-16&revision_date=2020-03-16&nd=1986-01-02'
ffr_url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=EFFR&scale=left&cosd=' + start + '&coed=' + end + '&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Daily&fam=avg&fgst=lin&fgsnd=2009-06-01&line_index=1&transformation=lin&vintage_date=2020-03-16&revision_date=2020-03-16&nd=2000-07-03'
interim_folder_path = 'interim_files/'
aux_col_lab = ['Oil_Price', 'FFR']
target = 'Close_HMC'
features = ['Volume_HMC', 'Close_TKS', 'Volume_TKS', 'Oil_Price', 'FFR']

class Analysis:
	def __init__(self, input_data, target, features, split = 0.8):
		self.input_data, self.target, self.features, self.split = input_data, target, features, split
		self.df = self.input_data.dropna()
		self.linear_model = None
		self.linear_result = None
		self.X_train = pd.DataFrame()
		self.y_train = pd.DataFrame()
		self.X_test = pd.DataFrame()
		self.y_test = pd.DataFrame()

	def data_preprocess(self):
		'''Feature engineering prepared for parametric statistical models'''
		self.df[target] = self.df[target].pct_change()
		self.df = self.df.iloc[1:, :]
		X, y = self.df[features], self.df[target]
		self.X_train, self.X_test, self.y_train, self.y_test = X[:int(X.shape[0]*self.split)].astype(float), X[int(X.shape[0]*self.split):].astype(float), y[:int(X.shape[0]*self.split)].astype(float), y[int(X.shape[0]*self.split):]

	def linear_regression(self):
		'''Construct a linear model on Honda Motor's volatility'''
		self.X_train = sm.add_constant(self.X_train)
		self.X_test = sm.add_constant(self.X_test)
		self.linear_model = sm.OLS(self.y_train, self.X_train)
		self.linear_result = self.linear_model.fit()
		print(self.linear_result.summary())
		y_test_hat = self.linear_result.predict(self.X_test)
		fig, ax = plt.subplots(figsize = (16, 9))
		ax.plot(self.y_test.index, self.y_test, 'o', label = 'Data')
		ax.plot(self.y_test.index, y_test_hat, 'r', label = 'OLS Prediction')
		ax.set_title('OLS Model Prediction of HMC Stock Return')
		ax.set_xlabel('Date')
		ax.set_ylabel('Stock Return in %')
		ax.legend(loc = 'best')
		plt.savefig('Linear_Model_Result.png', dpi = 300)

	def exec(self):
		self.data_preprocess()
		self.linear_regression()





if __name__ == '__main__':
	obj = Data(ticker_list, period, start, end, oil_url, ffr_url, interim_folder_path, aux_col_lab)
	obj.exec()
	obj_2 = Analysis(obj.df, target, features)
	obj_2.exec()
