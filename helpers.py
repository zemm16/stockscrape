#Define all variables. Is there a better way to do this?
def define_metrics():
    industry = []
    market_cap = []
    P_E = []
    current_assets = []
    current_liabilities = []
    long_term_debt = []
    net_tangible_assets = []
    stakeholders_equity = []
    accumlated_amortization = []
    price_sales = []
    price_book = []
    fifty_day_ma = []
    two_hundred_ma = []
    profit_margin = []
    return_assets = []
    return_equity = []
    revenue = []
    revenue_share = []
    gross_profit = []
    total_debt = []
    total_cash = []
    total_cash_per_share = []
    current_ratio = []
    book_value_share = []
    operating_cash_flow = []
    percent_held_insiders = []
    trailing_annual_dividend_rate = [] 
    trailing_annual_dividend_yield = []
    five_year_dividend_yield = []
    payout_ratio = []
    ceo = []
    ceo_pay = []
    ceo_born = []
    pres = []
    pres_pay = []
    pre_born = []
    research_development = []
    gross_profit = []
    non_recurring = []
    net_income_applic_shares = []
    depreciation = []
    net_income = []
    dividends_paid = []
    accumulated_amortization = []
    date = []
    close_price = []
    volume = []
    history_symbol = []
    eps1 = []
    eps2 = []
    eps3 = []
    eps4 = []
    recent_price = []
    history_df = pd.DataFrame()
    metric_summary = {'Market Cap': market_cap}
    metric_income = {'Research Development':research_development, 
                           'Non Recurring': non_recurring,
                     'Net Income Applicable To Common Shares':net_income_applic_shares}

    metric_balance = {'Total Current Assets':current_assets,'Total Current Liabilities':current_liabilities,
                           'Long Term Debt':long_term_debt,'Net Tangible Assets':net_tangible_assets,
                          'Total Stockholder Equity':stakeholders_equity,
                           'Accumulated Amortization':accumulated_amortization }
    metric_cash = {'Depreciation':depreciation,'Net Income':net_income,'Dividends Paid':dividends_paid}

    metric_statistics = {'Trailing P/E ':P_E,'Price/Sales (ttm)':price_sales,'Price/Book (mrq)':price_book,
                           '50-Day Moving Average 3': fifty_day_ma, '200-Day Moving Average 3':two_hundred_ma, 
                            'Profit Margin ':profit_margin,'Return on Assets (ttm)':return_assets,
                             'Return on Equity (ttm)': return_equity,'Revenue (ttm)':revenue,
                             'Revenue Per Share (ttm)':revenue_share, 'Gross Profit (ttm)':gross_profit,
                            'Total Debt (mrq)':total_debt,'Total Cash (mrq)':total_cash,
                            'Total Cash Per Share (mrq)':total_cash_per_share, 'Current Ratio (mrq)':current_ratio,
                           'Book Value Per Share (mrq)':book_value_share,'Operating Cash Flow (ttm)':operating_cash_flow,
                            '% Held by Insiders 1':percent_held_insiders,
                             'Trailing Annual Dividend Rate 3':trailing_annual_dividend_rate,
                             'Trailing Annual Dividend Yield 3':trailing_annual_dividend_yield,
                             '5 Year Average Dividend Yield 4': five_year_dividend_yield,
                            'Payout Ratio 4':payout_ratio}
    url_dict = {'summary': "https://finance.yahoo.com/quote/%s?p=%s", 'stat':"https://finance.yahoo.com/quote/%s/key-statistics?p=%s",
         'profile':"https://finance.yahoo.com/quote/%s/profile?p=%s", 'income': "https://finance.yahoo.com/quote/%s/financials?p=%s",
        'balance': "https://finance.yahoo.com/quote/%s/balance-sheet?p=%s", 'cash':"https://finance.yahoo.com/quote/%s/cash-flow?p=%s", 'analysis':"https://finance.yahoo.com/quote/%s/analysis?p=%s"    
    }
       
        
        
     
    return recent_price, eps1, eps2, eps3, eps4, industry, pres, pres_pay, ceo, ceo_born, ceo_pay, history_df,\
     metric_summary, metric_income, metric_balance, metric_statistics, metric_cash,url_dict