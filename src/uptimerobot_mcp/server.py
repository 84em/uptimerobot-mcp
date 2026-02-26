"""UptimeRobot MCP server entry point."""

from fastmcp import FastMCP

from uptimerobot_mcp.tools.account import register_account_tools
from uptimerobot_mcp.tools.contacts import register_contact_tools
from uptimerobot_mcp.tools.maintenance import register_maintenance_tools
from uptimerobot_mcp.tools.monitors import register_monitor_tools


def create_server() -> FastMCP:
    """Create and configure the UptimeRobot MCP server."""
    mcp = FastMCP(
        "UptimeRobot MCP",
        instructions=(
            "MCP server for managing UptimeRobot monitors, alert contacts, and "
            "maintenance windows via the UptimeRobot API v2. "
            "Requires the UPTIMEROBOT_API_KEY environment variable."
        ),
    )

    register_monitor_tools(mcp)
    register_account_tools(mcp)
    register_contact_tools(mcp)
    register_maintenance_tools(mcp)

    return mcp


mcp = create_server()


def main() -> None:
    """CLI entry point."""
    mcp.run()


if __name__ == "__main__":
    main()
