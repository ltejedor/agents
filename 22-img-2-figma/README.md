<!--
Documentation for the image-to-FigJam whiteboard importer.
--> 
# Image-to-FigJam Whiteboard Importer

This directory contains tools to parse a whiteboard image into structured elements and recreate that board in FigJam via an MCP server and plugin.

## Overview

- **`image_to_data.py`**: Stub module where you should implement `parse_whiteboard(image_path)`. This function should analyze an image (e.g. via OCR or layout analysis) and return a list of elements:
  ```js
  [
    { type: 'sticky', text: 'Note', x: 100, y: 200 },
    { type: 'connector', start_id: '0', end_id: '1' },
    // ...
  ]
  ```
- **`main.py`**: CLI agent built on [smolagents](https://github.com/openai/smolagents). Provides tools to enqueue FigJam actions:
  - `create_sticky(text, x, y)`
  - `move_node(id, x, y)`
  - `start_timer(seconds)`
  - `create_connector(start_id?, end_id?)`
  - `ingest_whiteboard(image_path)`
- **`MCPJam/`**: The FigJam plugin that polls the MCP server and applies the queued commands on the canvas.

## Getting Started

1. **Ensure Python dependencies** (in your project environment):
   ```bash
   pip install smolagents requests python-dotenv
   ```
2. **Run the MCP server** (from its folder):
   ```bash
   cd mcp-servers/mcp_server
   uvicorn main:app --reload --port 8787
   ```
3. **Build the FigJam plugin**:
   ```bash
   cd 22-img-2-figma/MCPJam
   npm install
   npm run build
   ```
   Then load it in FigJam development mode using the generated `manifest.json` and `code.js`.
4. **Launch the CLI agent**:
   ```bash
   cd 22-img-2-figma
   python main.py
   ```
5. **Import a whiteboard** (in the agent REPL):
   ```text
   Enter command> ingest_whiteboard path/to/whiteboard.png
   ```
   The agent will parse the image, enqueue the corresponding sticky and connector commands, and the FigJam plugin will render them.

## Extending Image Parsing

- Implement the `parse_whiteboard(image_path)` function in `image_to_data.py` using your preferred vision/ML tools.
- Output element dictionaries with fields matching the supported commands.

## Standalone Plugin & Server

If you only need the FigJam plugin and MCP server (no image import), see the [figjam-mcp-and-plugin](https://github.com/ltejedor/figjam-mcp-and-plugin) repository for a ready-to-use setup.