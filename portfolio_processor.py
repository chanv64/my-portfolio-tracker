import pandas as pd

def process_daily_transactions(date, day_transactions, open_positions, portfolio_value, closed_positions, total_cash_in_cumulative, total_cash_out_cumulative):
    for _, row in day_transactions.iterrows():
        ticker, trans_type, quantity, price, commission = row['Ticker'], row['Type'], row['Quantity'], row['Price'], row['Commission']

        if trans_type == 'Buy':
            if ticker not in open_positions:
                open_positions[ticker] = {'quantity': 0, 'cost_basis': 0, 'lots': []}
            
            open_positions[ticker]['lots'].append({'quantity': quantity, 'cost_per_share': (quantity * price + commission) / quantity})
            open_positions[ticker]['quantity'] += quantity
            open_positions[ticker]['cost_basis'] += round(quantity * price + commission, 2)
            total_cash_in_cumulative += round(quantity * price + commission, 2)

        elif trans_type == 'Sell':
            if ticker in open_positions and open_positions[ticker]['quantity'] >= quantity:
                realised_pnl = 0
                sold_cost = 0
                
                remaining_quantity = quantity
                for lot in open_positions[ticker]['lots']:
                    if remaining_quantity == 0:
                        break
                    
                    if lot['quantity'] >= remaining_quantity:
                        sold_cost += remaining_quantity * lot['cost_per_share']
                        lot['quantity'] -= remaining_quantity
                        remaining_quantity = 0
                    else:
                        sold_cost += lot['quantity'] * lot['cost_per_share']
                        remaining_quantity -= lot['quantity']
                        lot['quantity'] = 0
                
                open_positions[ticker]['lots'] = [lot for lot in open_positions[ticker]['lots'] if lot['quantity'] > 0]

                realised_pnl = (quantity * price) - sold_cost - commission
                portfolio_value.loc[date, 'Closed P&L'] += realised_pnl
                
                open_positions[ticker]['quantity'] -= quantity
                open_positions[ticker]['cost_basis'] -= sold_cost
                total_cash_out_cumulative += round(quantity * price - commission, 2)
                
                closed_positions.append({
                    'Symbol': ticker,
                    'Quantity': quantity,
                    'Cost': round(sold_cost, 2),
                    'Sell Price': round(price, 2),
                    'Sell Date': date,
                    'P&L': round(realised_pnl, 2)
                })
    return open_positions, portfolio_value, closed_positions, total_cash_in_cumulative, total_cash_out_cumulative

def calculate_daily_metrics(date, open_positions, price_data, portfolio_value, total_cash_in_cumulative, total_cash_out_cumulative, i):
    current_value = 0
    total_cost = 0
    
    for ticker, data in open_positions.items():
        if data['quantity'] > 0 and ticker in price_data.columns and date in price_data.index:
            eod_price = price_data.loc[date, ticker]
            if pd.notna(eod_price):
                current_value += data['quantity'] * eod_price
                total_cost += data['cost_basis']

    portfolio_value.loc[date, 'Current Value'] = round(current_value, 2)
    portfolio_value.loc[date, 'Cost'] = round(total_cost, 2)
    portfolio_value.loc[date, 'Current P&L'] = round(current_value - total_cost, 2)
    
    portfolio_value.loc[date, 'Overall P&L'] = round(portfolio_value.loc[date, 'Current P&L'] + portfolio_value.loc[date, 'Closed P&L'], 2)
    
    if portfolio_value.loc[date, 'Overall P&L'] > 0:
        portfolio_value.loc[date, 'P&L Positive'] = round(portfolio_value.loc[date, 'Overall P&L'], 2)
        portfolio_value.loc[date, 'P&L Negative'] = 0.0
    else:
        portfolio_value.loc[date, 'P&L Positive'] = 0.0
        portfolio_value.loc[date, 'P&L Negative'] = round(portfolio_value.loc[date, 'Overall P&L'], 2)
        
    if i > 0:
        prev_trading_day = portfolio_value.index[i-1]
        portfolio_value.loc[date, 'Daily P&L Change'] = round(portfolio_value.loc[date, 'Overall P&L'] - portfolio_value.loc[prev_trading_day, 'Overall P&L'], 2)

    portfolio_value.loc[date, 'total_cash_in_cumulative'] = total_cash_in_cumulative
    portfolio_value.loc[date, 'total_cash_out_cumulative'] = total_cash_out_cumulative
    net_invested_capital = total_cash_in_cumulative - total_cash_out_cumulative
    portfolio_value.loc[date, 'Net Invested Capital'] = round(net_invested_capital, 2)

    if net_invested_capital != 0:
        cumulative_value = portfolio_value.loc[date, 'Current Value'] + portfolio_value.loc[date, 'Closed P&L']
        portfolio_value.loc[date, 'Cumulative Cash Flow Adjusted Return'] = round((cumulative_value - net_invested_capital) / net_invested_capital, 4)
    else:
        portfolio_value.loc[date, 'Cumulative Cash Flow Adjusted Return'] = 0.0
    
    return portfolio_value

def calculate_twr(i, date, portfolio_value, transactions, price_data, spy_ticker):
    if i > 0:
        prev_trading_day = portfolio_value.index[i-1]
        net_cash_flow = 0
        daily_transactions_for_twr = transactions[transactions['Date'] == date]
        if not daily_transactions_for_twr.empty:
            for _, trans_row in daily_transactions_for_twr.iterrows():
                if trans_row['Type'] == 'Buy':
                    net_cash_flow -= trans_row['Quantity'] * trans_row['Price']
                elif trans_row['Type'] == 'Sell':
                    net_cash_flow += trans_row['Quantity'] * trans_row['Price']

            adjusted_start_value = portfolio_value.loc[prev_trading_day, 'Current Value'] + net_cash_flow

            if adjusted_start_value != 0:
                daily_return = (portfolio_value.loc[date, 'Current Value'] - adjusted_start_value) / adjusted_start_value
                portfolio_value.loc[date, 'TWR'] = round(portfolio_value.loc[prev_trading_day, 'TWR'] * (1 + daily_return), 4)
            else:
                portfolio_value.loc[date, 'TWR'] = portfolio_value.loc[prev_trading_day, 'TWR']

        else:
            if portfolio_value.loc[prev_trading_day, 'Current Value'] != 0:
                daily_return = (portfolio_value.loc[date, 'Current Value'] / portfolio_value.loc[prev_trading_day, 'Current Value']) - 1
                portfolio_value.loc[date, 'TWR'] = round(portfolio_value.loc[prev_trading_day, 'TWR'] * (1 + daily_return), 4)
            else:
                portfolio_value.loc[date, 'TWR'] = portfolio_value.loc[prev_trading_day, 'TWR']


        if prev_trading_day in price_data[spy_ticker].index and date in price_data[spy_ticker].index:
            spy_daily_return = (price_data[spy_ticker][date] / price_data[spy_ticker][prev_trading_day]) - 1
            portfolio_value.loc[date, 'SPY_TWR'] = round(portfolio_value.loc[prev_trading_day, 'SPY_TWR'] * (1 + spy_daily_return), 4)
        else:
            portfolio_value.loc[date, 'SPY_TWR'] = portfolio_value.loc[prev_trading_day, 'SPY_TWR']
    return portfolio_value