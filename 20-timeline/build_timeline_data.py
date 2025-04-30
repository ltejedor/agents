#!/usr/bin/env python3
"""
build_timeline_data.py

Convert a provenance dictionary into groups and items suitable
for a vis-timeline swimlane view.
"""
from typing import Dict, List, Tuple
from datetime import datetime
import json

def build_timeline_data(provenance: Dict) -> Tuple[List[Dict], List[Dict]]:
    """
    Build groups and items for a timeline visualization.

    Args:
        provenance: dict from proof_of_work JSON under 'provenance'.

    Returns:
        groups: list of dicts with keys 'id' and 'content' for each agent.
        items: list of dicts with keys 'id', 'group', 'content', 'start'.
    """
    groups = []
    items: List[Dict] = []
    # Root agent with nested step subgroups
    root = provenance.get('root_agent', {})
    root_name = root.get('name', 'root')
    root_group: Dict = {'id': root_name, 'content': root_name, 'nestedGroups': []}
    groups.append(root_group)
    # Steps for root agent
    for step in root.get('steps', []):
        seq = step.get('sequence')
        step_type = step.get('type', '')
        start = step.get('start_time')
        end = step.get('end_time')
        if start is None:
            continue
        # define subgroup for this step
        step_id = f"{root_name}-step-{seq}"
        root_group['nestedGroups'].append(step_id)
        groups.append({'id': step_id, 'content': f"Step {seq}: {step_type}"})
        # format times
        start_str = datetime.fromtimestamp(start).isoformat()
        # Action/step item with duration
        item = {
            'id': step_id,
            'group': root_name,
            'subgroup': step_id,
            'content': step_type,
            'start': start_str,
            'className': step_type,
            'style': 'background-color: #FFCC66; border-color: #FFCC66;'
        }
        if end is not None:
            item['end'] = datetime.fromtimestamp(end).isoformat()
        items.append(item)
        # tool calls as point items within this step subgroup
        for idx, call in enumerate(step.get('tool_calls', []) or []):
            func = call.get('function', {})
            call_name = func.get('name', call.get('name', 'tool_call'))
            call_id = f"{step_id}-call-{idx}"
            # Tool call point item
            call_item = {
                'id': call_id,
                'group': root_name,
                'subgroup': step_id,
                'content': f"🔧 {call_name}",
                'start': start_str,
                'type': 'point',
                'className': 'tool_call',
                'style': 'background-color: #FF9966; border-color: #FF9966;',
                'title': json.dumps(call, indent=2)
            }
            items.append(call_item)
    # Managed agents (same pattern)
    for ma in provenance.get('managed_agents', {}).values():
        name = ma.get('name')
        if not name:
            continue
        ma_group: Dict = {'id': name, 'content': name, 'nestedGroups': []}
        groups.append(ma_group)
        for step in ma.get('steps', []):
            seq = step.get('sequence')
            step_type = step.get('type', '')
            start = step.get('start_time')
            end = step.get('end_time')
            if start is None:
                continue
            step_id = f"{name}-step-{seq}"
            ma_group['nestedGroups'].append(step_id)
            groups.append({'id': step_id, 'content': f"Step {seq}: {step_type}"})
            start_str = datetime.fromtimestamp(start).isoformat()
            # Action/step item for managed agent
            item = {
                'id': step_id,
                'group': name,
                'subgroup': step_id,
                'content': step_type,
                'start': start_str,
                'className': step_type,
                'style': 'background-color: #FFCC66; border-color: #FFCC66;'
            }
            if end is not None:
                item['end'] = datetime.fromtimestamp(end).isoformat()
            items.append(item)
            for idx, call in enumerate(step.get('tool_calls', []) or []):
                func = call.get('function', {})
                call_name = func.get('name', call.get('name', 'tool_call'))
                call_id = f"{step_id}-call-{idx}"
                # Tool call point item for managed agent
                call_item = {
                    'id': call_id,
                    'group': name,
                    'subgroup': step_id,
                    'content': f"🔧 {call_name}",
                    'start': start_str,
                    'type': 'point',
                    'className': 'tool_call',
                    'style': 'background-color: #FF9966; border-color: #FF9966;',
                    'title': json.dumps(call, indent=2)
                }
                items.append(call_item)
    return groups, items