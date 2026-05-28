# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Teaching/demo backend for the [Introduction to Agents with ADK](https://ghacks.dev/hacks/adk-intro) gHack. It contains two independent services that deploy to Cloud Run and talk to each other:

- **`mcp-server/`** — a FastMCP server exposing Compute Engine VM **label** tools (`get_labels`, `add_label`, `remove_label`).
- **`a2a-server/`** — a Google ADK agent (`resource_cleaner_agent`) served over the Agent2Agent (A2A) protocol. It consumes the MCP server's tools plus its own local tools.

## Architecture

The agent is a "Cloud Resource Janitor": it finds VMs whose `janitor-scheduled` label is a date ≤ today, stops them, and removes the label.

- **Tool split** — the agent (`a2a-server/resource_cleaner_agent/agent.py`) composes tools from two sources: an `MCPToolset` pointing at the deployed MCP server (label operations) and local Python functions in `tools.py` (`get_current_date`, `stop_vms`). Label reads/writes live remotely in MCP; VM stop and date logic are local to the agent.
- **Service-to-service auth** — both services deploy with `--no-allow-unauthenticated`. The agent reaches the MCP server using a Google-issued OIDC **ID token** as a Bearer header. `tools.get_bearer_token(audience)` mints this via `google.oauth2.id_token.fetch_id_token`, where the audience is the MCP server's Cloud Run URL (`MCP_SERVER_CLOUD_RUN_URL`).
- **Instance identifier convention** — every tool that touches a VM expects instance strings in the format `project_id/zone/instance_name` and splits on `/`. Keep this format consistent across both services when adding tools.
- **MCP transport** — `streamable-http`, stateless, served at path `/` on `$PORT` (default 8080), bound to `0.0.0.0` (required for Cloud Run).
- **A2A serving** — the agent runs under `adk api_server --a2a` (see `startup.sh`), which auto-discovers the agent package and serves it at `/a2a/resource_cleaner_agent`. `agent.json` is the A2A agent card (capabilities, skills, input/output modes).
- **Model** — `gemini-2.5-flash` via Vertex AI (`GOOGLE_GENAI_USE_VERTEXAI=TRUE`).

## Commands

Each service is a separate `uv` project; run commands from inside its directory.

```shell
# Run MCP server locally (serves on $PORT, default 8080)
cd mcp-server && uv run server.py

# Run the A2A agent locally
cd a2a-server && PORT=8080 ./startup.sh
# or: uv run adk api_server --a2a --host 0.0.0.0 --port 8080 .

# Deploy (run from each service dir; see service README.md for full env vars)
gcloud run deploy mcp-server --no-allow-unauthenticated --source . ...
gcloud run deploy a2a-server --no-allow-unauthenticated --source . ...

# Proxy a deployed service to localhost for testing
gcloud run services proxy --port=8888 mcp-server   # mcp-server
gcloud run services proxy --port=8080 a2a-server   # a2a-server
```

Deployment requires `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, and `GOOGLE_GENAI_USE_VERTEXAI=TRUE` env vars. The a2a-server additionally needs `MCP_SERVER_CLOUD_RUN_URL` set to the deployed MCP server's URL (the README derives it via `gcloud run services describe`). See each service's `README.md` for the exact deploy invocations.

## Conventions

- **Dependencies are pinned** (e.g. `google-adk[a2a]==1.12.0`, `fastmcp==2.12.3`). Keep them pinned when modifying `pyproject.toml`.
- All source files carry the MIT license header (Copyright Murat Eken). Preserve it on existing files and add it to new ones.
- ADK requires the agent to live in a package with a module-level `root_agent` — the package directory name (`resource_cleaner_agent`) is the agent's identity used in the A2A URL and `agent.json`.
