# Timeline Visualization Tool

A tool for visualizing agent activities through interactive timelines and knowledge graphs. This project captures detailed proof of work from agent executions and transforms them into rich, interactive visualizations.

## Overview

This tool provides a multi-view visualization system for agent activities:

1. **Knowledge Graph View**: Shows relationships between agents, steps, tool calls, and observations
2. **Timeline View**: Displays agent activities chronologically in a swimlane format
3. **Messages Panel**: Lists all nodes with detailed information available on click

The visualization helps analyze agent behavior, understand tool usage patterns, and debug complex workflows.

## Workflow

The typical workflow consists of two main steps:

1. **Run the agent and generate proof of work**:
   ```
   python main.py
   ```
   - Enter your task when prompted
   - The agent will execute the task using available tools
   - When finished, type `exit` to quit and save the proof of work JSON

2. **Generate the visualization**:
   ```
   python viz_multi_view.py output/proof_of_work_TIMESTAMP.json
   ```
   - This creates an HTML file with the interactive visualization
   - Open the HTML file in any modern web browser

## Usage

### Running the Agent

```bash
python main.py
```

When prompted, enter your task. For example:
```
Enter task (or 'exit' to quit): Find information about climate change initiatives in Europe
```

The agent will execute the task and display its steps in real-time. When finished, type `exit` to quit and save the proof of work JSON file to the `output` directory.

### Generating the Visualization

```bash
python viz_multi_view.py output/proof_of_work_TIMESTAMP.json
```

Options:
- `-o, --output`: Specify output HTML file path
- `--title`: Set a custom title for the visualization

Example:
```bash
python viz_multi_view.py output/proof_of_work_20250429_182651.json --title "Climate Change Research" -o climate_viz.html
```

## Components

### main.py
An interactive CLI that:
- Initializes a CodeAgent with the `visit_webpage` tool
- Processes user tasks and records detailed step information
- Saves comprehensive proof of work as a JSON file

### build_knowledge_graph.py
Builds a directed graph representation of agent activities:
- Nodes represent agents, steps, tool calls, and observations
- Edges represent relationships between these elements
- Can export graphs in GEXF, GraphML, or JSON formats

### build_timeline_data.py
Converts proof of work data into timeline visualization format:
- Creates swimlanes for each agent
- Positions actions and tool calls chronologically
- Preserves hierarchical relationships between steps

### viz_multi_view.py
Generates an HTML visualization with three integrated views:
- Knowledge graph using vis-network
- Timeline using vis-timeline
- Messages panel with detailed node information
- Includes interactive features like node selection and view switching
