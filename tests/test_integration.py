"""Integration tests against the real UptimeRobot API v2.

Requires UPTIMEROBOT_API_KEY to be set in the environment.
CRUD tests use https://84em.blog as the test monitor URL.
"""

import os

import pytest

from uptimerobot_mcp.client import call_api

TEST_URL = "https://84em.blog"
TEST_MONITOR_NAME = "84em.blog - MCP Integration Test"

# Shared state across tests (monitor ID created in test_create)
created_monitor_id: int | None = None
created_contact_id: int | None = None
created_mwindow_id: int | None = None


def require_api_key() -> None:
    if not os.environ.get("UPTIMEROBOT_API_KEY"):
        pytest.skip("UPTIMEROBOT_API_KEY not set")


# ---------------------------------------------------------------------------
# Account
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_account_details() -> None:
    require_api_key()
    result = await call_api("getAccountDetails", {})
    assert result["stat"] == "ok"
    account = result["account"]
    assert "email" in account
    assert "monitor_limit" in account
    up, down = account["up_monitors"], account["down_monitors"]
    print(f"\nAccount: {account['email']}, monitors: {up} up / {down} down")


# ---------------------------------------------------------------------------
# Monitors - list
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_monitors() -> None:
    require_api_key()
    result = await call_api("getMonitors", {"offset": 0, "limit": 10})
    assert result["stat"] == "ok"
    assert "monitors" in result or result.get("pagination", {}).get("total", 0) == 0
    total = result.get("pagination", {}).get("total", 0)
    print(f"\nTotal monitors: {total}")


@pytest.mark.asyncio
async def test_get_monitors_filtered_by_status() -> None:
    require_api_key()
    result = await call_api("getMonitors", {"statuses": "2", "limit": 10})
    assert result["stat"] == "ok"
    monitors = result.get("monitors", [])
    for m in monitors:
        assert m["status"] == 2, (
            f"Expected status 2 (up), got {m['status']} for {m['friendly_name']}"
        )
    print(f"\nUp monitors returned: {len(monitors)}")


# ---------------------------------------------------------------------------
# Monitors - CRUD
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_monitor() -> None:
    global created_monitor_id
    require_api_key()
    result = await call_api(
        "newMonitor",
        {
            "friendly_name": TEST_MONITOR_NAME,
            "url": TEST_URL,
            "type": 1,
            "interval": 300,
        },
    )
    assert result["stat"] == "ok", f"Create failed: {result}"
    created_monitor_id = result["monitor"]["id"]
    assert isinstance(created_monitor_id, int)
    print(f"\nCreated monitor ID: {created_monitor_id}")


@pytest.mark.asyncio
async def test_get_single_monitor() -> None:
    require_api_key()
    if not created_monitor_id:
        pytest.skip("No monitor created yet")
    result = await call_api(
        "getMonitors",
        {
            "monitors": created_monitor_id,
            "logs": 1,
            "alert_contacts": 1,
        },
    )
    assert result["stat"] == "ok"
    monitors = result.get("monitors", [])
    assert len(monitors) == 1
    m = monitors[0]
    assert m["id"] == created_monitor_id
    assert m["friendly_name"] == TEST_MONITOR_NAME
    assert m["url"] == TEST_URL
    print(f"\nFetched monitor: {m['friendly_name']} (status: {m['status']})")


@pytest.mark.asyncio
async def test_edit_monitor() -> None:
    require_api_key()
    if not created_monitor_id:
        pytest.skip("No monitor created yet")
    new_name = TEST_MONITOR_NAME + " (edited)"
    result = await call_api(
        "editMonitor",
        {
            "id": created_monitor_id,
            "friendly_name": new_name,
            "interval": 600,
        },
    )
    assert result["stat"] == "ok", f"Edit failed: {result}"
    assert result["monitor"]["id"] == created_monitor_id
    print(f"\nEdited monitor {created_monitor_id} -> interval 600s")


@pytest.mark.asyncio
async def test_pause_and_resume_monitor() -> None:
    require_api_key()
    if not created_monitor_id:
        pytest.skip("No monitor created yet")
    # Pause
    result = await call_api("editMonitor", {"id": created_monitor_id, "status": 0})
    assert result["stat"] == "ok", f"Pause failed: {result}"
    print(f"\nPaused monitor {created_monitor_id}")

    # Resume
    result = await call_api("editMonitor", {"id": created_monitor_id, "status": 1})
    assert result["stat"] == "ok", f"Resume failed: {result}"
    print(f"Resumed monitor {created_monitor_id}")


@pytest.mark.asyncio
async def test_reset_monitor() -> None:
    require_api_key()
    if not created_monitor_id:
        pytest.skip("No monitor created yet")
    result = await call_api("resetMonitor", {"id": created_monitor_id})
    assert result["stat"] == "ok", f"Reset failed: {result}"
    print(f"\nReset monitor {created_monitor_id}")


@pytest.mark.asyncio
async def test_get_monitor_logs() -> None:
    require_api_key()
    if not created_monitor_id:
        pytest.skip("No monitor created yet")
    result = await call_api(
        "getMonitors",
        {
            "monitors": created_monitor_id,
            "logs": 1,
            "logs_limit": 10,
        },
    )
    assert result["stat"] == "ok"
    monitors = result.get("monitors", [])
    assert len(monitors) == 1
    logs = monitors[0].get("logs", [])
    print(f"\nLogs for monitor {created_monitor_id}: {len(logs)} entries")


@pytest.mark.asyncio
async def test_delete_monitor() -> None:
    require_api_key()
    if not created_monitor_id:
        pytest.skip("No monitor created yet")
    result = await call_api("deleteMonitor", {"id": created_monitor_id})
    assert result["stat"] == "ok", f"Delete failed: {result}"
    assert result["monitor"]["id"] == created_monitor_id
    print(f"\nDeleted monitor {created_monitor_id}")


# ---------------------------------------------------------------------------
# Alert Contacts - CRUD
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_alert_contacts() -> None:
    require_api_key()
    result = await call_api("getAlertContacts", {"limit": 10})
    assert result["stat"] == "ok"
    contacts = result.get("alert_contacts", [])
    print(f"\nAlert contacts: {len(contacts)}")


@pytest.mark.asyncio
async def test_create_alert_contact() -> None:
    global created_contact_id
    require_api_key()
    try:
        result = await call_api(
            "newAlertContact",
            {
                "type": 2,
                "friendly_name": "MCP Test Contact",
                "value": "mcp-test@84em.blog",
            },
        )
    except ValueError as e:
        if "only 1 active alert contact" in str(e) or "not_authorized" in str(e):
            pytest.skip(f"Plan limit reached for alert contacts: {e}")
        raise
    assert result["stat"] == "ok", f"Create contact failed: {result}"
    created_contact_id = result["alertcontact"]["id"]
    print(f"\nCreated alert contact ID: {created_contact_id}")


@pytest.mark.asyncio
async def test_edit_alert_contact() -> None:
    require_api_key()
    if not created_contact_id:
        pytest.skip("No contact created yet")
    result = await call_api(
        "editAlertContact",
        {
            "id": created_contact_id,
            "friendly_name": "MCP Test Contact (edited)",
        },
    )
    assert result["stat"] == "ok", f"Edit contact failed: {result}"
    print(f"\nEdited contact {created_contact_id}")


@pytest.mark.asyncio
async def test_delete_alert_contact() -> None:
    require_api_key()
    if not created_contact_id:
        pytest.skip("No contact created yet")
    result = await call_api("deleteAlertContact", {"id": created_contact_id})
    assert result["stat"] == "ok", f"Delete contact failed: {result}"
    print(f"\nDeleted contact {created_contact_id}")


# ---------------------------------------------------------------------------
# Maintenance Windows - CRUD
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_mwindows() -> None:
    require_api_key()
    result = await call_api("getMWindows", {"limit": 10})
    assert result["stat"] == "ok"
    windows = result.get("mwindows", [])
    print(f"\nMaintenance windows: {len(windows)}")


@pytest.mark.asyncio
async def test_create_mwindow() -> None:
    global created_mwindow_id
    require_api_key()
    # Daily window: start_time is HH:MM for recurring types (2/3/4)
    result = await call_api(
        "newMWindow",
        {
            "friendly_name": "MCP Test Window",
            "type": 2,
            "start_time": "02:00",
            "duration": 30,
        },
    )
    assert result["stat"] == "ok", f"Create mwindow failed: {result}"
    created_mwindow_id = result["mwindow"]["id"]
    print(f"\nCreated maintenance window ID: {created_mwindow_id}")


@pytest.mark.asyncio
async def test_edit_mwindow() -> None:
    require_api_key()
    if not created_mwindow_id:
        pytest.skip("No mwindow created yet")
    result = await call_api(
        "editMWindow",
        {
            "id": created_mwindow_id,
            "friendly_name": "MCP Test Window (edited)",
            "duration": 60,
        },
    )
    assert result["stat"] == "ok", f"Edit mwindow failed: {result}"
    print(f"\nEdited mwindow {created_mwindow_id}")


@pytest.mark.asyncio
async def test_delete_mwindow() -> None:
    require_api_key()
    if not created_mwindow_id:
        pytest.skip("No mwindow created yet")
    result = await call_api("deleteMWindow", {"id": created_mwindow_id})
    assert result["stat"] == "ok", f"Delete mwindow failed: {result}"
    print(f"\nDeleted mwindow {created_mwindow_id}")
