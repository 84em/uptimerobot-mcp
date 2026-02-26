"""Account tools for UptimeRobot MCP."""

from fastmcp import FastMCP

from uptimerobot_mcp.client import call_api


def register_account_tools(mcp: FastMCP) -> None:
    """Register account tools with the MCP server."""

    @mcp.tool()
    async def get_account_details() -> dict:
        """
        Get UptimeRobot account details.

        Returns account information including email, monitor limits,
        and counts of up, down, and paused monitors.
        """
        return await call_api("getAccountDetails", {})
