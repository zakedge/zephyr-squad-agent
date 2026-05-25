from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

from src.config import Settings
from src.zephyr_auth import generate_jwt_token


class ZephyrClient:
    def __init__(self, settings: Settings):
        self.settings = settings

    def _headers(self, method: str, api_path: str) -> Dict[str, str]:
        token = generate_jwt_token(
            access_key=self.settings.zephyr_access_key,
            secret_key=self.settings.zephyr_secret_key,
            account_id=self.settings.zephyr_account_id,
            method=method,
            api_path=api_path,
        )

        return {
            "Authorization": f"JWT {token}",
            "zapiAccessKey": self.settings.zephyr_access_key,
            "Content-Type": "application/json",
        }

    def get_executions_for_cycle(self) -> List[Dict[str, Any]]:
        api_path = f"/public/rest/api/1.0/executions/search/cycle/{self.settings.cycle_id}"
        url = f"{self.settings.zephyr_base_url}{api_path}"

        params = {
            "projectKey": self.settings.project_key,
            "versionId": self.settings.version_id,
        }

        response = requests.get(
            url,
            headers=self._headers("GET", api_path),
            params=params,
            timeout=30,
        )

        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):
            return data

        if "executions" in data:
            return data["executions"]

        if "searchObjectList" in data:
            return data["searchObjectList"]

        return []

    def build_execution_lookup(self) -> Dict[str, str]:
        executions = self.get_executions_for_cycle()
        lookup: Dict[str, str] = {}

        for item in executions:
            issue_key = (
                item.get("issueKey")
                or item.get("issue", {}).get("key")
                or item.get("execution", {}).get("issueKey")
            )

            execution_id = (
                item.get("executionId")
                or item.get("id")
                or item.get("execution", {}).get("id")
            )

            if issue_key and execution_id:
                lookup[str(issue_key)] = str(execution_id)

        return lookup

    def update_execution_status(
        self,
        execution_id: str,
        status_id: int,
        comment: str = "",
    ) -> Dict[str, Any]:
        api_path = f"/public/rest/api/1.0/execution/{execution_id}/execute"
        url = f"{self.settings.zephyr_base_url}{api_path}"

        payload = {
            "status": {"id": status_id},
            "comment": comment,
        }

        response = requests.put(
            url,
            headers=self._headers("PUT", api_path),
            json=payload,
            timeout=30,
        )

        response.raise_for_status()
        return response.json() if response.text else {}

    def upload_attachment(
        self,
        execution_id: str,
        evidence_path: str,
    ) -> Optional[Dict[str, Any]]:
        file_path = Path(evidence_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Evidence file not found: {evidence_path}")

        api_path = "/public/rest/api/1.0/attachment"
        url = f"{self.settings.zephyr_base_url}{api_path}"

        token = generate_jwt_token(
            access_key=self.settings.zephyr_access_key,
            secret_key=self.settings.zephyr_secret_key,
            account_id=self.settings.zephyr_account_id,
            method="POST",
            api_path=api_path,
        )

        headers = {
            "Authorization": f"JWT {token}",
            "zapiAccessKey": self.settings.zephyr_access_key,
        }

        data = {
            "entityId": execution_id,
            "entityType": "EXECUTION",
        }

        with open(file_path, "rb") as file_obj:
            files = {"file": (file_path.name, file_obj)}
            response = requests.post(
                url,
                headers=headers,
                data=data,
                files=files,
                timeout=60,
            )

        response.raise_for_status()
        return response.json() if response.text else None