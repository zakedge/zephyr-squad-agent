from typing import Dict


STATUS_MAP: Dict[str, int] = {
    "PASS": 1,
    "FAIL": 2,
    "WIP": 3,
    "BLOCKED": 4,
    "UNEXECUTED": -1,
}


def map_status(status: str) -> int:
    if status is None:
        raise ValueError("Status cannot be empty")

    normalized = str(status).strip().upper()

    if normalized not in STATUS_MAP:
        allowed = ", ".join(STATUS_MAP.keys())
        raise ValueError(f"Invalid status '{status}'. Allowed values: {allowed}")

    return STATUS_MAP[normalized]