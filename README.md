# Portfolio Tracker

This project provides a comprehensive portfolio tracking and analysis tool built with Python. It processes transaction data from a CSV file, fetches historical stock prices, calculates various portfolio performance metrics, and generates insightful reports and charts.

## Features

- **Transaction Processing**: Reads and processes buy and sell transactions from a `transactions.csv` file.
- **Daily Performance Calculation**: Calculates daily portfolio value, cost basis, current P&L, closed P&L, and overall P&L.
- **Cash Flow Adjusted Return**: Computes a cumulative cash flow adjusted return (similar to Money-Weighted Return) to reflect performance based on actual capital invested.
- **Open and Closed Positions Reports**: Generates detailed reports for open and closed positions, including cost basis and realized P&L.
- **Historical Data Fetching**: Utilizes `yfinance` to fetch historical end-of-day stock prices.
- **Advanced Performance Metrics**: Calculates key financial metrics such as Sharpe Ratio, Sortino Ratio, Alpha, and Beta.
- **Visualizations**: Generates several charts to visualize portfolio performance:
    - Total Portfolio Value vs. Total Cost over time.
    - Daily P&L Change (bar chart).
    - Portfolio Asset Allocation (pie chart).
    - Time-Weighted Return (TWR) of the portfolio compared to SPY.
    - Cumulative Cash Flow Adjusted Return over time.

## Project Structure

```
```
portfolio_tracker/
├── main.py
├── requirements.txt
├── data/
│   └── transactions.csv
├── src/
│   ├── __init__.py
│   ├── data_handler.py
│   ├── portfolio_processor.py
│   ├── report_generator.py
│   └── chart_generator.py
├── scripts/
│   ├── run_portfolio_update.sh
│   └── update_portfolio_data.py
├── lambda/
│   └── lambda_function.py
├── portfolio_web_app/
│   ├── app.py
│   ├── portfolio_web_app_react/
│   └── static/
└── output/
    ├── portfolio_value.csv
    ├── open_positions.csv
    ├── closed_positions.csv
    ├── portfolio_value_over_time.png
    ├── daily_pnl_change.png
    ├── asset_allocation.png
    ├── twr_vs_spy.png
    └── cumulative_cash_flow_adjusted_return.png
```
```

## Web Application (portfolio_web_app)

The `portfolio_web_app` is a FastAPI application that provides a web interface for the portfolio tracking and analysis tool. It offers the following functionalities:

-   **Interactive Dashboard**: Serves a React-based frontend for an interactive user experience.
-   **API Endpoints**: Exposes RESTful APIs to retrieve processed portfolio data (e.g., portfolio value, open/closed positions) and chart-specific data.
-   **Transaction Management**: Allows users to add new transactions via a web form, triggering an immediate recalculation of portfolio performance.
-   **Advanced Metrics Display**: Provides endpoints to fetch and display advanced portfolio metrics like Sharpe Ratio, Sortino Ratio, Alpha, and Beta.
-   **AWS S3 Integration**: Supports uploading updated transaction data to an AWS S3 bucket when deployed in a Lambda environment.

To run the web application:

```bash
uvicorn portfolio_web_app.app:app --reload
```

Then, open your browser and navigate to `http://127.0.0.1:8000`.

## Setup and Installation

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone https://github.com/chanv64/my-portfolio-tracker.git
    cd my-portfolio-tracker
    ```

2.  **Create a virtual environment using `uv`:**
    ```bash
    uv venv
    ```

3.  **Activate the virtual environment:**
    ```bash
    source .venv/bin/activate
    ```

4.  **Install dependencies:**
    ```bash
    uv pip install -r requirements.txt
    ```

## Usage

1.  **Prepare your `transactions.csv` file:** Ensure your transaction data is in the specified format within `transactions.csv`.

2.  **Run the main script:**
    ```bash
    python main.py
    ```

    The script will:
    - Fetch historical stock data.
    - Process your transactions daily.
    - Generate CSV reports in the `output/` directory.
    - Generate PNG charts in the `output/` directory.

## Data Considerations

- The script fetches historical data using `yfinance`. Ensure your system's timezone is correctly configured if you encounter issues with the latest day's data. The script attempts to fetch data up to the day after the current execution date to ensure the latest available market data is included.
- Realized P&L calculations account for both buy and sell commissions.

## Contributing

Feel free to fork this repository, open issues, or submit pull requests to improve the project.