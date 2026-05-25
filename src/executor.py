from pathlib import Path
from typing import Any, Dict, List

from src.status_mapper import map_status
from src.zephyr_client import ZephyrClient


class ExecutionRunner:
    def __init__(self, zephyr_client: ZephyrClient, evidence_dir: str = "evidence"):
        self.zephyr_client = zephyr_client
        self.evidence_dir = Path(evidence_dir)

    def run(self, records: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        execution_lookup = self.zephyr_client.build_execution_lookup()
        results: List[Dict[str, Any]] = []

        for record in records:
            test_case_key = record["test_case_key"]
            status_text = record["status"]
            evidence_file = record["evidence_file"]
            comment = record["comment"]

            result = {
                "test_case_key": test_case_key,
                "status": status_text,
                "execution_id": "",
                "evidence_file": evidence_file,
                "result": "SKIPPED",
                "message": "",
            }

            try:
                execution_id = execution_lookup.get(test_case_key)

                if not execution_id:
                    raise RuntimeError(f"No execution found for test case {test_case_key}")

                result["execution_id"] = execution_id

                status_id = map_status(status_text)

                self.zephyr_client.update_execution_status(
                    execution_id=execution_id,
                    status_id=status_id,
                    comment=comment,
                )

                if evidence_file:
                    evidence_path = self.evidence_dir / evidence_file
                    self.zephyr_client.upload_attachment(
                        execution_id=execution_id,
                        evidence_path=str(evidence_path),
                    )

                result["result"] = "SUCCESS"
                result["message"] = "Updated successfully"

            except Exception as exc:
                result["result"] = "FAILED"
                result["message"] = str(exc)

            results.append(result)

        return results