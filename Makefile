.PHONY: help install version run run-stdio inspector mcp-dev client client-http list list-http inspect

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

install: ## Install / sync dependencies
	uv sync

version: ## Show FastMCP and MCP versions
	uv run fastmcp version
	uv run mcp version

run: ## Start server over HTTP (port 8000)
	uv run python my_server.py

run-stdio: ## Start server over stdio (for Cursor / Claude)
	uv run fastmcp run my_server.py:mcp

inspector: ## Open MCP Inspector (for FastMCP servers)
	uv run fastmcp dev inspector my_server.py:mcp

mcp-dev: inspector ## Alias — use FastMCP inspector (mcp CLI needs MCPServer, not FastMCP)

client: ## Test tools in-process (no HTTP server needed)
	uv run python my_client.py

client-http: ## Test tools over HTTP (need: make run in another terminal)
	uv run python my_client.py --http

list: ## List tools from my_server.py (in-process via stdio)
	uv run fastmcp list my_server.py --input-schema

list-http: ## List tools on running HTTP server (need: make run)
	uv run fastmcp list http://127.0.0.1:8000/mcp --input-schema

inspect: ## Inspect server without running a host
	uv run fastmcp inspect my_server.py
