"""Monitor management tools for UptimeRobot MCP."""

from __future__ import annotations

from typing import Any

from fastmcp import FastMCP

from uptimerobot_mcp.client import call_api
from uptimerobot_mcp.validation import (
    validate_alert_contacts,
    validate_custom_http_headers,
    validate_interval,
    validate_pagination,
    validate_statuses,
    validate_timeout,
)


def register_monitor_tools(mcp: FastMCP) -> None:
    """Register all monitor management tools with the MCP server."""

    @mcp.tool()
    async def get_monitors(
        search: str | None = None,
        statuses: str | None = None,
        offset: int = 0,
        limit: int = 50,
        include_logs: bool = False,
        include_response_times: bool = False,
        include_alert_contacts: bool = False,
        include_mwindows: bool = False,
    ) -> dict[str, Any]:
        """
        Get all monitors with optional filtering.

        Args:
            search: Filter monitors by friendly name (partial match).
            statuses: Filter by status codes, dash-separated. Values: 0=Paused,
                1=Not checked yet, 2=Up, 8=Seems down, 9=Down.
                Example: "2-9" returns up and down monitors only.
            offset: Pagination offset (default 0).
            limit: Number of monitors to return, max 50 (default 50).
            include_logs: Include up/down event logs in response.
            include_response_times: Include response time history in response.
            include_alert_contacts: Include attached alert contacts in response.
            include_mwindows: Include attached maintenance windows in response.
        """
        validate_pagination(limit, offset)
        if statuses:
            validate_statuses(statuses)
        params: dict[str, Any] = {
            "offset": offset,
            "limit": limit,
            "logs": 1 if include_logs else 0,
            "response_times": 1 if include_response_times else 0,
            "alert_contacts": 1 if include_alert_contacts else 0,
            "mwindows": 1 if include_mwindows else 0,
        }
        if search:
            params["search"] = search
        if statuses:
            params["statuses"] = statuses
        return await call_api("getMonitors", params)

    @mcp.tool()
    async def get_monitor(
        monitor_id: int,
        include_logs: bool = True,
        include_response_times: bool = True,
        include_alert_contacts: bool = True,
        include_mwindows: bool = True,
        logs_limit: int = 25,
        response_times_limit: int = 24,
    ) -> dict[str, Any]:
        """
        Get a single monitor by ID with detailed information.

        Args:
            monitor_id: The UptimeRobot monitor ID.
            include_logs: Include up/down event logs (default True).
            include_response_times: Include response time history (default True).
            include_alert_contacts: Include attached alert contacts (default True).
            include_mwindows: Include attached maintenance windows (default True).
            logs_limit: Number of log entries to return (default 25).
            response_times_limit: Number of response time entries to return (default 24).
        """
        if not (1 <= logs_limit <= 50):
            raise ValueError(f"logs_limit must be between 1 and 50, got {logs_limit}")
        if not (1 <= response_times_limit <= 50):
            raise ValueError(
                f"response_times_limit must be between 1 and 50, got {response_times_limit}"
            )
        params: dict[str, Any] = {
            "monitors": monitor_id,
            "logs": 1 if include_logs else 0,
            "logs_limit": logs_limit,
            "response_times": 1 if include_response_times else 0,
            "response_times_limit": response_times_limit,
            "alert_contacts": 1 if include_alert_contacts else 0,
            "mwindows": 1 if include_mwindows else 0,
        }
        return await call_api("getMonitors", params)

    @mcp.tool()
    async def create_monitor(
        friendly_name: str,
        url: str,
        type: int = 1,
        interval: int = 300,
        timeout: int = 30,
        http_method: int | None = None,
        keyword_type: int | None = None,
        keyword_value: str | None = None,
        keyword_case_type: int | None = None,
        http_auth_type: int | None = None,
        http_auth_user: str | None = None,
        http_auth_secret: str | None = None,
        post_type: str | None = None,
        post_value: str | None = None,
        post_content_type: str | None = None,
        custom_http_headers: str | None = None,
        custom_http_statuses: str | None = None,
        ignore_ssl_errors: bool = False,
        alert_contacts: str | None = None,
    ) -> dict[str, Any]:
        """
        Create a new monitor.

        Args:
            friendly_name: Display name for the monitor.
            url: URL or IP address to monitor.
            type: Monitor type. 1=HTTP(S), 2=Keyword, 3=Ping, 4=Port, 5=Heartbeat.
            interval: Check interval in seconds (60-2592000, default 300).
            timeout: Timeout in seconds (1-300, default 30).
            http_method: HTTP method for HTTP(S) monitors.
                1=HEAD, 2=GET, 3=POST, 4=PUT, 5=PATCH, 6=DELETE, 7=OPTIONS.
            keyword_type: Required for Keyword monitors (type=2).
                1=Keyword exists, 2=Keyword not exists.
            keyword_value: The keyword to search for. Required for type=2.
            keyword_case_type: 0=Case insensitive, 1=Case sensitive.
            http_auth_type: HTTP authentication type. 0=None, 1=Basic, 2=Digest.
            http_auth_user: Username for HTTP authentication.
            http_auth_secret: Credential for HTTP authentication.
            post_type: POST body format: "raw" or "keyvalue".
            post_value: POST body content.
            post_content_type: Content-Type header for POST requests.
                Options: "application/json", "application/x-www-form-urlencoded",
                "text/xml", "text/plain".
            custom_http_headers: JSON string of additional request headers.
                Example: '{"X-Custom-Header":"value"}'.
            custom_http_statuses: Custom HTTP status code mappings.
                Format: "200:1_201:1_404:0" where 1=up, 0=down.
            ignore_ssl_errors: Whether to ignore SSL certificate errors.
            alert_contacts: Alert contacts to attach, format "id_threshold_recurrence".
                Separate multiple contacts with "-". Example: "123_0_0-456_0_0".
        """
        validate_interval(interval)
        validate_timeout(timeout)
        if custom_http_headers is not None:
            validate_custom_http_headers(custom_http_headers)
        if alert_contacts is not None:
            validate_alert_contacts(alert_contacts)
        params: dict[str, Any] = {
            "friendly_name": friendly_name,
            "url": url,
            "type": type,
            "interval": interval,
            "timeout": timeout,
            "ignore_ssl_errors": 1 if ignore_ssl_errors else 0,
        }
        optional_fields: dict[str, Any] = {
            "http_method": http_method,
            "keyword_type": keyword_type,
            "keyword_value": keyword_value,
            "keyword_case_type": keyword_case_type,
            "http_auth_type": http_auth_type,
            "http_username": http_auth_user,
            "http_password": http_auth_secret,
            "post_type": post_type,
            "post_value": post_value,
            "post_content_type": post_content_type,
            "custom_http_headers": custom_http_headers,
            "custom_http_statuses": custom_http_statuses,
            "alert_contacts": alert_contacts,
        }
        params.update({k: v for k, v in optional_fields.items() if v is not None})
        return await call_api("newMonitor", params)

    @mcp.tool()
    async def edit_monitor(
        monitor_id: int,
        friendly_name: str | None = None,
        url: str | None = None,
        interval: int | None = None,
        timeout: int | None = None,
        status: int | None = None,
        http_method: int | None = None,
        keyword_type: int | None = None,
        keyword_value: str | None = None,
        http_auth_type: int | None = None,
        http_auth_user: str | None = None,
        http_auth_secret: str | None = None,
        custom_http_headers: str | None = None,
        custom_http_statuses: str | None = None,
        ignore_ssl_errors: bool | None = None,
        alert_contacts: str | None = None,
    ) -> dict[str, Any]:
        """
        Edit an existing monitor. Only provided fields are updated.

        Args:
            monitor_id: The UptimeRobot monitor ID to edit.
            friendly_name: New display name.
            url: New URL to monitor.
            interval: New check interval in seconds.
            timeout: New timeout in seconds.
            status: Change monitor state. 0=Pause, 1=Resume.
            http_method: New HTTP method (1-7, see create_monitor).
            keyword_type: New keyword match type (1=exists, 2=not exists).
            keyword_value: New keyword to search for.
            http_auth_type: New auth type (0=None, 1=Basic, 2=Digest).
            http_auth_user: New HTTP auth username.
            http_auth_secret: New HTTP auth credential.
            custom_http_headers: New custom headers JSON string.
            custom_http_statuses: New custom status code mappings.
            ignore_ssl_errors: Whether to ignore SSL errors.
            alert_contacts: New alert contacts string (replaces all existing).
        """
        if interval is not None:
            validate_interval(interval)
        if timeout is not None:
            validate_timeout(timeout)
        if custom_http_headers is not None:
            validate_custom_http_headers(custom_http_headers)
        if alert_contacts is not None:
            validate_alert_contacts(alert_contacts)
        params: dict[str, Any] = {"id": monitor_id}
        optional_fields: dict[str, Any] = {
            "friendly_name": friendly_name,
            "url": url,
            "interval": interval,
            "timeout": timeout,
            "status": status,
            "http_method": http_method,
            "keyword_type": keyword_type,
            "keyword_value": keyword_value,
            "http_auth_type": http_auth_type,
            "http_username": http_auth_user,
            "http_password": http_auth_secret,
            "custom_http_headers": custom_http_headers,
            "custom_http_statuses": custom_http_statuses,
            "alert_contacts": alert_contacts,
        }
        params.update({k: v for k, v in optional_fields.items() if v is not None})
        if ignore_ssl_errors is not None:
            params["ignore_ssl_errors"] = 1 if ignore_ssl_errors else 0
        return await call_api("editMonitor", params)

    @mcp.tool()
    async def delete_monitor(monitor_id: int) -> dict[str, Any]:
        """
        Permanently delete a monitor by ID.

        Args:
            monitor_id: The UptimeRobot monitor ID to delete.
        """
        return await call_api("deleteMonitor", {"id": monitor_id})

    @mcp.tool()
    async def reset_monitor(monitor_id: int) -> dict[str, Any]:
        """
        Reset a monitor, clearing all historical statistics and logs.

        Args:
            monitor_id: The UptimeRobot monitor ID to reset.
        """
        return await call_api("resetMonitor", {"id": monitor_id})

    @mcp.tool()
    async def get_monitor_logs(
        monitor_id: int,
        limit: int = 25,
        offset: int = 0,
    ) -> dict[str, Any]:
        """
        Get up/down event logs for a specific monitor.

        Args:
            monitor_id: The UptimeRobot monitor ID.
            limit: Number of log entries to return (default 25).
            offset: Pagination offset (default 0).
        """
        validate_pagination(limit, offset)
        params: dict[str, Any] = {
            "monitors": monitor_id,
            "logs": 1,
            "logs_limit": limit,
            "offset": offset,
        }
        return await call_api("getMonitors", params)
