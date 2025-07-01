import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def load_transactions(transactions_file):
    transactions = pd.read_csv(transactions_file)
    transactions['Date'] = pd.to_datetime(transactions['Date'], format='%m/%d/%y')
    transactions = transactions.sort_values(by='Date')
    return transactions

def fetch_price_data(tickers, start_date, end_date):
    price_data = yf.download(tickers, start=start_date, end=end_date)['Close']
    return price_data