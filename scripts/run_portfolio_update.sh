#!/bin/bash

# Description:
# This script automates the daily update process for the portfolio tracker.
# It navigates to the project directory, activates the Python virtual environment,
# runs the `update_portfolio_data.py` script to fetch new data and recalculate
# portfolio metrics, and logs the entire process.
# This script is intended to be run as a scheduled task (e.g., via cron job).


# Navigate to the project directory
cd /Users/chanv/scripts/portfolio_tracker/

# Create log directory if it doesn't exist
mkdir -p log

# Define log file path
LOG_FILE="$(pwd)/log/update_portfolio.log"

# Capture current date and time
CURRENT_DATETIME=$(date "+%Y-%m-%d %H:%M:%S")

# Write separator and timestamp to log file
echo "
--- Script started at $CURRENT_DATETIME ---" >> "$LOG_FILE"

# Activate the uv virtual environment
source .venv/bin/activate

# Run the Python script and redirect output to log file
python scripts/update_portfolio_data.py >> "$LOG_FILE" 2>&1

# Deactivate the virtual environment (optional, but good practice)
deactivate

# Write end timestamp to log file
CURRENT_DATETIME=$(date "+%Y-%m-%d %H:%M:%S")
echo "--- Script finished at $CURRENT_DATETIME ---" >> "$LOG_FILE"

