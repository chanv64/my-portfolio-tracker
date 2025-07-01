import matplotlib.pyplot as plt
import pandas as pd

def generate_charts(portfolio_value, open_positions_data):
    # 1. Portfolio Value Over Time
    plt.figure(figsize=(12, 6))
    plt.plot(portfolio_value.index, portfolio_value['Current Value'], label='Total Portfolio Value')
    plt.plot(portfolio_value.index, portfolio_value['Cost'], label='Total Cost')
    plt.title('Portfolio Value Over Time')
    plt.xlabel('Date')
    plt.ylabel('Value ($)')
    plt.grid(True)
    plt.legend()
    plt.savefig('output/portfolio_value_over_time.png')
    plt.close()

    # 2. Daily P&L Change
    plt.figure(figsize=(12, 6))
    colors = ['g' if x > 0 else 'r' for x in portfolio_value['Daily P&L Change']]
    plt.bar(portfolio_value.index, portfolio_value['Daily P&L Change'], color=colors)
    plt.title('Daily Portfolio P&L Change')
    plt.xlabel('Date')
    plt.ylabel('P&L Change ($)')
    plt.grid(True)
    plt.savefig('output/daily_pnl_change.png')
    plt.close()

    # 3. Asset Allocation
    plt.figure(figsize=(8, 8))
    open_pos_df = pd.DataFrame(open_positions_data)
    if not open_pos_df.empty:
        plt.pie(open_pos_df['Value'], labels=open_pos_df['Symbol'], autopct='%1.1f%%', startangle=140)
        plt.title('Portfolio Asset Allocation')
        plt.axis('equal')
        plt.savefig('output/asset_allocation.png')
    plt.close()

    # 4. TWR vs. SPY
    plt.figure(figsize=(12, 6))
    plt.plot(portfolio_value.index, portfolio_value['TWR'], label='Portfolio TWR')
    plt.plot(portfolio_value.index, portfolio_value['SPY_TWR'], label='SPY TWR')
    plt.title('Time-Weighted Return (TWR) vs. SPY')
    plt.xlabel('Date')
    plt.ylabel('TWR (Normalized to 1)')
    plt.grid(True)
    plt.legend()
    plt.savefig('output/twr_vs_spy.png')
    plt.close()

    # 5. Cumulative Cash Flow Adjusted Return
    plt.figure(figsize=(12, 6))
    plt.plot(portfolio_value.index, portfolio_value['Cumulative Cash Flow Adjusted Return'], label='Cumulative Cash Flow Adjusted Return')
    plt.title('Cumulative Cash Flow Adjusted Return Over Time')
    plt.xlabel('Date')
    plt.ylabel('Return (%)')
    plt.grid(True)
    plt.legend()
    plt.savefig('output/cumulative_cash_flow_adjusted_return.png')
    plt.close()