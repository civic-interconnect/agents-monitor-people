"""
main.py - Civic Interconnect People Monitor Agent

Pulls legislators and governor data from OpenStates and summarizes counts.

MIT License — Civic Interconnect
"""

import os
import sys
from pathlib import Path

from civic_lib_core import config_utils, log_utils
from civic_lib_core.date_utils import today_utc_str
from civic_lib_core.path_utils import ensure_dir
from civic_lib_core.yaml_utils import write_yaml
from dotenv import load_dotenv

from agents_monitor_people.parsers import openstates_people_parser


def main():
    """
    Main function for the People Monitor Agent.
    Expected config.yaml keys:
    - report_path
    - openstates_graphql_url
    """
    log_utils.init_logger()
    logger = log_utils.logger

    logger.info("===== Starting Monitor People Agent =====")
    load_dotenv()

    root_dir = Path.cwd()
    config = config_utils.load_yaml_config("config.yaml", root_dir=root_dir)
    version = config_utils.load_version("VERSION", root_dir=root_dir)
    api_key: str | None = os.getenv("OPENSTATES_API_KEY")
    today = today_utc_str()
    logger.info(f"Polling date: {today}")

    report_path = ensure_dir(Path(config["report_path"]) / today)
    logger.info(f"Report path: {report_path}")

    if api_key:
        try:
            summary = openstates_people_parser.run(".", config, api_key)
        except Exception as e:
            logger.error(f"OpenStates people pull failed: {str(e)}")
            summary = f"People pull failed: {str(e)}"

    else:
        logger.error("OPENSTATES_API_KEY not set in environment variables.")
        summary = "People pull failed: OPENSTATES_API_KEY not set."

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
    except Exception:
        sys.exit(1)
