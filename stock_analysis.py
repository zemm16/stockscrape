import pandas as pd
import numpy
import datetime
from lxml import html
import requests
from time import sleep
import json
import argparse
from random import randint
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def make_float(num): num = num.replace(u'\N{MINUS SIGN}', '-') 


# Clean up Dataframe module (look into lambda function). Input? Dataframe column. Output dataframe column
def clean_column(stocks_df, df_column_list):
    """Take out - and replace with N/A. Repalce 'N/A with 0 when not a string. Take out commas so we can turn values 
    into float values'"""
    for i in df_column_list:
        stocks_df[i] = stocks_df[i].astype(str).apply(lambda x: (x.replace('-','N/A')))
        if i == "Long Term Det":
            print(stocks_df[i])
        
        stocks_df[i] = stocks_df[i].replace('N/A', 0)
        stocks_df[i] = stocks_df[i].astype(str).apply(lambda x: float(x.replace(',','')))
        stocks_df[i] = stocks_df[i].astype(float)
    return stocks_df

def clean_negative_value(stocks_df, df_column_list):
    """Take out percentages and commas so we can turn values into floats. There is a character error for - so we need 
    to account for that. Replace N/A with 0 and change values to floats."""
    for i in df_column_list:
        stocks_df[i] = stocks_df[i].astype(str).replace('%','')
        stocks_df[i] = stocks_df[i].astype(str).apply(lambda x: (x.replace(',','')))
        stocks_df[i] = stocks_df[i].astype(str).apply(lambda x:  x.replace('-', '-') if len(x)>1else x.replace('-', 'N/A'))
        stocks_df[i] = stocks_df[i].replace('N/A', 0)
        stocks_df[i] = stocks_df[i].astype(float)
    return stocks_df
    #return df_column.astype(float)

def clean_money_column(stocks_df, df_column_list):
    """Take out periods and convert to millions and billions so we can convert these values to floats"""
    for i in df_column_list:
        stocks_df[i] = stocks_df[i].astype(str).apply(lambda x: (x.replace('.','')))
        stocks_df[i] = stocks_df[i].astype(str).apply(lambda x: (x.replace('M','000')))
        stocks_df[i] = stocks_df[i].astype(str).apply(lambda x: (x.replace('B','000000')))
    return stocks_df


def growth(stocks_df, net_income_applicable, dividends, depreciation, stockholder_equity, long_term_debt):
    """calculate growth of stocks: (net_income - total_dividends - depreciation)/(stockholder_equity + long_term_debt)"""
    stocks_df['Growth'] = (stocks_df[net_income_applicable] + stocks_df[dividends] - stocks_df[depreciation])\
    /(stocks_df[stockholder_equity] + stocks_df[long_term_debt].astype(float))
    
    return stocks_df



def dividend_five(stocks_df, average_dividend_yield):
    """There has been a Dividend for 5 Years"""
    return stocks_df[stocks_df[average_dividend_yield].notnull()]
    


    
def PE_filter(stocks_df, trailing_PE):
    """Filter trailing PE ratio to be less than 25"""
    stocks_df[trailing_PE] = stocks_df[trailing_PE].astype(str).apply(lambda x: float(x.replace(',','')))
    return stocks_df[stocks_df[trailing_PE].replace('N/A', numpy.nan).astype(float) <= 25.0]
    

def price_book(stocks_df, price_book_ratio):
    """Filter price/book ratio to be under or equal to 4 """
    return stocks_df[stocks_df[price_book_ratio].replace('N/A', numpy.nan).astype(float) <= 4]
    

def price_sales(stocks_df, price_sales_ratio):
    """Filter price/sales ratio to be under or equal to 3"""
    return stocks_df[stocks_df[price_sales_ratio].replace('N/A', numpy.nan).astype(float) <= 3]

def current_ratio(stocks_df, current_ratio):
    """Filter current ratio to be greater than 1.5"""
    return stocks_df[stocks_df[current_ratio].replace('N/A', numpy.nan).astype(float) >= 1.5]


def debt_filter(stocks_df, long_term_debt, total_current_assets):
    """debt compared to total current assets greater than 110%"""
    stocks_df['debt ratio'] = stocks_df[long_term_debt].astype(float)/stocks_df[total_current_assets].astype(float)
    return stocks_df[~(stocks_df['debt ratio'] > 1.1)]


def return_assets(stocks_df, return_on_assets):
    """return on assets greater than 5%"""
    stocks_df[return_on_assets] = stocks_df[return_on_assets].astype(str).apply(lambda x: float(x.replace('%','')))
    return stocks_df[stocks_df[return_on_assets] > 5]


def return_equity(stocks_df, return_on_equity):
    """return on equity greater than 15%"""
    stocks_df[return_on_equity] = stocks_df[return_on_equity].astype(str).apply(lambda x: float(x.replace('%','')))
    return stocks_df[stocks_df[return_on_equity] > 15]

def price_filter(stocks_df, price):
    """filter stocks where price is above $1"""
    return stocks_df[stocks_df[price]>1.0]

def analysis():
	#"Everything Combined!"

	stocks_df = pd.read_csv('stocks' + str(datetime.date.today()) + '.csv', index_col = 0,encoding='utf8')
	history_df = pd.read_csv('history' + str(datetime.date.today()) + '.csv', index_col = 0, encoding='utf8')
	stocks_clean = ['Market Cap', 'Long Term Debt', 'Total Current Assets']
	stocks_negative_clean = ['Dividends Paid', 'Total Stockholder Equity', 'Depreciation', 'Net Income Applicable To Common Shares']
	stocks_money_clean = ['Market Cap']

	clean_money_df = clean_money_column(stocks_df, stocks_money_clean)
	clean_column_df = clean_column(clean_money_df, stocks_clean)
	clean_negatives_df = clean_negative_value(clean_column_df, stocks_negative_clean )

	growth_df = growth(clean_negatives_df, 'Net Income Applicable To Common Shares','Dividends Paid', 'Depreciation', 'Total Stockholder Equity',
                 'Long Term Debt')
	dividends_df = dividend_five(growth_df, '5 Year Average Dividend Yield 4')
	PE_df = PE_filter(dividends_df, trailing_PE ='Trailing P/E ')
	price_book_df = price_book(PE_df, 'Price/Book (mrq)')
	price_sales_df = price_sales(price_book_df,'Price/Sales (ttm)')
	current_ratio_df = current_ratio(price_sales_df,'Current Ratio (mrq)' )
	debt_df = debt_filter(current_ratio_df,'Long Term Debt','Total Current Assets')
	assets_df = return_assets(debt_df, 'Return on Assets (ttm)')
	equity_df = return_equity(assets_df, 'Return on Equity (ttm)')
	stocks_filtered_df = price_filter(equity_df, 'Price')


	stocks_filtered_df.to_csv('stocks_filtered' + str(datetime.date.today()) + '.csv')
	history_df.to_csv('stock_history' + str(datetime.date.today()) + '.csv')


