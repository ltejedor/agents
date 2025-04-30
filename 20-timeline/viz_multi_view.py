#!/usr/bin/env python3
"""
viz_multi_view.py

Generate a combined knowledge-graph + timeline + messages HTML visualization
from a proof_of_work JSON provenance.

Usage:
  python viz_multi_view.py proof.json [-o output.html] [--title TITLE]
"""
import os
import json
import argparse
from build_knowledge_graph import build_graph
from build_timeline_data import build_timeline_data
try:
    from pyvis.network import Network
except ImportError:
    raise ImportError("pyvis is required to run this script: pip install pyvis")

def main():
    parser = argparse.ArgumentParser(
        description='Visualize provenance with graph, timeline, and messages panes'
    )
    parser.add_argument('input_json', help='Path to proof_of_work JSON file')
    parser.add_argument('-o', '--output', help='Output HTML file', default=None)
    parser.add_argument('--title', help='Title for the visualization', default=None)
    args = parser.parse_args()

    # Load provenance JSON
    with open(args.input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    provenance = data.get('provenance', {})

    # Build networkx graph and export to vis DataSets
    G = build_graph(provenance)
    net = Network(height='100%', width='100%', directed=True, notebook=False)
    if args.title:
        net.heading = args.title
    net.from_nx(G)
    # Export nodes & edges as lists of dicts
    net_nodes = net.nodes
    net_edges = net.edges

    # Build timeline data (groups and items)
    groups, items = build_timeline_data(provenance)

    # Remove step subgroup rows under root agent but keep action/tool items
    root_agent = provenance.get('root_agent', {}) or {}
    root_name = root_agent.get('name')
    if root_name:
        # Filter out subgroup definitions for root agent steps
        filtered_groups = []
        for g in groups:
            gid = g.get('id')
            if gid == root_name:
                # clear nestedGroups for root agent
                if 'nestedGroups' in g:
                    g['nestedGroups'] = []
                filtered_groups.append(g)
            elif not (isinstance(gid, str) and gid.startswith(f"{root_name}-step-")):
                filtered_groups.append(g)
        groups = filtered_groups
        # Flatten items: move step and tool_call items to root swimlane
        for it in items:
            if it.get('group') == root_name and \
               isinstance(it.get('subgroup'), str) and \
               it['subgroup'].startswith(f"{root_name}-step-"):
                # remove subgroup so item appears on root group
                del it['subgroup']

    # Serialize JSON blobs for embedding
    net_nodes_json = json.dumps(net_nodes, indent=2)
    net_edges_json = json.dumps(net_edges, indent=2)
    groups_json = json.dumps(groups, indent=2)
    items_json = json.dumps(items, indent=2)

    title = args.title or os.path.basename(args.input_json)
    base = os.path.splitext(args.input_json)[0]
    out_file = args.output or f"{base}_multi.html"

    # Generate HTML with three-pane grid: graph | timeline | messages
    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset=\"utf-8\">
  <title>{title}</title>
  <script src=\"https://unpkg.com/vis-network/standalone/umd/vis-network.min.js\"></script>
  <link href=\"https://unpkg.com/vis-timeline/styles/vis-timeline-graph2d.min.css\" rel=\"stylesheet\" />
  <script src=\"https://unpkg.com/vis-timeline/standalone/umd/vis-timeline-graph2d.min.js\"></script>
  <style>
    body {{
      margin: 0;
      font-family: Arial, sans-serif;
      display: grid;
      grid-template-columns: 2fr 1fr;
      grid-template-rows: auto minmax(0, 1fr);
      grid-template-areas:
        "controls controls"
        "main messages";
      height: 100vh;
    }}
    #controls {{
      grid-area: controls;
      padding: 10px;
      border-bottom: 1px solid #ddd;
    }}
    #network, #timeline {{
      grid-area: main;
      position: relative;
      width: 100%;   /* fill available grid column */
      height: 100%;  /* fill available grid row */
    }}
    #messages {{
      grid-area: messages;
      overflow-y: auto;
      padding: 10px;
      box-sizing: border-box;
      border-left: 1px solid #ddd;
    }}
    .msg-box {{
      padding: 8px;
      margin-bottom: 8px;
      border: 1px solid #ccc;
      border-radius: 4px;
      cursor: pointer;
    }}
    .msg-box.active {{
      background-color: #eef;
      border-color: #66a;
    }}
    /* hide message details by default, show when active */
    .msg-box pre {{
      display: none;
      background-color: #f9f9f9;
      padding: 8px;
      margin-top: 4px;
      border-radius: 4px;
    }}
    .msg-box.active pre {{
      display: block;
    }}
    pre {{
      margin: 0;
      white-space: pre-wrap;
      word-wrap: break-word;
    }}
  </style>
</head>
<body>
  <div id=\"controls\">
    <label><input type=\"radio\" name=\"view\" value=\"graph\" checked> Knowledge Graph</label>
    <label style=\"margin-left: 10px;\"><input type=\"radio\" name=\"view\" value=\"timeline\"> Timeline</label>
  </div>
  <div id=\"network\" style=\"width:100%; height:100%;\"></div>
  <div id=\"timeline\" style=\"display: none; width:100%; height:100%;\"></div>
  <div id=\"messages\"></div>
  <script>
  // view toggle logic using radio buttons
  var netDiv = document.getElementById('network');
  var timDiv = document.getElementById('timeline');
  document.getElementsByName('view').forEach(function(radio) {{
    radio.onchange = function() {{
      if (this.value === 'graph') {{
        netDiv.style.display = 'block';
        timDiv.style.display = 'none';
        // redraw network when shown
        if (typeof network !== 'undefined' && network.redraw) {{ network.redraw(); }}
      }} else {{
        netDiv.style.display = 'none';
        timDiv.style.display = 'block';
        // optional: redraw timeline
        if (typeof timeline !== 'undefined' && timeline.redraw) {{ timeline.redraw(); }}
      }}
    }};
  }});
  // -- Knowledge Graph --
  var graphData = {{
    nodes: new vis.DataSet({net_nodes_json}),
    edges: new vis.DataSet({net_edges_json})
  }};
  // apply color coding by node type (background colors)
  var typeColors = {{
    'agent': '#FF6666',
    'tool': '#66FF66',
    'tool_call': '#FF9966',
    'observation': '#6666FF',
    'action': '#FFCC66',
    'step': '#CCCCCC',
    'final_answer': '#CC66FF'
  }};
  // update node colors in the DataSet
  graphData.nodes.get().forEach(function(node) {{
    var c = typeColors[node.type];
    if (c) {{
      graphData.nodes.update({{ id: node.id, color: {{ background: c }} }});
    }}
  }});
  var network = new vis.Network(
    document.getElementById('network'),
    graphData,
    {{ interaction: {{ hover: true }}, edges: {{ arrows: {{ to: true }} }} }}
  );
  // ensure network knows its container size
  network.setSize('100%', '100%');
  network.redraw();
  // redraw on window resize
  window.addEventListener('resize', function() {{ network.redraw(); }});
  // ensure initial redraw after page load
  window.addEventListener('load', function() {{ if (network && network.redraw) network.redraw(); }});

  // -- Timeline View --
  var timelineGroups = new vis.DataSet({groups_json});
  var timelineItems = new vis.DataSet({items_json});
  var timelineOptions = {{
    selectable: true,
    showCurrentTime: false,
    // enable nested step subgroups display
    showNested: true
  }};
  var timeline = new vis.Timeline(
    document.getElementById('timeline'),
    timelineItems,
    timelineGroups,
    timelineOptions
  );

  // -- Messages Pane --
  var allNodes = new vis.DataSet({net_nodes_json});
  var messagesDiv = document.getElementById('messages');
  // Create one clickable box per graph node
  allNodes.forEach(node => {{
    var b = document.createElement('div');
    b.className = 'msg-box';
    b.dataset.nodeId = node.id;
    b.innerHTML = '<strong>' + (node.label || node.id) + '</strong>' + (node.title || '');
    // attach hidden message details (JSON content)
    var pre = document.createElement('pre');
    pre.textContent = JSON.stringify(node, null, 2);
    b.appendChild(pre);
    b.onclick = () => {{
      // highlight message box and show details
      document.querySelectorAll('.msg-box.active').forEach(e => e.classList.remove('active'));
      b.classList.add('active');
      b.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
      // select node in graph
      network.selectNodes([node.id]);
      network.focus(node.id, {{ scale: 1.2 }});
    }};
    messagesDiv.appendChild(b);
  }});
  // Highlight message when a node is selected in the graph
  network.on('selectNode', (params) => {{
    var sel = params.nodes[0];
    var el = document.querySelector('.msg-box[data-node-id="' + sel + '"]');
    if (el) {{
      document.querySelectorAll('.msg-box.active').forEach(e => e.classList.remove('active'));
      el.classList.add('active');
      el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
    }}
  }});
  </script>
</body>
</html>"""

    # Write out the combined HTML
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Multi-view visualization written to {out_file}")

if __name__ == '__main__':
    main()