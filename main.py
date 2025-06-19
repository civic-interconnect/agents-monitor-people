"""
main.py - Civic Interconnect People Monitor Agent

Pulls legislators and governor data from OpenStates and summarizes counts.

MIT License — Civic Interconnect
"""

import sys
from pathlib import Path
from dotenv import load_dotenv
from civic_lib import log_utils, config_utils
from civic_lib.date_utils import today_utc_str
from civic_lib.path_utils import ensure_dir
from civic_lib.yaml_utils import write_yaml
from parsers import openstates_people_parser

log_utils.init_logger()
logger = log_utils.logger


def main():
    """
    Main function for the People Monitor Agent.
    Expected config.yaml keys:
    - report_path
    - openstates_graphql_url
    """
    logger.info("===== Starting Monitor People Agent =====")
    load_dotenv()

    ROOT_DIR = Path(__file__).resolve().parent
    config = config_utils.load_yaml_config("config.yaml", root_dir=ROOT_DIR)
    version = config_utils.load_version("VERSION", root_dir=ROOT_DIR)
    api_key = config_utils.load_openstates_api_key()
    today = today_utc_str()
    logger.info(f"Polling date: {today}")

    report_path = ensure_dir(Path(config["report_path"]) / today)
    logger.info(f"Report path: {report_path}")

    try:
        summary = openstates_people_parser.run(".", config, api_key)
    except Exception as e:
        logger.error(f"OpenStates people pull failed: {str(e)}")
        summary = f"People pull failed: {str(e)}"

    report = {
        "date": today,
        "version": version,
        "People Summary": summary,
    }

    report_file = report_path / f"{today}-people-report.yaml"
    write_yaml(report, report_file)
    logger.info(f"Report created: {report_file}")


if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except Exception as e:
        logger.exception(f"Agent failed unexpectedly. {e}")
        sys.exit(1)
