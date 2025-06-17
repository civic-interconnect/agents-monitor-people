"""
main.py - Civic Interconnect People Monitor Agent

Pulls legislators and governor data from OpenStates and summarizes counts.
"""

import os
import yaml
from datetime import datetime, timezone
from dotenv import load_dotenv
from civic_lib import logging_utils, api_utils
from parsers import openstates_people_parser


logging_utils.init_logger()
logging_utils.logger.info("===== Starting Monitor People Agent =====")

# Load environment variables
load_dotenv()

# Load API keys and configuration
openstates_api_key = api_utils.load_openstates_api_key()
config = api_utils.load_yaml_config("config.yaml")
version = api_utils.load_version("VERSION")

# Generate today's date string
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
logging_utils.logger.info(f"Polling date: {today}")

# Create storage paths
daily_report_path = os.path.join("reports", today)
os.makedirs(daily_report_path, exist_ok=True)
logging_utils.logger.info(f"Report path: {daily_report_path}")

# Query OpenStates
try:
    summary = openstates_people_parser.run(".", config, openstates_api_key)
except Exception as e:
    logging_utils.logger.error(f"Failed OpenStates query: {str(e)}")
    summary = f"People pull failed: {str(e)}"

# Write daily report
report = {"date": today, "People Summary": summary}
report_file = os.path.join(daily_report_path, f"{today}-people-report.yaml")
with open(report_file, "w") as f:
    yaml.dump(report, f, sort_keys=False)
logging_utils.logger.info(f"Report created: {report_file}")
