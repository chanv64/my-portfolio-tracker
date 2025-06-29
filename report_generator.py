import pandas as pd

def generate_csv_reports(portfolio_value, open_positions_data, closed_positions):
    portfolio_value = portfolio_value.round(2)
    portfolio_value.to_csv('output/portfolio_value.csv')

    pd.DataFrame(open_positions_data).to_csv('output/open_positions.csv', index=False)

    pd.DataFrame(closed_positions).to_csv('output/closed_positions.csv', index=False)