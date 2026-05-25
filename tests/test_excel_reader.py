import pandas as pd
import pytest

from src.excel_reader import read_execution_file


def test_read_execution_csv(tmp_path):
    file_path = tmp_path / "execution.csv"

    df = pd.DataFrame(
        [
            {
                "test_case_key": "QA-101",
                "status": "PASS",
                "evidence_file": "QA-101.png",
                "comment": "Passed",
            }
        ]
    )

    df.to_csv(file_path, index=False)

    records = read_execution_file(str(file_path))

    assert len(records) == 1
    assert records[0]["test_case_key"] == "QA-101"
    assert records[0]["status"] == "PASS"
    assert records[0]["evidence_file"] == "QA-101.png"
    assert records[0]["comment"] == "Passed"


def test_missing_required_column_raises_error(tmp_path):
    file_path = tmp_path / "bad.csv"

    df = pd.DataFrame(
        [
            {
                "test_case_key": "QA-101",
                "status": "PASS",
            }
        ]
    )

    df.to_csv(file_path, index=False)

    with pytest.raises(ValueError):
        read_execution_file(str(file_path))


def test_unsupported_file_type_raises_error(tmp_path):
    file_path = tmp_path / "execution.txt"
    file_path.write_text("hello")

    with pytest.raises(ValueError):
        read_execution_file(str(file_path))