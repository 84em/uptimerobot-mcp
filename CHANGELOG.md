# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-02-26

### Added
- Initial release
- `get_monitors` - list all monitors with filtering by status and search term
- `get_monitor` - retrieve a single monitor with logs, response times, and contacts
- `create_monitor` - create HTTP(S), Keyword, Ping, Port, and Heartbeat monitors
- `edit_monitor` - update monitor properties including pause/resume
- `delete_monitor` - permanently remove a monitor
- `reset_monitor` - clear all historical statistics for a monitor
- `get_monitor_logs` - retrieve up/down event logs for a monitor
- `get_account_details` - retrieve account stats and monitor limits
- `get_alert_contacts` - list all alert contacts
- `create_alert_contact` - add a new alert contact (email, SMS, Slack, webhook, etc.)
- `edit_alert_contact` - update an existing alert contact
- `delete_alert_contact` - remove an alert contact
- `get_mwindows` - list all maintenance windows
- `create_mwindow` - schedule one-time or recurring maintenance windows
- `edit_mwindow` - update maintenance window schedule or duration
- `delete_mwindow` - remove a maintenance window
- Environment variable-based credential management (`UPTIMEROBOT_API_KEY`)
- `.env` file support via python-dotenv

[Unreleased]: https://github.com/84em/uptimerobot-mcp/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/84em/uptimerobot-mcp/releases/tag/v1.0.0
