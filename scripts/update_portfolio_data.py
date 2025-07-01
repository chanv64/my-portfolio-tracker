import sys
import os
import boto3
import tempfile
from datetime import datetime, timedelta

# Adjust path to import calculate_portfolio_performance from main.py
# This assumes update_portfolio_data.py is in the same directory as main.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import calculate_portfolio_performance

def update_portfolio_data():
    s3_bucket_name = 'chanvawsbucket'
    s3_key = 'data/transactions.csv'

    s3 = boto3.client('s3')

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        transactions_file_path = temp_file.name
        s3.download_file(s3_bucket_name, s3_key, transactions_file_path)
    
    # Use a fixed start date as seen in app.py, or make it dynamic if needed
    start_date = '2025-03-26' 
    
    # Calculate end_date as tomorrow's date to ensure all data up to today is processed
    end_date = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')

    print(f"Starting portfolio data update for period {start_date} to {end_date}...")
    try:
        advanced_metrics = calculate_portfolio_performance(transactions_file_path, start_date, end_date)
        print("Portfolio data updated successfully.")
        print("Advanced Metrics:", advanced_metrics)
    except Exception as e:
        print(f"Error updating portfolio data: {e}")
    finally:
        # Clean up the temporary file
        os.remove(transactions_file_path)

if __name__ == "__main__":
    update_portfolio_data()
