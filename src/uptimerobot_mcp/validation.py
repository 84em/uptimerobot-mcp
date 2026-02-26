"""Input validation helpers for UptimeRobot MCP tools."""

import json
import re


def validate_pagination(limit: int, offset: int, max_limit: int = 50) -> None:
    """Validate pagination parameters."""
    if not (1 <= limit <= max_limit):
        raise ValueError(f"limit must be between 1 and {max_limit}, got {limit}")
    if offset < 0:
        raise ValueError(f"offset must be non-negative, got {offset}")


def validate_interval(interval: int) -> None:
    """Validate monitor check interval (60s - 30 days)."""
    if not (60 <= interval <= 2592000):
        raise ValueError(f"interval must be between 60 and 2592000 seconds, got {interval}")


def validate_timeout(timeout: int) -> None:
    """Validate monitor request timeout (1s - 5 min)."""
    if not (1 <= timeout <= 300):
        raise ValueError(f"timeout must be between 1 and 300 seconds, got {timeout}")


def validate_statuses(statuses: str) -> None:
    """Validate statuses filter string format (e.g. '2-9' or '0-2-8-9')."""
    valid_codes = {0, 1, 2, 8, 9}
    if not re.fullmatch(r"[0-9]+(-[0-9]+)*", statuses):
        raise ValueError(
            f"statuses must be dash-separated status codes (e.g. '2-9'), got {statuses!r}"
        )
    for code in statuses.split("-"):
        if int(code) not in valid_codes:
            raise ValueError(
                f"invalid status code {code!r}; valid values are 0, 1, 2, 8, 9"
            )


def validate_alert_contacts(alert_contacts: str) -> None:
    """Validate alert_contacts format: 'id_threshold_recurrence[-id_threshold_recurrence...]'."""
    if not re.fullmatch(r"\d+_\d+_\d+(-\d+_\d+_\d+)*", alert_contacts):
        raise ValueError(
            "alert_contacts must be in 'id_threshold_recurrence' format separated by '-', "
            f"e.g. '123_0_0-456_0_0', got {alert_contacts!r}"
        )


def validate_custom_http_headers(headers: str) -> None:
    """Validate that custom_http_headers is valid JSON."""
    try:
        parsed = json.loads(headers)
    except json.JSONDecodeError as exc:
        raise ValueError(f"custom_http_headers must be valid JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ValueError("custom_http_headers must be a JSON object, not an array or scalar")
