"""FastMCP client demo for my_server.

Default: in-process Client(mcp) — no HTTP server needed.
HTTP mode: start `make run`, then `uv run python my_client.py --http`.

Docs: https://gofastmcp.com/docs/clients/client.md
"""

from __future__ import annotations

import argparse
import asyncio
import sys

from fastmcp import Client
from fastmcp.client.client import CallToolResult

from my_server import mcp


def build_client(*, use_http: bool) -> Client:
    if use_http:
        # Needs: make run  →  http://127.0.0.1:8000/mcp
        return Client("http://127.0.0.1:8000/mcp")
    # In-memory transport: talks to the FastMCP instance in this process
    return Client(mcp)


def result_text(result: CallToolResult) -> str:
    """Prefer structured .data; fall back to text content blocks."""
    if result.data is not None:
        return str(result.data)
    parts: list[str] = []
    for block in result.content:
        text = getattr(block, "text", None)
        if text is not None:
            parts.append(text)
    return "\n".join(parts) if parts else repr(result)


async def demo(client: Client) -> None:
    async with client:
        # 1) Discover tools + schemas the host/agent would see
        tools = await client.list_tools()
        print("=== tools ===")
        for tool in tools:
            print(f"- {tool.name}: {tool.description}")
            print(f"  input_schema: {tool.input_schema}")

        # 2) Happy path: read → edit → read
        read = await client.call_tool(
            "read_doc_contents",
            {"doc_id": "plan.md"},
        )
        print("\n=== read plan.md ===")
        print(result_text(read))

        edited = await client.call_tool(
            "edit_doc_contents",
            {
                "doc_id": "plan.md",
                "old_str": "implementation",
                "new_str": "rollout",
            },
        )
        print("\n=== after edit ===")
        print(result_text(edited))

        # 3) Meaningful failure (unknown doc) — raise_on_error=False keeps output clean
        print("\n=== expected error ===")
        failed = await client.call_tool(
            "read_doc_contents",
            {"doc_id": "missing.txt"},
            raise_on_error=False,
        )
        print(f"is_error={failed.is_error}")
        print(result_text(failed))


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Call my_server tools via FastMCP Client")
    parser.add_argument(
        "--http",
        action="store_true",
        help="Connect over HTTP (requires make run)",
    )
    args = parser.parse_args(argv)
    asyncio.run(demo(build_client(use_http=args.http)))


if __name__ == "__main__":
    main(sys.argv[1:])
