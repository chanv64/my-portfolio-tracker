from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
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
TRANSACTIONS_FILE = os.path.join(PROJECT_ROOT, 'data', 'transactions.csv')

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Templates for serving HTML (we'll use a simple HTML string for now, but Jinja2 is an option)
# templates = Jinja2Templates(directory="portfolio_tracker/portfolio_web_app/templates")

# Mount the React app's static files
app.mount("/app", StaticFiles(directory=os.path.join(APP_DIR, "portfolio_web_app_react/dist"), html=True), name="react_app")

@app.get("/")
async def read_root_redirect():
    return RedirectResponse(url="/app/")

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

# Catch-all route for React Router
@app.get("/app/{full_path:path}", response_class=HTMLResponse)
async def serve_react_app_paths(full_path: str):
    return FileResponse(os.path.join(APP_DIR, "portfolio_web_app_react/dist/index.html"))
