from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from pydantic import Field

mcp = FastMCP("My MCP Server")

docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures",
    "outlook.pdf": "This document presents the projected future performance of the system",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment"
}


def _require_doc(doc_id: str) -> str:
    if doc_id not in docs:
        # ToolError = message intentional for the client (no noisy server traceback)
        raise ToolError(
            f"Document '{doc_id}' not found. "
            f"Available: {', '.join(sorted(docs))}"
        )
    return docs[doc_id]


@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string",
)
def read_document(
    doc_id: str = Field(description="The id of the document to read")
):
    return _require_doc(doc_id)


@mcp.tool(
    name="edit_doc_contents",
    description="Edit a document by replacing the contents with new contents",
)
def edit_document(
    doc_id: str = Field(description="The id of the document that will be edited"),
    old_str: str = Field(description="The text to replace. Must match exactly, including whitespace and capitalization."),
    new_str: str = Field(description="The text to replace the old text with. Must match exactly, including whitespace and capitalization."),
):
    content = _require_doc(doc_id)
    docs[doc_id] = content.replace(old_str, new_str)
    return docs[doc_id]

@mcp.resource(
    "docs://documents",
    mime_type="application/json",
)
def list_docs() -> list[str]:
    return list(docs.keys())

@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain",
)
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document '{doc_id}' not found. ")
    return docs[doc_id]

if __name__ == "__main__":
    # 0.0.0.0 = nhận kết nối từ máy khác trong LAN (remote nội bộ)
    # Endpoint MCP: http://<ip-máy-này>:8000/mcp
    mcp.run(transport="http", host="0.0.0.0", port=8000)
