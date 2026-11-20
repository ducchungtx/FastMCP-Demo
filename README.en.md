# MCP Quickstart (FastMCP Demo)

[![en](https://img.shields.io/badge/lang-English-0A66C2?style=flat-square&logo=googletranslate&logoColor=white)](README.en.md)
[![vi](https://img.shields.io/badge/lang-Tiếng_Việt-DA251D?style=flat-square)](README.md)

**Languages:** [🇬🇧 English](README.en.md) · [🇻🇳 Tiếng Việt](README.md)

---

Demo MCP server built with [FastMCP](https://gofastmcp.com): mock document store (read/edit tools + read-only resources), connectable from Cursor, VS Code / Copilot, or a Python client.

## Requirements

- Python **3.13+**
- [uv](https://docs.astral.sh/uv/) (recommended via Homebrew: `brew install uv`)

## Setup

```bash
uv sync
make version   # verify FastMCP / MCP SDK
```

## Available tools

| Tool | Description |
|------|-------------|
| `read_doc_contents` | Read document content by `doc_id` |
| `edit_doc_contents` | Replace text in a document (`old_str` → `new_str`) |

Sample docs: `deposition.md`, `report.pdf`, `financials.docx`, `outlook.pdf`, `plan.md`, `spec.txt`.

## Available resources

| URI | Mime | Description |
|-----|------|-------------|
| `docs://documents` | `application/json` | List all `doc_id` values |
| `docs://documents/{doc_id}` | `text/plain` | Read one document’s content |

Concrete URI examples: `docs://documents/plan.md`, `docs://documents/report.pdf`.

| | Tool | Resource |
|---|------|----------|
| How you address it | Tool name + args (`doc_id`, …) | URI like an address (`docs://…`) |
| Best for | Read **and** write (side effects) | Read-only content |
| In Cursor | Agent calls the tool on request | Agent calls `FetchMcpResource` with the URI |

> A resource is **not** a browser URL. The host connects over MCP and sends `resources/read` with the URI.

## Quick commands (Makefile)

```bash
make help          # list targets

make list          # list tools (in-process)
make client        # test client in-process (no HTTP needed)
make inspector     # open MCP Inspector in the browser

make run           # HTTP server → http://127.0.0.1:8000/mcp
make client-http   # test client over HTTP (run make run first)
make list-http     # list tools over HTTP
```

> **Note:** use the `fastmcp` CLI with this project. The MCP SDK command `mcp dev` will **not** work — this server is `FastMCP`, not `MCPServer`.

## Two ways to connect a host (Cursor / VS Code)

### 1. Local stdio — IDE launches the server

Cursor spawns `uv` → `fastmcp run my_server.py:mcp`.  
No `make run` needed. Best for local development.

### 2. Remote HTTP — IDE calls a URL

1. Terminal: `make run` (server listens on `0.0.0.0:8000`)
2. Point the host at `http://127.0.0.1:8000/mcp` (other LAN machines: `http://<this-machine-ip>:8000/mcp`)

Good for a “one server, many clients” demo (marketing / other machines).

## Cursor configuration

File: [`.cursor/mcp.json`](.cursor/mcp.json) (both servers are already defined):

- **My MCP Server (stdio local)** — enable and use immediately
- **My MCP Server (remote HTTP)** — requires `make run` first

In Cursor: **Settings → MCP** → enable a server (test **one** at a time to avoid duplicate tools).

Try in chat:

- Tool: *“read plan.md using the tool”*
- Resource list: *`docs://documents`* or *“list documents via resource”*
- One file: *`docs://documents/plan.md`* or *“contents of docs://documents/plan.md”*

The agent will call MCP (tool or `FetchMcpResource`) — no need to open a link in the browser.

## VS Code / Copilot configuration

File: [`.vscode/mcp.json`](.vscode/mcp.json) — same two entries, but under the `servers` key (not `mcpServers`).

## Python client (test / integration)

[`my_client.py`](my_client.py) follows the [FastMCP Client](https://gofastmcp.com/docs/clients/client.md) guide:

```bash
# In-process: Client(mcp) — no HTTP needed
uv run python my_client.py

# HTTP remote
make run   # other terminal
uv run python my_client.py --http
```

Call a single tool via CLI:

```bash
uv run fastmcp call my_server.py read_doc_contents --input-json '{"doc_id":"plan.md"}'
```

## Project layout

```
my_server.py      # FastMCP server: tools + resources
my_client.py      # Client demo (in-process / HTTP)
Makefile          # Common commands
.cursor/mcp.json  # Cursor config (stdio + HTTP)
.vscode/mcp.json  # VS Code / Copilot config
README.md         # Tiếng Việt
README.en.md      # English
```

## References

- [FastMCP Quickstart](https://gofastmcp.com/docs/getting-started/quickstart)
- [FastMCP Resources](https://gofastmcp.com/servers/resources)
- [FastMCP Client](https://gofastmcp.com/docs/clients/client)
- [Install into Cursor / Claude / …](https://gofastmcp.com/docs/cli/install-mcp)
- [HTTP deployment](https://gofastmcp.com/docs/deployment/http)
