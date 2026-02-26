# UptimeRobot MCP

[![CI](https://img.shields.io/github/actions/workflow/status/84em/uptimerobot-mcp/ci.yml?branch=main)](https://github.com/84em/uptimerobot-mcp/actions)
[![License: MIT](https://img.shields.io/github/license/84em/uptimerobot-mcp)](LICENSE)
[![Python versions](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)

A [Model Context Protocol](https://modelcontextprotocol.io/) server for managing [UptimeRobot](https://uptimerobot.com/) monitors, alert contacts, and maintenance windows via the UptimeRobot API v2.

---

## Features

- **16 tools** covering the full UptimeRobot API v2
- Manage monitors (HTTP, Keyword, Ping, Port, Heartbeat)
- Manage alert contacts (email, SMS, Slack, webhooks, and more)
- Schedule and manage maintenance windows
- Retrieve account details and monitor statistics
- Credentials loaded from environment variables only - no secrets in code

---

## Requirements

- Python 3.12+
- A [UptimeRobot](https://uptimerobot.com/) account
- Your UptimeRobot API key from the dashboard under **Integrations & API → API**
- [uv](https://docs.astral.sh/uv/) installed

---

## Installation

### Install from source

```bash
git clone https://github.com/84em/uptimerobot-mcp.git
cd uptimerobot-mcp
uv sync
```

---

## Configuration

Set your UptimeRobot API key as an environment variable:

```bash
export UPTIMEROBOT_API_KEY=u123456-yourApiKeyHere
```

Or create a `.env` file in your working directory (see [.env.example](.env.example)):

```env
UPTIMEROBOT_API_KEY=u123456-yourApiKeyHere
```

Your API key is available in the UptimeRobot dashboard under **Integrations & API → API** in the left sidebar. A read-only API key is also available there if you only need monitoring access.

---

## MCP Client Configuration

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or
`%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "uptimerobot": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/uptimerobot-mcp", "uptimerobot-mcp"],
      "env": {
        "UPTIMEROBOT_API_KEY": "u123456-yourApiKeyHere"
      }
    }
  }
}
```

### Cursor

Add to your Cursor MCP settings:

```json
{
  "mcpServers": {
    "uptimerobot": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/uptimerobot-mcp", "uptimerobot-mcp"],
      "env": {
        "UPTIMEROBOT_API_KEY": "u123456-yourApiKeyHere"
      }
    }
  }
}
```

### Zed

Add to your Zed settings:

```json
{
  "context_servers": {
    "uptimerobot": {
      "command": {
        "path": "uv",
        "args": ["run", "--directory", "/path/to/uptimerobot-mcp", "uptimerobot-mcp"],
        "env": {
          "UPTIMEROBOT_API_KEY": "u123456-yourApiKeyHere"
        }
      }
    }
  }
}
```

---

## Tools

### Monitors

| Tool | Description |
|------|-------------|
| `get_monitors` | List all monitors with optional status/search filtering |
| `get_monitor` | Get a single monitor by ID with logs and response times |
| `create_monitor` | Create a new monitor (HTTP, Keyword, Ping, Port, Heartbeat) |
| `edit_monitor` | Update monitor properties, or pause/resume a monitor |
| `delete_monitor` | Permanently delete a monitor |
| `reset_monitor` | Clear all historical statistics for a monitor |
| `get_monitor_logs` | Get up/down event logs for a monitor |

### Account

| Tool | Description |
|------|-------------|
| `get_account_details` | Get account info, monitor counts, and plan limits |

### Alert Contacts

| Tool | Description |
|------|-------------|
| `get_alert_contacts` | List all alert contacts |
| `create_alert_contact` | Add an alert contact (email, SMS, Slack, webhook, etc.) |
| `edit_alert_contact` | Update an existing alert contact |
| `delete_alert_contact` | Remove an alert contact |

### Maintenance Windows

| Tool | Description |
|------|-------------|
| `get_mwindows` | List all maintenance windows |
| `create_mwindow` | Schedule a one-time or recurring maintenance window |
| `edit_mwindow` | Update a maintenance window's schedule or duration |
| `delete_mwindow` | Remove a maintenance window |

---

## Monitor Types

| Value | Type |
|-------|------|
| `1` | HTTP(S) |
| `2` | Keyword |
| `3` | Ping |
| `4` | Port |
| `5` | Heartbeat |

## Monitor Statuses

| Value | Status |
|-------|--------|
| `0` | Paused |
| `1` | Not checked yet |
| `2` | Up |
| `8` | Seems down |
| `9` | Down |

---

## Development

```bash
git clone https://github.com/84em/uptimerobot-mcp.git
cd uptimerobot-mcp
uv sync --group dev
cp .env.example .env
# Add your UPTIMEROBOT_API_KEY to .env

# Lint
uv run ruff check .

# Format
uv run ruff format .

# Type check
uv run mypy src/

# Run tests
uv run pytest
```

---

## License

[MIT](LICENSE) - Copyright (c) 2026 [84EM LLC](https://84em.com)
