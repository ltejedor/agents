import os
import json
from datetime import datetime

def extract_tool_calls(agent):
    """
    Extract tool calls from an agent's memory steps.

    Args:
        agent: Agent instance with memory attribute (e.g., smolagents CodeAgent).

    Returns:
        List of tool call dictionaries representing each function call made by the agent.
    """
    memory = getattr(agent, 'memory', None)
    if memory is None:
        raise ValueError("Agent has no memory attribute")
    # Try succinct steps, then full steps, then direct steps list
    if hasattr(memory, 'get_succinct_steps'):
        steps = memory.get_succinct_steps()
    elif hasattr(memory, 'get_full_steps'):
        steps = memory.get_full_steps()
    else:
        steps = []
        for step in getattr(memory, 'steps', []):
            if hasattr(step, 'dict'):
                steps.append(step.dict())
    # Collect tool_calls
    calls = []
    for step in steps:
        tool_calls = step.get('tool_calls') or []
        for call in tool_calls:
            calls.append(call)
    return calls

def save_proof_of_work(agent, output_dir='output', prefix='proof_of_work'):
    """
    Save the proof of work (tool calls) to a JSON file in the specified output directory.

    Args:
        agent: Agent instance with recorded memory of steps.
        output_dir: Directory path to save the output file (will be created if not exists).
        prefix: Filename prefix for the proof of work file.

    Returns:
        The path to the saved JSON file.
    """
    os.makedirs(output_dir, exist_ok=True)
    calls = extract_tool_calls(agent)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{prefix}_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(calls, f, indent=2)
    return filepath
