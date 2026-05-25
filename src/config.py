import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    jira_base_url: str
    zephyr_base_url: str
    zephyr_access_key: str
    zephyr_secret_key: str
    zephyr_account_id: str
    project_key: str
    cycle_id: str
    version_id: str


def get_settings() -> Settings:
    required_vars = [
        "JIRA_BASE_URL",
        "ZEPHYR_BASE_URL",
        "ZEPHYR_ACCESS_KEY",
        "ZEPHYR_SECRET_KEY",
        "ZEPHYR_ACCOUNT_ID",
        "PROJECT_KEY",
        "CYCLE_ID",
        "VERSION_ID",
    ]

    missing = [key for key in required_vars if not os.getenv(key)]

    if missing:
        raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")

    return Settings(
        jira_base_url=os.getenv("JIRA_BASE_URL", "").rstrip("/"),
        zephyr_base_url=os.getenv("ZEPHYR_BASE_URL", "").rstrip("/"),
        zephyr_access_key=os.getenv("ZEPHYR_ACCESS_KEY", ""),
        zephyr_secret_key=os.getenv("ZEPHYR_SECRET_KEY", ""),
        zephyr_account_id=os.getenv("ZEPHYR_ACCOUNT_ID", ""),
        project_key=os.getenv("PROJECT_KEY", ""),
        cycle_id=os.getenv("CYCLE_ID", ""),
        version_id=os.getenv("VERSION_ID", "-1"),
    )