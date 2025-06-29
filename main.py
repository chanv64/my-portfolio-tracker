import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from scipy import stats
import os

from data_handler import load_transactions, fetch_price_data
from portfolio_processor import process_daily_transactions, calculate_daily_metrics, calculate_twr
from report_generator import generate_csv_reports
from chart_generator import generate_charts

def calculate_portfolio_performance(transactions_file, start_date, end_date):
    """
    Calculates daily portfolio performance and generates reports and charts.

    Args:
        transactions_file (str): Path to the CSV file with transaction data.
        start_date (str): The start date for the analysis in 'YYYY-MM-DD' format.
        end_date (str): The end date for the analysis in 'YYYY-MM-DD' format.
    """
    transactions = load_transactions(transactions_file)

    tickers = transactions['Ticker'].unique().tolist()
    spy_ticker = 'SPY'
    if spy_ticker not in tickers:
        tickers.append(spy_ticker)

    price_data = fetch_price_data(tickers, start_date, end_date)

    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)

    portfolio_value = pd.DataFrame(index=price_data[spy_ticker].index)
    open_positions = {}
    closed_positions = []

    portfolio_value['Current Value'] = 0.0
    portfolio_value['Cost'] = 0.0
    portfolio_value['Current P&L'] = 0.0
    portfolio_value['Closed P&L'] = 0.0
    portfolio_value['Overall P&L'] = 0.0
    portfolio_value['P&L Positive'] = 0.0
    portfolio_value['P&L Negative'] = 0.0
    portfolio_value['Daily P&L Change'] = 0.0
    portfolio_value['TWR'] = 1.0
    portfolio_value['SPY_TWR'] = 1.0
    portfolio_value['Net Invested Capital'] = 0.0
    portfolio_value['Cumulative Cash Flow Adjusted Return'] = 0.0
    portfolio_value['Drawdown'] = 0.0
    portfolio_value['Portfolio Daily Return'] = 0.0
    portfolio_value['SPY Daily Return'] = 0.0

    total_cash_in_cumulative = 0.0
    total_cash_out_cumulative = 0.0
    running_peak = 0.0

    for i, date in enumerate(portfolio_value.index):
        if i > 0:
            prev_trading_day = portfolio_value.index[i-1]
            portfolio_value.loc[date, 'Closed P&L'] = portfolio_value.loc[prev_trading_day, 'Closed P&L']
            total_cash_in_cumulative = portfolio_value.loc[prev_trading_day, 'total_cash_in_cumulative']
            total_cash_out_cumulative = portfolio_value.loc[prev_trading_day, 'total_cash_out_cumulative']
            running_peak = portfolio_value.loc[prev_trading_day, 'running_peak'] # Carry forward running_peak
        else:
            total_cash_in_cumulative = 0.0
            total_cash_out_cumulative = 0.0
            running_peak = 0.0 # Initialize for the first day

        day_transactions = transactions[transactions['Date'] == date]

        open_positions, portfolio_value, closed_positions, total_cash_in_cumulative, total_cash_out_cumulative = \
            process_daily_transactions(date, day_transactions, open_positions, portfolio_value, closed_positions, total_cash_in_cumulative, total_cash_out_cumulative)

        portfolio_value, running_peak = calculate_daily_metrics(date, open_positions, price_data, portfolio_value, total_cash_in_cumulative, total_cash_out_cumulative, i, running_peak)
        portfolio_value.loc[date, 'running_peak'] = running_peak # Store running_peak for next iteration

        portfolio_value = calculate_twr(i, date, portfolio_value, transactions, price_data, spy_ticker)

    open_positions_data = []
    total_market_value = portfolio_value['Current Value'].iloc[-1] if not portfolio_value.empty else 0
    for ticker, data in open_positions.items():
        if data['quantity'] > 0 and ticker in price_data.columns and not price_data[ticker].empty:
            eod_price = price_data[ticker].iloc[-1]
            value = data['quantity'] * eod_price
            portfolio_percent = round((value / total_market_value) * 100, 2) if total_market_value > 0 else 0.0
            pnl = round(value - data['cost_basis'], 2)
            open_positions_data.append({
                'Symbol': ticker,
                'Portfolio %': portfolio_percent,
                'Quantity': data['quantity'],
                'Price': round(eod_price, 2),
                'Cost': round(data['cost_basis'], 2),
                'Value': round(value, 2),
                'P&L': pnl
            })

    # --- Calculate Advanced Metrics ---
    # Risk-free rate (annualized, then converted to daily)
    RISK_FREE_RATE_ANNUAL = 0.02 # Example: 2% annual risk-free rate
    TRADING_DAYS_IN_YEAR = 252
    risk_free_rate_daily = RISK_FREE_RATE_ANNUAL / TRADING_DAYS_IN_YEAR

    # Portfolio Daily Returns (excluding the first day which has no return)
    portfolio_returns = portfolio_value['Portfolio Daily Return'][1:]
    spy_returns = portfolio_value['SPY Daily Return'][1:]

    # Sharpe Ratio
    avg_portfolio_return = portfolio_returns.mean()
    std_portfolio_return = portfolio_returns.std()
    sharpe_ratio = (avg_portfolio_return - risk_free_rate_daily) / std_portfolio_return if std_portfolio_return != 0 else 0.0
    sharpe_ratio_annualized = sharpe_ratio * np.sqrt(TRADING_DAYS_IN_YEAR)

    # Sortino Ratio
    downside_returns = portfolio_returns[portfolio_returns < risk_free_rate_daily]
    downside_deviation = downside_returns.std() if not downside_returns.empty else 0.0
    sortino_ratio = (avg_portfolio_return - risk_free_rate_daily) / downside_deviation if downside_deviation != 0 else 0.0
    sortino_ratio_annualized = sortino_ratio * np.sqrt(TRADING_DAYS_IN_YEAR)

    # Alpha and Beta (using linear regression)
    # Ensure both series have data and align their indices
    common_index = portfolio_returns.index.intersection(spy_returns.index)
    if len(common_index) > 1:
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            spy_returns.loc[common_index],
            portfolio_returns.loc[common_index]
        )
        beta = slope
        alpha_daily = intercept
        alpha_annualized = alpha_daily * TRADING_DAYS_IN_YEAR
    else:
        beta = 0.0
        alpha_daily = 0.0
        alpha_annualized = 0.0

    # Store advanced metrics in a dictionary to pass around
    advanced_metrics = {
        "sharpe_ratio": round(sharpe_ratio_annualized, 2),
        "sortino_ratio": round(sortino_ratio_annualized, 2),
        "beta": round(beta, 2),
        "alpha": round(alpha_annualized, 2)
    }

    generate_csv_reports(portfolio_value, open_positions_data, closed_positions)
    generate_charts(portfolio_value, open_positions_data)
    print("\n--- Portfolio Value DataFrame Columns before CSV generation ---")
    print(portfolio_value.columns)

    return advanced_metrics # Return advanced metrics

if __name__ == '__main__':
    transactions_file = 'transactions.csv'
    start_date = '2025-03-26'
    end_date = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    calculate_portfolio_performance(transactions_file, start_date, end_date)
    print("Portfolio analysis complete. Reports and charts are in the 'output/' directory.")