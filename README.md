# MCP Quickstart (FastMCP Demo)

[![vi](https://img.shields.io/badge/lang-Tiếng_Việt-DA251D?style=flat-square)](README.md)
[![en](https://img.shields.io/badge/lang-English-0A66C2?style=flat-square&logo=googletranslate&logoColor=white)](README.en.md)

**Ngôn ngữ:** [🇻🇳 Tiếng Việt](README.md) · [🇬🇧 English](README.en.md)

---

Demo MCP server bằng [FastMCP](https://gofastmcp.com): quản lý nội dung tài liệu giả lập (đọc / sửa), kết nối từ Cursor, VS Code / Copilot, hoặc client Python.

## Yêu cầu

- Python **3.13+**
- [uv](https://docs.astral.sh/uv/) (khuyến nghị cài bằng Homebrew: `brew install uv`)

## Cài đặt

```bash
uv sync
make version   # kiểm tra FastMCP / MCP SDK
```

## Tools hiện có

| Tool | Mô tả |
|------|--------|
| `read_doc_contents` | Đọc nội dung document theo `doc_id` |
| `edit_doc_contents` | Thay thế chuỗi trong document (`old_str` → `new_str`) |

Document mẫu: `plan.md`, `report.pdf`, `spec.txt`, …

## Chạy nhanh (Makefile)

```bash
make help          # danh sách lệnh

make list          # liệt kê tools (in-process)
make client        # test client in-process (không cần HTTP)
make inspector     # mở MCP Inspector trên browser

make run           # HTTP server → http://127.0.0.1:8000/mcp
make client-http   # test client qua HTTP (cần make run trước)
make list-http     # list tools qua HTTP
```

> **Lưu ý:** dùng `fastmcp` CLI với project này. Lệnh `mcp dev` của MCP SDK **không** chạy được vì server là `FastMCP`, không phải `MCPServer`.

## Hai cách kết nối host (Cursor / VS Code)

### 1. Stdio local — IDE tự chạy server

Cursor spawn process `uv` → `fastmcp run my_server.py:mcp`.  
Không cần `make run`. Phù hợp khi đang dev trên máy mình.

### 2. Remote HTTP — IDE chỉ gọi URL

1. Terminal: `make run` (server listen `0.0.0.0:8000`)
2. Host nối tới `http://127.0.0.1:8000/mcp` (máy khác trong LAN: `http://<IP-máy-này>:8000/mcp`)

Phù hợp demo “một server, nhiều client” (marketing / team khác máy).

## Cấu hình Cursor

File: [`.cursor/mcp.json`](.cursor/mcp.json) (đã có sẵn cả hai server):

- **My MCP Server (stdio local)** — bật là dùng được ngay
- **My MCP Server (remote HTTP)** — cần `make run` trước

Trong Cursor: **Settings → MCP** → bật server (nên test **một** server tại một thời điểm để tránh trùng tool).

Chat thử: *“đọc nội dung plan.md bằng tool”*.

## Cấu hình VS Code / Copilot

File: [`.vscode/mcp.json`](.vscode/mcp.json) — cùng hai entry, nhưng key là `servers` (không phải `mcpServers`).

## Client Python (test / tích hợp)

[`my_client.py`](my_client.py) demo theo [FastMCP Client](https://gofastmcp.com/docs/clients/client.md):

```bash
# In-process: Client(mcp) — không cần HTTP
uv run python my_client.py

# HTTP remote
make run   # terminal khác
uv run python my_client.py --http
```

CLI gọi một tool:

```bash
uv run fastmcp call my_server.py read_doc_contents --input-json '{"doc_id":"plan.md"}'
```

## Cấu trúc chính

```
my_server.py      # FastMCP server + tools
my_client.py      # Client demo (in-process / HTTP)
Makefile          # Lệnh thường dùng
.cursor/mcp.json  # Config Cursor (stdio + HTTP)
.vscode/mcp.json  # Config VS Code / Copilot
README.md         # Tiếng Việt
README.en.md      # English
```

## Tài liệu tham khảo

- [FastMCP Quickstart](https://gofastmcp.com/docs/getting-started/quickstart)
- [FastMCP Client](https://gofastmcp.com/docs/clients/client)
- [Install vào Cursor / Claude / …](https://gofastmcp.com/docs/cli/install-mcp)
- [HTTP deployment](https://gofastmcp.com/docs/deployment/http)
