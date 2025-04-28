#!/usr/bin/env python3
"""
viz_knowledge_graph.py

Generate an interactive HTML visualization of a proof_of_work JSON knowledge graph.
This script reads the provenance JSON, builds a NetworkX graph, and uses PyVis to emit
an HTML file you can open in your browser.

Usage:
  pip install networkx pyvis
  python viz_knowledge_graph.py proof_of_work_20250428_145452.json
"""
import os
import json
import argparse


import networkx as nx
try:
    from pyvis.network import Network
except ImportError:
    raise ImportError("pyvis is required to run this script: pip install pyvis")

from build_knowledge_graph import build_graph


def main():
    parser = argparse.ArgumentParser(
        description="Visualize a proof_of_work JSON as an interactive HTML graph"
    )
    parser.add_argument(
        'input_json', help='Path to proof_of_work JSON file'
    )
    parser.add_argument(
        '-o', '--output', help='Output HTML file', default=None
    )
    parser.add_argument(
        '--title', help='Title for the visualization', default=None
    )
    args = parser.parse_args()

    # Load proof_of_work JSON
    with open(args.input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    provenance = data.get('provenance', {})

    # Build NetworkX graph
    G = build_graph(provenance)

    # Initialize PyVis network
    net = Network(
        height='750px', width='100%', directed=True, notebook=False
    )
    if args.title:
        net.heading = args.title
    # Transfer nodes & edges
    net.from_nx(G)

    # Determine output HTML path
    base = os.path.splitext(args.input_json)[0]
    out_file = args.output or f"{base}.html"
    # Generate and save HTML (use write_html directly to avoid notebook template issues)
    net.write_html(out_file, open_browser=False, notebook=False)
    print(f"Interactive visualization written to {out_file}")


if __name__ == '__main__':
    main()