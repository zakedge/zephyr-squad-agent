from typing import Any, Dict, List


def print_execution_summary(executions: List[Dict[str, Any]]) -> None:
    print()
    print("=" * 80)
    print("ZEPHYR EXECUTIONS")
    print("=" * 80)

    if not executions:
        print("No executions found")
        return

    for item in executions:
        issue_key = (
            item.get("issueKey")
            or item.get("issue", {}).get("key")
            or item.get("execution", {}).get("issueKey")
            or "UNKNOWN"
        )

        execution_id = (
            item.get("executionId")
            or item.get("id")
            or item.get("execution", {}).get("id")
            or "UNKNOWN"
        )

        status = (
            item.get("status", {}).get("name")
            or item.get("executionStatus")
            or item.get("execution", {}).get("status", {}).get("name")
            or "UNKNOWN"
        )

        print(
            f"Test Case: {issue_key:<20} "
            f"Execution ID: {execution_id:<15} "
            f"Status: {status}"
        )

    print("=" * 80)