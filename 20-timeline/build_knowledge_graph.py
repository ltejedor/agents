#!/usr/bin/env python3
"""
build_knowledge_graph.py

Reads a proof_of_work JSON file and builds a knowledge graph of agents,
steps, tool calls, observations, and final answers. Exports the graph in GEXF format.
"""
import os
import json
import argparse

try:
    import networkx as nx
except ImportError:
    raise ImportError("networkx is required to build the knowledge graph. Install with `pip install networkx`.")


def build_graph(provenance: dict) -> nx.DiGraph:
    G = nx.DiGraph()
    # Root agent
    root = provenance.get('root_agent', {})
    root_name = root.get('name', 'root')
    root_id = f"agent:{root_name}"
    # Filter out None values in attributes
    root_attrs = {
        'type': 'agent',
        'class_name': root.get('class'),
        'model': root.get('model'),
    }
    root_attrs = {k: v for k, v in root_attrs.items() if v is not None}
    G.add_node(root_id, **root_attrs)

    # Helper to add agent steps
    def add_agent_steps(agent_info, agent_id):
        prev_step = None
        for step in agent_info.get('steps', []):
            seq = step.get('sequence')
            step_type = step.get('type', 'step')
            step_id = f"{agent_id}:step:{seq}"
            # Build attributes, skipping None values
            attrs = {'type': step_type, 'sequence': seq}
            for key in ('task', 'plan', 'model_output', 'observations', 'action_output', 'duration'):
                val = step.get(key)
                if val is not None:
                    attrs[key] = val
            G.add_node(step_id, **attrs)
            # Link agent to its first step
            G.add_edge(agent_id, step_id, relation='has_step')
            # Link sequential steps
            if prev_step:
                G.add_edge(prev_step, step_id, relation='next_step')
            prev_step = step_id
            # For action steps, create a distinct node per tool invocation
            if step_type == 'action':
                for idx, call in enumerate(step.get('tool_calls', [])):
                    func = call.get('function', {})
                    tool_name = func.get('name')
                    # create a unique node for this tool call and capture details
                    call_id = f"{step_id}:tool_call:{idx}"
                    call_attrs = {'type': 'tool_call', 'tool': tool_name}
                    # capture code or arguments of the call
                    if 'arguments' in func and func['arguments'] is not None:
                        call_attrs['arguments'] = func['arguments']
                    # attach explicit call output/result
                    obs = None
                    if 'output' in call and call['output'] is not None:
                        obs = call['output']
                    elif 'result' in call and call['result'] is not None:
                        obs = call['result']
                    # fallback: if exactly one call in step, use step observations
                    elif len(step.get('tool_calls', [])) == 1 and step.get('observations') is not None:
                        obs = step.get('observations')
                    if obs is not None:
                        call_attrs['observations'] = obs
                    G.add_node(call_id, **call_attrs)
                    # link step to this specific call
                    G.add_edge(step_id, call_id, relation='calls_tool')
                    # link this call to the generic tool node (skip python interpreter)
                    if tool_name != 'python_interpreter':
                        tool_id = f"tool:{tool_name}"
                        G.add_node(tool_id, type='tool')
                        G.add_edge(call_id, tool_id, relation='uses_tool')
            # Final answer inside processing will be separate
        # After steps, check for final answer node
        # It may appear as its own step

    # Build graph for root agent
    add_agent_steps(root, root_id)

    # Managed agents
    for ma in provenance.get('managed_agents', {}).values():
        ma_name = ma.get('name')
        ma_id = f"agent:{ma_name}"
        # Filter out None values in attributes
        ma_attrs = {
            'type': 'agent',
            'class_name': ma.get('class'),
            'model': ma.get('model'),
        }
        ma_attrs = {k: v for k, v in ma_attrs.items() if v is not None}
        G.add_node(ma_id, **ma_attrs)
        # Link management
        G.add_edge(root_id, ma_id, relation='manages')
        add_agent_steps(ma, ma_id)

    # Finally, attach final answers if any
    # Search for final_answer steps across all agents
    for node, data in list(G.nodes(data=True)):
        if isinstance(data.get('type'), str) and data.get('type') == 'final_answer':
            # Already a step node with final_answer attribute
            continue
    return G


def main():
    parser = argparse.ArgumentParser(description='Build a knowledge graph from proof_of_work JSON.')
    parser.add_argument('input_json', help='Path to proof_of_work JSON file')
    parser.add_argument('-o', '--output', help='Output graph file path (extension defines format)', default=None)
    parser.add_argument('-f', '--format', choices=['gexf', 'graphml', 'json'],
                        help='Explicit output format (overrides extension)', default=None)
    args = parser.parse_args()

    # Load JSON
    with open(args.input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    provenance = data.get('provenance', {})

    # Build graph
    G = build_graph(provenance)

    # Determine output format and path
    base = os.path.splitext(args.input_json)[0]
    fmt = args.format
    if args.output:
        out_path = args.output
        # infer format if not given
        if fmt is None:
            ext = os.path.splitext(out_path)[1].lower().lstrip('.')
            fmt = ext if ext in ['gexf', 'graphml', 'json'] else 'gexf'
    else:
        fmt = fmt or 'gexf'
        out_path = f"{base}.{fmt}"

    # Write graph in chosen format
    if fmt == 'gexf':
        nx.write_gexf(G, out_path)
    elif fmt == 'graphml':
        nx.write_graphml(G, out_path)
    elif fmt == 'json':
        from networkx.readwrite import json_graph
        data = json_graph.node_link_data(G)
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    else:
        raise ValueError(f"Unsupported format: {fmt}")
    print(f'Knowledge graph saved to {out_path} ({fmt})')


if __name__ == '__main__':
    main()