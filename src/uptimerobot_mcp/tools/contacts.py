"""Alert contact management tools for UptimeRobot MCP."""

from __future__ import annotations

from fastmcp import FastMCP

from uptimerobot_mcp.client import call_api


def register_contact_tools(mcp: FastMCP) -> None:
    """Register all alert contact tools with the MCP server."""

    @mcp.tool()
    async def get_alert_contacts(
        offset: int = 0,
        limit: int = 50,
    ) -> dict:
        """
        Get all alert contacts.

        Args:
            offset: Pagination offset (default 0).
            limit: Number of contacts to return, max 50 (default 50).
        """
        return await call_api(
            "getAlertContacts",
            {"offset": offset, "limit": limit},
        )

    @mcp.tool()
    async def create_alert_contact(
        type: int,
        friendly_name: str,
        value: str,
    ) -> dict:
        """
        Create a new alert contact.

        Args:
            type: Contact type. 1=SMS, 2=Email, 3=Twitter DM, 5=Webhook,
                6=Pushbullet, 7=Zapier, 9=Pushover, 10=HipChat, 11=Slack.
            friendly_name: Display name for the contact.
            value: Contact destination. Email address for type 2, phone number
                for type 1, webhook URL for type 5, etc.
        """
        params: dict = {
            "type": type,
            "friendly_name": friendly_name,
            "value": value,
        }
        return await call_api("newAlertContact", params)

    @mcp.tool()
    async def edit_alert_contact(
        contact_id: int,
        friendly_name: str | None = None,
        value: str | None = None,
    ) -> dict:
        """
        Edit an existing alert contact.

        Args:
            contact_id: The alert contact ID to edit.
            friendly_name: New display name.
            value: New contact destination (email, phone, URL, etc.).
        """
        params: dict = {"id": contact_id}
        if friendly_name is not None:
            params["friendly_name"] = friendly_name
        if value is not None:
            params["value"] = value
        return await call_api("editAlertContact", params)

    @mcp.tool()
    async def delete_alert_contact(contact_id: int) -> dict:
        """
        Delete an alert contact by ID.

        Args:
            contact_id: The alert contact ID to delete.
        """
        return await call_api("deleteAlertContact", {"id": contact_id})
