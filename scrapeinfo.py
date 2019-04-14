from lxml import html
import requests
import sys
import time
import json
import argparse
from random import randint
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd
import pandas_datareader as web
import datetime
import helpers
import stock_analysis

## Methods to use in main

def extract_tickers(base_url,first_url):
    """extract NASDAQ ticker values from marketvolume.com"""
    symbols = []
    names = []
    urls = []
    url = first_url
    while url not in urls:
        headers = {
        "Host":"www.marketvolume.com",
        "Referer":"https://www.marketvolume.com",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"
          }
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        html = list(soup.children)[1]
        body = list(html.children)[1]
        table = list(body.children)[5]
        for tr in table.find_all('tr'):
            tds = tr.find_all('td')
            symbols.append(tds[0].text)
            names.append(tds[1].text)
        for a in table.find_all('a',class_='b', href=True):
            extra_url = a['href']
        urls.append(url)
        url = base_url + extra_url
    symbols.pop(0)
    names.pop(0)
    return symbols, names


def extract_info(table, metric_dict,counter):
    for tr in table.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) > 1:
            if tds[1].text:
                if tds[0].text in metric_dict.keys():
                    metric_dict[tds[0].text].append(tds[1].text)
                    
               
    for key in metric_dict:
            if len(metric_dict[key]) != counter+1 :
                    metric_dict[key].append(None)  
                    

def extract_eps(table, eps1,eps2,eps3,eps4, counter):
    for tr in table.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) != 0:
            if tds[0].text == 'EPS Actual':
                eps1.append(tds[1].text)
                eps2.append(tds[2].text)
                eps3.append(tds[3].text)
                eps4.append(tds[4].text)
    if len(eps1) != counter + 1:
            eps1.append(None)
    if len(eps2) != counter + 1:
            eps2.append(None)
    if len(eps3) != counter + 1:
            eps3.append(None)
    if len(eps4) != counter + 1:
            eps4.append(None)


def profile_loop(table, ceo, ceo_pay, pres, pres_pay, counter):
    counter_ceo = 0
    counter_pres = 0
    for tr in table.find_all('tr'):
        tds = tr.find_all('td')
      
        if len(tds) > 1:
            if  "CEO" in tds[1].text and counter_ceo == 0:
                
                ceo.append(tds[0].text)
                ceo_pay.append(tds[2].text)
                counter_ceo+=1
            if "Pres" in tds[1].text and counter_pres == 0:
                pres.append(tds[0].text)
                pres_pay.append(tds[2].text)
                counter_pres+=1
    if len(ceo) < counter + 1:
        ceo.append(None)
        ceo_pay.append(None)
    if len(pres) < counter+ 1:
        pres.append(None)
        pres_pay.append(None)
    return ceo, ceo_pay, pres, pres_pay


def extract_history(symbol,history_df,counter,eps1, recent_price ):
    end = datetime.date.today()
    start = end - datetime.timedelta(days=5*365)
    f_df = web.DataReader(symbol, 'iex',start,end)
    f_df['symbol'] = symbol
    if len(eps1) == counter + 1:
        recent_price.append(f_df['close'].iloc[-1])
    elif len(recent_price) < counter+1:
    	recent_price.append(None)
    return history_df.append(f_df), recent_price  


def extract_page_info(url_dict, symbol):
    table_dict = {}
    for i in url_dict.keys():
        actual_url = url_dict[i] % (symbol, symbol)
        page = requests.get(actual_url, verify= False)
        soup = BeautifulSoup(page.content, 'html.parser')
        html = list(soup.children)[1]
        body = list(html.children)[1]
        table_dict[i] = list(body.children)[0]
    return table_dict
    
def extract_profile_info(profile_table, industry, ceo, ceo_pay, pres, pres_pay, counter):
    industry = extract_industry(profile_table,industry, counter)
    ceo, ceo_pay, pres, pres_pay = profile_loop(profile_table, ceo, ceo_pay, \
    	pres, pres_pay, counter) 


def extract_industry(profile_table, industry, counter):
    span_before = ''
  
    for span in profile_table.find_all('span'):
        if span_before == 'Industry':
            industry.append(span.text)
        span_before = span.text
    if len(industry) < counter+1:
        industry.append(None)


def main_webscrape(symbols_sample, names_sample):
    recent_price, eps1, eps2, eps3, eps4, industry, pres, pres_pay, ceo,\
    ceo_born, ceo_pay, history_df, metric_summary, metric_income, metric_balance,\
    metric_statistics, metric_cash, url_dict = helpers.define_metrics()
    counter = 0
    start = time.time()
    current_date = str(int(time.time()))
    for symbol in symbols_sample:
    	try:
	        table_dict = extract_page_info(url_dict, symbol)
	        extract_profile_info(table_dict['profile'], industry, ceo, ceo_pay, pres, pres_pay, counter)
	        extract_info(table_dict['summary'], metric_summary,counter)
	        extract_info(table_dict['stat'], metric_statistics,counter)
	        extract_info(table_dict['income'], metric_income,counter)
	        extract_info(table_dict['balance'], metric_balance, counter)
	        extract_eps(table_dict['analysis'], eps1,eps2,eps3,eps4, counter)
	        history_df,recent_price = extract_history(symbol,history_df,counter,eps1, recent_price)
	        extract_info(table_dict['cash'], metric_cash, counter)
	        counter+=1
	        print('stock: ' + symbol)
	        print('stocks analyzed: ' + str(counter))
	        print(len(recent_price))
	        print(len(metric_summary['Market Cap']))
	        print(len(metric_statistics['Price/Sales (ttm)']))
	        print(len(ceo_pay))
	        print(len(pres))
	        print(len(eps1))
	        print(len(industry))
	        print(len(metric_balance['Long Term Debt']))
	        print(len(metric_income['Non Recurring']))
    	except:
        	print("skipping stock")
        	symbols_sample.remove(symbol)
        	names_sample.pop(counter-1)
        	recent_price.append(None)
        	print("The new recent_price:")
        	print(len(recent_price))
        	counter+=1


    stocks_intro = {'name': names_sample,'ticker':symbols_sample,'industry':industry, 'ceo': ceo, 'ceo pay':ceo_pay,
              'president':pres, 'pres_pay':pres_pay, 'EPS Present Year': eps1, 'EPS Last Year':eps2, 
                'EPS 2 Years Prior': eps3, 'EPS 3 Years Prior':eps4, 'Price':recent_price}
    stocks_dict = {**stocks_intro, **metric_summary, **metric_statistics, **metric_income, **metric_balance, **metric_cash}
    stocks_df = pd.DataFrame.from_dict(stocks_dict)
    stocks_df.to_csv('stocks' + str(datetime.date.today()) + '.csv')
    history_df.to_csv('history' + str(datetime.date.today()) + '.csv')

    end = time.time()
    print("My program took " + str(end - start) + "to run")
    return stocks_df, history_df



first_page = "https://www.marketvolume.com/indexes_exchanges/nasdaq_components.asp" 
root_url = "https://www.marketvolume.com"

recent_price, eps1, eps2, eps3, eps4, industry, pres, pres_pay, ceo,\
ceo_born, ceo_pay, history_df, metric_summary, metric_income, metric_balance,\
metric_statistics, metric_cash, url_dict = helpers.define_metrics()

symbols, names = extract_tickers(root_url, first_page)


if len(sys.argv) > 1:
	symbols_sample = symbols[0:int(sys.argv[1])]
	names_sample = names[0:int(sys.argv[1])]
else:
	symbols_sample = symbols
	names_sample = names

stocks_df, history_df = main_webscrape(symbols_sample, names_sample)
stock_analysis.analysis()
