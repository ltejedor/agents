"""
Bare‑bones MCP server that exposes:
  • A *tool* → create_sticky(text, x=0, y=0)
  • A pulling endpoint for the FigJam plugin  (/pull?batch=32)
"""
"""
HTTP server for FigJam plugin polling (uses job_queue) and optional stdio JSON-RPC mode.
"""
# FastAPI-based HTTP polling server
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# job queue import (support both project-root and mcp_server-root execution)
try:
    from mcp_server import job_queue as qmod
except ImportError:
    import job_queue as qmod

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["null"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/pull")
def pull(batch: int | None = 32):
    """FigJam plugin hits this every 2 s and receives queued commands."""
    return qmod.pull(batch)

# handy health check
@app.get("/ping")
def ping():
    return {"pong": True}

# ─────────── HTTP mounting of MCP tool(s) ─────────────────────────
@app.get("/mcp/create_sticky")
def http_create_sticky(
    text: str,
    x: int = 0,
    y: int = 0,
):
    """
    HTTP endpoint wrapper for the create_sticky MCP tool.
    Allows GET requests to enqueue a sticky-creation command.

    Args:
        text: The text on the post-it.
        x: The x position.
        y: The y position.

    Returns:
        dict: Result of the operation.
    """
    # enqueue the same command as the MCP tool
    qmod.push({"op": "create_sticky", "text": text, "x": x, "y": y})
    return {"result": "queued"}
    
@app.get("/mcp/move_node")
def http_move_node(
    id: str,
    x: int = 0,
    y: int = 0,
):
    """
    HTTP endpoint wrapper for the move_node MCP tool.
    Allows GET requests to enqueue a node-movement command.

    Args:
        id: The ID of the node to move.
        x: The new x position.
        y: The new y position.

    Returns:
        dict: Result of the operation.
    """
    qmod.push({"op": "move_node", "id": id, "x": x, "y": y})
    return {"result": "queued"}

@app.get("/mcp/start_timer")
def http_start_timer(
    seconds: int,
):
    """
    HTTP endpoint wrapper for the start_timer MCP tool.
    Allows GET requests to enqueue a timer-start command.

    Args:
        seconds: The timer duration in seconds.

    Returns:
        dict: Result of the operation.
    """
    qmod.push({"op": "start_timer", "seconds": seconds})
    return {"result": "queued"}

@app.get("/mcp/create_connector")
def http_create_connector(
    start_id: str | None = None,
    end_id: str | None = None,
):
    """
    HTTP endpoint for the create_connector MCP tool.
    Optionally accepts start_id and end_id to connect specific nodes.
    """
    cmd = {"op": "create_connector"}
    if start_id is not None:
        cmd["start_id"] = start_id
    if end_id is not None:
        cmd["end_id"] = end_id
    qmod.push(cmd)
    return {"result": "queued"}


# ─────────── entry point ─────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="MCP server for FigJam plugin: HTTP for plugin, or stdio JSON-RPC for CLI clients"
    )
    parser.add_argument("--stdio", action="store_true",
                        help="Run server over stdin/stdout (JSON-RPC) instead of HTTP")
    parser.add_argument("--host", default="0.0.0.0",
                        help="HTTP host (when not using --stdio)")
    parser.add_argument("--port", type=int, default=8787,
                        help="HTTP port (when not using --stdio)")
    parser.add_argument("--reload", action="store_true",
                        help="Enable HTTP reload (when not using --stdio)")
    args = parser.parse_args()

    # In stdio mode, run JSON-RPC MCP server over stdin/stdout
    if args.stdio:
        # Spawn stdio-mode MCP server and register tools
        from mcp.server.fastmcp import FastMCP
        # Initialize MCP server with a name and optional instructions
        mcp_server = FastMCP(name="MCPJam", instructions="Stdio MCP server for FigJam plugin")
        # Register the create_sticky tool for JSON-RPC clients
        @mcp_server.tool(name="create_sticky")
        def create_sticky_tool(text: str, x: int = 0, y: int = 0):  # noqa: F811
            qmod.push({"op": "create_sticky", "text": text, "x": x, "y": y})
            return "queued"
        @mcp_server.tool(name="move_node")
        def move_node_tool(id: str, x: int = 0, y: int = 0):  # noqa: F811
            qmod.push({"op": "move_node", "id": id, "x": x, "y": y})
            return "queued"
        @mcp_server.tool(name="start_timer")
        def start_timer_tool(seconds: int):  # noqa: F811
            qmod.push({"op": "start_timer", "seconds": seconds})
            return "queued"
        @mcp_server.tool(name="create_connector")
        def create_connector_tool(
            start_id: str | None = None,
            end_id: str | None = None,
        ):  # noqa: F811
            cmd = {"op": "create_connector"}
            if start_id is not None:
                cmd["start_id"] = start_id
            if end_id is not None:
                cmd["end_id"] = end_id
            qmod.push(cmd)
            return "queued"
        # Run the server over stdio
        mcp_server.run("stdio")
    else:
        # Default: HTTP server for FigJam plugin polling and manual calls
        import uvicorn
        # Serve FastAPI app
        uvicorn.run(app, host=args.host, port=args.port, reload=args.reload)
