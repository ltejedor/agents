import os
import sys
# Ensure local smolagents-ref is used before any installed smolagents
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'smolagents-ref', 'src'))
import requests
import xml.etree.ElementTree as ET
import json
import re
from smolagents import CodeAgent, tool, LiteLLMModel
from dotenv import load_dotenv
from requests.exceptions import RequestException
from datetime import date
from proof_of_work import save_proof_of_work

load_dotenv()


@tool
def visit_webpage(url: str) -> str:
    """Visits a webpage at the given URL and returns its content as a markdown string.

    Args:
        url: The URL of the webpage to visit.

    Returns:
        The content of the webpage converted to Markdown, or an error message if the request fails.
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Convert the HTML content to Markdown - assuming a markdownify function exists
        # You'll need to add the import for markdownify or implement the conversion
        from markdownify import markdownify
        markdown_content = markdownify(response.text).strip()

        # Remove multiple line breaks
        markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)

        return markdown_content

    except RequestException as e:
        return f"Error fetching the webpage: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


# -----------------------------------------------------------------------------
# Main Agent Workflow
# -----------------------------------------------------------------------------
def main():

    # Set up the tools list for the agent.
    tools = [visit_webpage]
    
    # Initialize the agent with the chosen tools and a basic model.
    #model = HfApiModel()
    model = LiteLLMModel(model_id="anthropic/claude-3-7-sonnet-latest")

    agent = CodeAgent(
        tools=tools,
        model=model,
        add_base_tools=True,
        additional_authorized_imports=["time", "json", "pydoc", "watchdog"],
        max_steps=100
    )
    
    # Import step types for recording
    from smolagents.memory import TaskStep, PlanningStep, ActionStep, SystemPromptStep, FinalAnswerStep
    import json

    def record_step(step, agent_obj):
        # Convert a memory step to a dict for real-time provenance logging
        agent_name = getattr(agent_obj, 'name', None) or getattr(agent_obj, 'agent_name', type(agent_obj).__name__)
        seq = len(agent_obj.memory.steps) - 1
        rec = {'agent': agent_name, 'sequence': seq}
        if isinstance(step, SystemPromptStep):
            rec.update({'type': 'system_prompt', 'system_prompt': step.system_prompt})
        elif isinstance(step, TaskStep):
            rec.update({'type': 'task', 'task': step.task})
        elif isinstance(step, PlanningStep):
            rec.update({'type': 'planning', 'plan': step.plan})
        elif isinstance(step, ActionStep):
            calls = [tc.dict() for tc in (step.tool_calls or [])]
            rec.update({
                'type': 'action',
                'step_number': step.step_number,
                'model_output': step.model_output,
                'tool_calls': calls,
                'observations': step.observations,
                'action_output': step.action_output,
                'start_time': step.start_time,
                'end_time': step.end_time,
                'duration': step.duration,
            })
        elif isinstance(step, FinalAnswerStep):
            rec.update({'type': 'final_answer', 'final_answer': step.final_answer})
        else:
            rec.update({'type': 'unknown'})
        return rec

    # Interactive REPL via manager with real-time provenance
    while True:
        task = input("\nEnter task (or 'exit' to quit): ")
        if task.lower() in ['exit', 'quit']:
            break
        print(f"Starting run for task: {task}")
        try:
            # Stream steps as they occur
            stream = agent.run(task, stream=True)
            # Emit initial task step
            if agent.memory.steps:
                initial = agent.memory.steps[0]
                rec0 = record_step(initial, agent)
                print(json.dumps(rec0, default=str))
            # Emit subsequent steps
            for step in stream:
                rec = record_step(step, agent)
                print(json.dumps(rec, default=str))
        except Exception as e:
            print(f"Error during run: {e}")

    # Save full provenance at end
    saved_path = save_proof_of_work(agent, output_dir='./output')
    print(f"Full proof of work written to {saved_path}")
if __name__ == '__main__':
    main()