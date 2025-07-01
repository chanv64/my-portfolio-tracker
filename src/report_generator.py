import pandas as pd

def generate_csv_reports(portfolio_value, open_positions_data, closed_positions):
    portfolio_value = portfolio_value.round(2)
    # Select only the desired columns for the final CSV report
    columns_to_save = [
        'Current Value', 'Cost', 'Current P&L', 'Closed P&L', 'Overall P&L',
        'P&L Positive', 'P&L Negative', 'Daily P&L Change', 'TWR', 'SPY_TWR',
        'Net Invested Capital', 'Cumulative Cash Flow Adjusted Return', 'Drawdown',
        'Portfolio Daily Return', 'SPY Daily Return'
    ]
    portfolio_value[columns_to_save].to_csv('output/portfolio_value.csv', index=True, index_label='Date')

    pd.DataFrame(open_positions_data).to_csv('output/open_positions.csv', index=False)

    pd.DataFrame(closed_positions).to_csv('output/closed_positions.csv', index=False)