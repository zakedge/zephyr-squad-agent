import argparse
from pathlib import Path

import pandas as pd

from src.config import get_settings
from src.excel_reader import read_execution_file
from src.executor import ExecutionRunner
from src.zephyr_client import ZephyrClient


def main() -> None:
    parser = argparse.ArgumentParser(description="Zephyr Squad execution agent")

    parser.add_argument(
        "--input",
        required=True,
        help="Path to CSV or Excel execution file",
    )

    parser.add_argument(
        "--evidence-dir",
        default="evidence",
        help="Folder containing evidence files",
    )

    parser.add_argument(
        "--report",
        default="reports/execution_report.csv",
        help="Output report path",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview updates without changing Zephyr Squad",
    )

    args = parser.parse_args()

    settings = get_settings()
    records = read_execution_file(args.input)

    client = ZephyrClient(settings)
    runner = ExecutionRunner(
        client,
        evidence_dir=args.evidence_dir,
        dry_run=args.dry_run,
    )

    results = runner.run(records)

    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(results).to_csv(report_path, index=False)

    print(f"Execution completed. Report saved to: {report_path}")

    dry_run_count = sum(1 for item in results if item["result"] == "DRY_RUN")
    success_count = sum(1 for item in results if item["result"] == "SUCCESS")
    failed_count = sum(1 for item in results if item["result"] == "FAILED")

    print(f"Dry run: {dry_run_count}")
    print(f"Success: {success_count}")
    print(f"Failed: {failed_count}")


if __name__ == "__main__":
    main()