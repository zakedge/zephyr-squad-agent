from pathlib import Path
from typing import Dict, List

import pandas as pd


REQUIRED_COLUMNS = ["test_case_key", "status", "evidence_file", "comment"]


def read_execution_file(file_path: str) -> List[Dict[str, str]]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    elif path.suffix.lower() in [".xlsx", ".xls"]:
        df = pd.read_excel(path)
    else:
        raise ValueError("Only CSV and Excel files are supported")

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    df = df.fillna("")

    records: List[Dict[str, str]] = []

    for _, row in df.iterrows():
        records.append(
            {
                "test_case_key": str(row["test_case_key"]).strip(),
                "status": str(row["status"]).strip(),
                "evidence_file": str(row["evidence_file"]).strip(),
                "comment": str(row["comment"]).strip(),
            }
        )

    return records