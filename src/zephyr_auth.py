import time
import jwt


def generate_jwt_token(
    access_key: str,
    secret_key: str,
    account_id: str,
    method: str,
    api_path: str,
) -> str:
    """
    Temporary JWT generator.

    Zephyr Squad Cloud requires JWT auth.
    We will later replace qsh with real query-string-hash signing.
    """
    now = int(time.time())

    payload = {
        "sub": account_id,
        "qsh": "context-qsh",
        "iss": access_key,
        "iat": now,
        "exp": now + 3600,
    }

    return jwt.encode(payload, secret_key, algorithm="HS256")