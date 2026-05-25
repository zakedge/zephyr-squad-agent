from src.executor import ExecutionRunner


class FakeZephyrClient:
    def __init__(self):
        self.updated = []
        self.uploaded = []

    def build_execution_lookup(self):
        return {
            "QA-101": "1001",
            "QA-102": "1002",
        }

    def update_execution_status(self, execution_id, status_id, comment=""):
        self.updated.append(
            {
                "execution_id": execution_id,
                "status_id": status_id,
                "comment": comment,
            }
        )
        return {}

    def upload_attachment(self, execution_id, evidence_path):
        self.uploaded.append(
            {
                "execution_id": execution_id,
                "evidence_path": evidence_path,
            }
        )
        return {}


def test_runner_updates_execution_without_evidence():
    client = FakeZephyrClient()
    runner = ExecutionRunner(client)

    records = [
        {
            "test_case_key": "QA-101",
            "status": "PASS",
            "evidence_file": "",
            "comment": "Passed",
        }
    ]

    results = runner.run(records)

    assert results[0]["result"] == "SUCCESS"
    assert results[0]["execution_id"] == "1001"
    assert client.updated[0]["status_id"] == 1
    assert client.updated[0]["comment"] == "Passed"


def test_runner_fails_when_execution_not_found():
    client = FakeZephyrClient()
    runner = ExecutionRunner(client)

    records = [
        {
            "test_case_key": "QA-999",
            "status": "PASS",
            "evidence_file": "",
            "comment": "Missing",
        }
    ]

    results = runner.run(records)

    assert results[0]["result"] == "FAILED"
    assert "No execution found" in results[0]["message"]