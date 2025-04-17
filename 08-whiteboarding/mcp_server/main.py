"""
Bare‑bones MCP server that exposes:
  • A *tool* → create_sticky(text, x=0, y=0)
  • A pulling endpoint for the FigJam plugin  (/pull?batch=32)
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mcp.server.fastmcp import FastMCP
from typing import Annotated
import job_queue as qmod

app = FastAPI()
server = FastMCP(app)             # registers MCP discovery routes

app.add_middleware(
    CORSMiddleware,
    allow_origins=["null"],
    allow_methods=["*"],            # GET, POST, OPTIONS, etc.
    allow_headers=["*"],            # all headers allowed
    allow_credentials=True,        # plugin fetch() has no credentials
)

# ─────────── MCP TOOL ────────────────────────────────────────────
@server.tool("create_sticky")
def create_sticky(
    text: Annotated[str, "..."],
    x:   Annotated[int, "Canvas X‑coord"] = 0,
    y:   Annotated[int, "Canvas Y‑coord"] = 0,
):
    """
    Enqueue a 'create_sticky' command that the FigJam bridge plugin
    will execute when it polls /pull.
    """
    qmod.push({"op": "create_sticky", "text": text, "x": x, "y": y})
    return "queued"


# ─────────── NON‑MCP helper for the plugin ───────────────────────
@app.get("/pull")
def pull(batch: int | None = 32):
    """FigJam plugin hits this every 2 s and receives queued commands."""
    return qmod.pull(batch)

# handy health check
@app.get("/ping")
def ping():
    return {"pong": True}


# ─────────── entry point ─────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8787, reload=True)
