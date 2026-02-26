# AGENTS.md — uptimerobot-mcp

## Project Overview

Python MCP (Model Context Protocol) server for the UptimeRobot API v2, built with FastMCP 3.x.
Repository: `github.com/84em/uptimerobot-mcp`

## Architecture

```
src/uptimerobot_mcp/
  server.py          # FastMCP instance + tool registration entry point
  client.py          # Async HTTP client (httpx); reads UPTIMEROBOT_API_KEY from env
  validation.py      # Input validation helpers (pagination, interval, statuses, etc.)
  __main__.py        # CLI entry point
  tools/
    account.py       # get_account_details
    monitors.py      # get_monitors, get_monitor, create_monitor, edit_monitor,
                     # delete_monitor, reset_monitor, get_monitor_logs
    contacts.py      # get_alert_contacts, create_alert_contact,
                     # edit_alert_contact, delete_alert_contact
    maintenance.py   # get_mwindows, create_mwindow, edit_mwindow, delete_mwindow
tests/
  test_integration.py  # Integration tests against real UptimeRobot API v2
```

## Environment

Requires `UPTIMEROBOT_API_KEY` in the environment (or a `.env` file).
The key is available from the UptimeRobot dashboard under **Integrations & API → API**.

Local `.env` maps from the workspace shared env:
- Workspace key: `UPTIME_ROBOT_KEY`
- Required key name: `UPTIMEROBOT_API_KEY`

## Development Commands

```bash
uv sync --group dev          # Install all dependencies including dev
uv run ruff check .          # Lint
uv run ruff format .         # Format
uv run mypy src/             # Type check (strict mode)
uv run pytest                # Run integration tests (requires UPTIMEROBOT_API_KEY)
```

## Conventions

- All tools follow the `register_*_tools(mcp: FastMCP)` pattern with closures.
- All API parameters are validated before calling `call_api()`.
- All type annotations use `dict[str, Any]` (never bare `dict`).
- Line length: 100 characters (ruff enforced).
- Python 3.12+ required.
- Conventional Commits for all commit messages.
- Semantic Versioning for releases.
- Keep a Changelog format for `CHANGELOG.md`.

## Testing

Integration tests use the real UptimeRobot API — no mocks.
CRUD monitor tests target `https://84em.blog` with name `"84em.blog - MCP Integration Test"`.
Alert contact creation is skipped gracefully on free-plan API limit errors.

## Git Workflow

- Never commit to `main` directly — use branches and PRs.
- Never push to `main`.
- Tag releases following `vX.Y.Z` format.
- Never commit `.env` or any file in `.gitignore`.
