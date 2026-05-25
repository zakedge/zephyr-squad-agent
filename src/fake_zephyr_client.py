from typing import Any, Dict, List


class FakeZephyrClient:
    """
    Local fake Zephyr client for testing the full CLI flow.

    It does not call Jira or Zephyr.
    It creates fake execution IDs from the input test case keys.
    """

    def __init__(self, test_case_keys: List[str]):
        self.test_case_keys = test_case_keys
        self.updated: List[Dict[str, Any]] = []
        self.uploaded: List[Dict[str, Any]] = []

    def build_execution_lookup(self) -> Dict[str, str]:
        lookup: Dict[str, str] = {}

        for index, test_case_key in enumerate(self.test_case_keys, start=1001):
            lookup[test_case_key] = str(index)

        return lookup

    def update_execution_status(
        self,
        execution_id: str,
        status_id: int,
        comment: str = "",
    ) -> Dict[str, Any]:
        self.updated.append(
            {
                "execution_id": execution_id,
                "status_id": status_id,
                "comment": comment,
            }
        )
        return {}

    def upload_attachment(
        self,
        execution_id: str,
        evidence_path: str,
    ) -> Dict[str, Any]:
        self.uploaded.append(
            {
                "execution_id": execution_id,
                "evidence_path": evidence_path,
            }
        )
        return {}