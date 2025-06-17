# agents-monitor-people

> People Monitor Agent for Civic Interconnect 

[![Version](https://img.shields.io/badge/version-v0.1.0-blue)](https://github.com/civic-interconnect/agents-monitor-people/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/civic-interconnect/agents-monitor-people/actions/workflows/agent-runner.yml/badge.svg)](https://github.com/civic-interconnect/agents-monitor-people/actions)

This agent queries basic people metadata from OpenStates using their GraphQL API.
It creates daily snapshot reports of people counts by jurisdiction to help track overall system volume and schema stability.

## Current Status

- Pulls OpenStates peoples via GraphQL (high-level people IDs only)
- Generates daily jurisdiction-level summary reports
- Introspection/schema monitoring not yet enabled
- Deeper people content monitoring (texts, sponsors, versions, etc.) not yet implemented

## Local development

```powershell
py -m venv .venv
.\.venv\Scripts\activate
py -m pip install --upgrade pip setuptools wheel --prefer-binary
py -m pip install --upgrade -r requirements.txt --timeout 100
py main.py
```

## Deployment

This agent is scheduled to run automatically using GitHub Actions.

## Before Starting Changes

```shell
git pull
```

## After Tested Changes (New Version Release)

```shell
git add .
git commit -m "Release: agents-monitor-people v0.1.0"
git push origin main
git tag v0.1.0
git push origin v0.1.0
```
