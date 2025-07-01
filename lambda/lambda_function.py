import os
import sys

# Add the project root to the sys.path to allow imports from main.py and update_portfolio_data.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.update_portfolio_data import update_portfolio_data

def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    This function is triggered by EventBridge (CloudWatch Events) and calls
    the update_portfolio_data function to refresh portfolio metrics.
    """
    print("Lambda function triggered. Starting portfolio data update...")
    try:
        update_portfolio_data()
        print("Portfolio data update completed successfully.")
        return {
            'statusCode': 200,
            'body': 'Portfolio data updated successfully!'
        }
    except Exception as e:
        print(f"Error during portfolio data update: {e}")
        return {
            'statusCode': 500,
            'body': f'Error updating portfolio data: {e}'
        }
