# agents-monitor-people

[![Version](https://img.shields.io/badge/version-v0.2.2-blue)](https://github.com/civic-interconnect/agents-monitor-people/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/civic-interconnect/agents-monitor-people/actions/workflows/agent-runner.yml/badge.svg)](https://github.com/civic-interconnect/agents-monitor-people/actions)

> People and Roles Agent for Civic Interconnect

This agent queries basic people and roles metadata from OpenStates using their GraphQL API.
It creates daily snapshot reports of counts by jurisdiction to help track overall system volume and schema stability.

## Current Status

- Pulls OpenStates peoples via GraphQL (high-level people IDs only)
- Generates daily jurisdiction-level summary reports
- Introspection/schema monitoring not yet enabled
- Deeper people content monitoring (texts, sponsors, versions, etc.) not yet implemented

## Deployment

This agent is scheduled to run automatically using GitHub Actions.

## Local Development

See [DEVELOPER.md](./DEVELOPER.md). Then:

```shell
people-agent start
```
