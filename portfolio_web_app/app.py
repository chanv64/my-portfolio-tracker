from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import os
from datetime import datetime, timedelta
import boto3

# Assuming main.py is in the parent directory and contains calculate_portfolio_performance
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from main import calculate_portfolio_performance

app = FastAPI()

# Define base directory for the app
APP_DIR = os.path.dirname(os.path.abspath(__file__))
# Define the project root directory (one level up from app.py)
PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, '..'))

# Define key file and directory paths
STATIC_DIR = os.path.join(APP_DIR, 'static')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output')
TRANSACTIONS_FILE = os.path.join(PROJECT_ROOT, 'transactions.csv')

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Templates for serving HTML (we'll use a simple HTML string for now, but Jinja2 is an option)
# templates = Jinja2Templates(directory="portfolio_tracker/portfolio_web_app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Portfolio Tracker</title>
        <link rel="stylesheet" href="/static/style.css">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <!-- DataTables CSS -->
        <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.css">
    </head>
    <body>
        <div class="container">
            <nav class="sidebar">
                <h2>Menu</h2>
                <ul>
                    <li><a href="#" id="nav-welcome">Welcome</a></li>
                    <li><a href="#" id="nav-charts">Charts</a></li>
                    <li><a href="#" id="nav-portfolio-values">Portfolio Values</a></li>
                    <li><a href="#" id="nav-open-positions">Open Positions</a></li>
                    <li><a href="#" id="nav-closed-positions">Closed Positions</a></li>
                    <li><a href="#" id="nav-add-transaction">Add Transaction</a></li>
                </ul>
            </nav>
            <div class="content-area">
                <h1>My Portfolio Dashboard</h1>

                <div id="welcome-section" class="content-section">
                    <h2>Welcome to Your Portfolio Tracker!</h2>
                    <p>Use the navigation on the left to explore your portfolio's performance, view detailed positions, or add new transactions.</p>
                    <img src="/static/welcome.jpg" alt="Welcome Image" class="welcome-image">
                </div>

                <div id="charts-section" class="content-section hidden">
                    <h2>Charts</h2>
                    <div class="tabs">
                        <button class="chart-tab-button active" data-tab-id="portfolio-value-chart-tab">Portfolio Value</button>
                        <button class="chart-tab-button" data-tab-id="daily-pnl-chart-tab">Daily P&L</button>
                        <button class="chart-tab-button" data-tab-id="asset-allocation-chart-tab">Asset Allocation</button>
                        <button class="chart-tab-button" data-tab-id="twr-chart-tab">TWR vs SPY</button>
                        <button class="chart-tab-button" data-tab-id="cumulative-return-chart-tab">Cumulative Return</button>
                    </div>

                    <div id="portfolio-value-chart-tab" class="chart-tab-content">
                        <h3>Portfolio Value Over Time</h3>
                        <canvas id="portfolio_value_chart"></canvas>
                    </div>
                    <div id="daily-pnl-chart-tab" class="chart-tab-content hidden">
                        <h3>Daily P&L Change</h3>
                        <canvas id="daily_pnl_chart"></canvas>
                    </div>
                    <div id="asset-allocation-chart-tab" class="chart-tab-content hidden">
                        <h3>Asset Allocation</h3>
                        <canvas id="asset_allocation_chart"></canvas>
                    </div>
                    <div id="twr-chart-tab" class="chart-tab-content hidden">
                        <h3>Time-Weighted Return (TWR) vs. SPY</h3>
                        <canvas id="twr_chart"></canvas>
                    </div>
                    <div id="cumulative-return-chart-tab" class="chart-tab-content hidden">
                        <h3>Cumulative Cash Flow Adjusted Return</h3>
                        <canvas id="cumulative_return_chart"></canvas>
                    </div>
                </div>

                <div id="portfolio-values-section" class="content-section hidden">
                    <h2>Portfolio Values</h2>
                    <table id="portfolio_value_table"></table>
                    <div id="metrics-display"></div>
                </div>

                <div id="open-positions-section" class="content-section hidden">
                    <h2>Open Positions</h2>
                    <table id="open_positions_table"></table>
                </div>

                <div id="closed-positions-section" class="content-section hidden">
                    <h2>Closed Positions</h2>
                    <table id="closed_positions_table"></table>
                </div>

                <div id="add-transaction-section" class="content-section hidden">
                    <h2>Add New Transaction</h2>
                    <form id="transaction_form">
                        <label for="date">Date:</label>
                        <input type="date" id="date" name="date" required><br><br>
                        <label for="ticker">Ticker:</label>
                        <input type="text" id="ticker" name="ticker" required><br><br>
                        <label for="type">Type:</label>
                        <select id="type" name="type" required>
                            <option value="Buy">Buy</option>
                            <option value="Sell">Sell</option>
                        </select><br><br>
                        <label for="quantity">Quantity:</label>
                        <input type="number" id="quantity" name="quantity" required min="1"><br><br>
                        <label for="price">Price:</label>
                        <input type="number" step="0.01" id="price" name="price" required min="0.01"><br><br>
                        <label for="commission">Commission:</label>
                        <input type="number" step="0.01" id="commission" name="commission" required min="0"><br><br>
                        <button type="submit">Add Transaction</button>
                    </form>
                    <p id="message"></p>
                </div>
            </div>
        </div>
        <!-- jQuery (required by DataTables) -->
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <!-- DataTables JS -->
        <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.js"></script>
        <script src="/static/script.js"></script>
    </body>
    </html>
    '''
    return HTMLResponse(content=html_content)

@app.get("/data/portfolio_value")
async def get_portfolio_value_data():
    df = pd.read_csv(os.path.join(OUTPUT_DIR, "portfolio_value.csv"))
    return df.to_dict(orient="records")

@app.get("/data/open_positions")
async def get_open_positions_data():
    df = pd.read_csv(os.path.join(OUTPUT_DIR, "open_positions.csv"))
    return df.to_dict(orient="records")

@app.get("/data/closed_positions")
async def get_closed_positions_data():
    df = pd.read_csv(os.path.join(OUTPUT_DIR, "closed_positions.csv"))
    return df.to_dict(orient="records")

@app.get("/data/chart/portfolio_value_over_time")
async def get_portfolio_value_chart_data():
    df = pd.read_csv(os.path.join(OUTPUT_DIR, "portfolio_value.csv"))
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
    return {"dates": df["Date"].tolist(), "current_value": df["Current Value"].tolist(), "cost": df["Cost"].tolist()}

@app.get("/data/chart/daily_pnl_change")
async def get_daily_pnl_change_chart_data():
    df = pd.read_csv(os.path.join(OUTPUT_DIR, "portfolio_value.csv"))
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
    return {"dates": df["Date"].tolist(), "daily_pnl_change": df["Daily P&L Change"].tolist()}

@app.get("/data/chart/asset_allocation")
async def get_asset_allocation_chart_data():
    df = pd.read_csv(os.path.join(OUTPUT_DIR, "open_positions.csv"))
    return {"labels": df["Symbol"].tolist(), "values": df["Value"].tolist()}

@app.get("/data/chart/twr_vs_spy")
async def get_twr_vs_spy_chart_data():
    df = pd.read_csv(os.path.join(OUTPUT_DIR, "portfolio_value.csv"))
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
    return {"dates": df["Date"].tolist(), "portfolio_twr": df["TWR"].tolist(), "spy_twr": df["SPY_TWR"].tolist()}

@app.get("/data/chart/cumulative_cash_flow_adjusted_return")
async def get_cumulative_return_chart_data():
    df = pd.read_csv(os.path.join(OUTPUT_DIR, "portfolio_value.csv"))
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
    return {"dates": df["Date"].tolist(), "cumulative_return": df["Cumulative Cash Flow Adjusted Return"].tolist()}

@app.get("/data/metrics/maximum_drawdown")
async def get_maximum_drawdown():
    df = pd.read_csv(os.path.join(OUTPUT_DIR, "portfolio_value.csv"))
    # Maximum Drawdown is the largest value in the 'Drawdown' column
    mdd = df['Drawdown'].max()
    return {"maximum_drawdown": round(mdd * 100, 2)} # Return as percentage

@app.post("/transactions")
async def add_transaction(request: Request,
                          date: str = Form(...),
                          ticker: str = Form(...),
                          type: str = Form(...),
                          quantity: int = Form(...),
                          price: float = Form(...),
                          commission: float = Form(...)):
    
    # Convert date from YYYY-MM-DD (from date picker) to MM/DD/YY for CSV
    formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%m/%d/%y')

    transaction_data = {
        "Date": formatted_date,
        "Ticker": ticker.upper(),
        "Type": type.capitalize(),
        "Quantity": quantity,
        "Price": price,
        "Commission": commission
    }

    transactions_file = TRANSACTIONS_FILE
    try:
        # Append to transactions.csv
        with open(transactions_file, 'a') as f:
            f.write(f"\n{transaction_data['Date']},{transaction_data['Ticker']},{transaction_data['Type']},{transaction_data['Quantity']},{transaction_data['Price']},{transaction_data['Commission']}")
        
        # Re-run the portfolio calculation
        # Get the latest end_date from the transactions file for recalculation
        latest_transaction_date = pd.to_datetime(date, format='%m/%d/%y')
        # Ensure end_date for yfinance is tomorrow's date relative to current execution
        end_date_for_calc = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        advanced_metrics = calculate_portfolio_performance(transactions_file, '2025-03-26', end_date_for_calc)

        # If running in AWS Lambda, upload the updated transactions.csv to S3
        if 'AWS_LAMBDA_FUNCTION_NAME' in os.environ:
            try:
                s3 = boto3.client('s3')
                s3_bucket_name = 'chanvawsbucket'
                s3_key = 'data/transactions.csv'
                s3.upload_file(transactions_file, s3_bucket_name, s3_key)
                return {"message": "Transaction added, portfolio updated, and data synced with S3 successfully!", "advanced_metrics": advanced_metrics}
            except Exception as e:
                return {"message": f"Error uploading to S3: {e}"}

        return {"message": "Transaction added and portfolio updated successfully!", "advanced_metrics": advanced_metrics}
    except Exception as e:
        return {"message": f"Error adding transaction: {e}"}

@app.get("/data/metrics/advanced")
async def get_advanced_metrics():
    # Re-run calculation to get the latest metrics
    transactions_file = TRANSACTIONS_FILE
    end_date_for_calc = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    advanced_metrics = calculate_portfolio_performance(transactions_file, '2025-03-26', end_date_for_calc)
    return advanced_metrics
