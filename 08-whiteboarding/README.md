# FigJam MCP Bridge

A **minimal Multi‑Cursor Protocol (MCP) server** that lets any downstream client—such as the companion FigJam plug‑in—spawn sticky notes programmatically.  
It’s perfect for rapid prototyping, white‑boarding bots, or teaching workshops where you want live content to appear on a shared canvas.

---

## Features

* **`/tools/create_sticky`** – enqueue a sticky note (text + x/y) to be rendered in FigJam.
* **`/pull`** – lightweight long‑polling endpoint the plug‑in hits every ~2 s for jobs.
* **CORS‑friendly** – safe defaults for local dev; configurable for prod.
* **Single‑file server** powered by **FastAPI + mcp‑server**.

---

## Quick‑start

### 1 · Clone & set up Python env
```bash
$ git clone https://github.com/ltejedor/agents.git && cd agents/mcp-servers/mcp_server
# Python ≥ 3.11 recommended
$ python -m venv .venv && source .venv/bin/activate
$ pip install -r requirements.txt   # fastapi, uvicorn, mcp‑server, etc.
```

### 2 · Run the server
```bash
$ uvicorn main:app --reload --port 8787
# ▶  Uvicorn running on http://0.0.0.0:8787
```

### 3 · Install & run the FigJam plug‑in
1. Open any FigJam file.
2. **Resources → Development → New Plug‑in…** and load the `MCPJam/` folder.
3. Hit the ▶ Run button—stickies will start appearing as jobs are pulled.

---

## API Overview

```text
GET  /pull                # returns queued commands
GET  /ping                # health check
POST /tools/create_sticky # call the tool directly
POST /tools/call          # generic MCP wrapper
GET  /openapi.json        # full schema
```

### Examples

```bash
# Direct endpoint
curl -X POST http://localhost:8787/tools/create_sticky \
     -H "Content-Type: application/json" \
     -d '{"text":"👋 from curl","x":100,"y":100}'

# Generic MCP wrapper
curl -X POST http://localhost:8787/tools/call \
     -H "Content-Type: application/json" \
     -d '{"name":"create_sticky","arguments":{"text":"via /call","x":200,"y":200}}'
```

---

## Configuration

| Env Var | Default | Description |
|---------|---------|-------------|
| `PORT`  | `8787`  | Port Uvicorn listens on. |
| `ALLOWED_ORIGINS` | `*` | Comma‑separated list for CORS. |

Edit `main.py` if you need finer‑grained CORS control (credentials, headers, etc.).

---

## Troubleshooting

* **404 on `/tools/call`** – you’re on `mcp‑server 0.4.x+`; make sure you mount the router:
  ```python
  mcp_router = FastMCP()
  app.include_router(mcp_router.router, prefix="/tools")
  ```
* **CORS errors in browser console** – if your FigJam iframe sends `credentials: "include"` you must set `allow_credentials=True` *and* avoid the wildcard origin.
* **Stickies never appear** – check the server log for queued jobs and ensure the plug‑in’s `/pull` requests return them.

