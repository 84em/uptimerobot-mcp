"""Maintenance window management tools for UptimeRobot MCP."""

from __future__ import annotations

from typing import Any

from fastmcp import FastMCP

from uptimerobot_mcp.client import call_api
from uptimerobot_mcp.validation import validate_pagination


def register_maintenance_tools(mcp: FastMCP) -> None:
    """Register all maintenance window tools with the MCP server."""

    @mcp.tool()
    async def get_mwindows(
        offset: int = 0,
        limit: int = 50,
    ) -> dict[str, Any]:
        """
        Get all maintenance windows.

        Args:
            offset: Pagination offset (default 0).
            limit: Number of windows to return, max 50 (default 50).
        """
        validate_pagination(limit, offset)
        return await call_api(
            "getMWindows",
            {"offset": offset, "limit": limit},
        )

    @mcp.tool()
    async def create_mwindow(
        friendly_name: str,
        type: int,
        start_time: str | int,
        duration: int,
        value: str | None = None,
    ) -> dict[str, Any]:
        """
        Create a new maintenance window.

        Args:
            friendly_name: Display name for the maintenance window.
            type: Window recurrence type. 1=Once, 2=Daily, 3=Weekly, 4=Monthly.
            start_time: For type 1 (Once): Unix timestamp (int) of the start time.
                For types 2-4 (recurring): time string in HH:MM format (e.g. "02:00").
            duration: Duration of the window in minutes.
            value: Required for Weekly and Monthly types.
                Weekly (type 3): dash-separated days of week, 1=Mon through 7=Sun.
                    Example: "1-3-5" for Mon/Wed/Fri.
                Monthly (type 4): dash-separated days of month.
                    Example: "1-15" for 1st and 15th.
        """
        params: dict[str, Any] = {
            "friendly_name": friendly_name,
            "type": type,
            "start_time": start_time,
            "duration": duration,
        }
        if value is not None:
            params["value"] = value
        return await call_api("newMWindow", params)

    @mcp.tool()
    async def edit_mwindow(
        mwindow_id: int,
        friendly_name: str | None = None,
        value: str | None = None,
        start_time: str | int | None = None,
        duration: int | None = None,
    ) -> dict[str, Any]:
        """
        Edit an existing maintenance window.

        Args:
            mwindow_id: The maintenance window ID to edit.
            friendly_name: New display name.
            value: New recurrence value (days for weekly/monthly windows).
            start_time: New start time. Unix timestamp (int) for one-time windows,
                HH:MM string for recurring windows.
            duration: New duration in minutes.
        """
        params: dict[str, Any] = {"id": mwindow_id}
        if friendly_name is not None:
            params["friendly_name"] = friendly_name
        if value is not None:
            params["value"] = value
        if start_time is not None:
            params["start_time"] = start_time
        if duration is not None:
            params["duration"] = duration
        return await call_api("editMWindow", params)

    @mcp.tool()
    async def delete_mwindow(mwindow_id: int) -> dict[str, Any]:
        """
        Delete a maintenance window by ID.

        Args:
            mwindow_id: The maintenance window ID to delete.
        """
        return await call_api("deleteMWindow", {"id": mwindow_id})
