import streamlit as st
import streamlit_nested_layout  # enable nested layout components
from smolagents import CodeAgent, ToolCallingAgent, HfApiModel, tool, LiteLLMModel
from streamlit_react_flow import react_flow
import json
from dotenv import load_dotenv
import re
from smolagents.gradio_ui import pull_messages_from_step
from smolagents.memory import FinalAnswerStep
from smolagents.agent_types import AgentText, AgentImage, AgentAudio

load_dotenv()

st.title("Your AI Organization")
st.subheader("Starter Org Template")

# Initialize session state to store agent configuration
if "agents_config" not in st.session_state:
    st.session_state.agents_config = {
        "manager": {
            "id": "0",
            "type": "manager",
            # user-facing label
            "display_name": "Leslie Knope",
            # internal identifier for CodeAgent
            "name": "leslie_knope",
            "description": "Hyper-organized and driven manager who never misses a detail. Loves binders, waffles, and getting things done."
        },
        "workers": [
            {
                "id": "1",
                "type": "agent",
                # user-facing label
                "display_name": "Ben Wyatt",
                # internal identifier for CodeAgent
                "name": "ben_wyatt",
                "description": "Numbers guy. Analytical, practical, and the go-to for budgeting and strategy.",
                "model": "claude"
            },
            {
                "id": "2",
                "type": "agent",
                "display_name": "April Ludgate",
                "name": "april_ludgate",
                "description": "Handles the weird stuff. Mysterious, unpredictable, and surprisingly effective.",
                "model": "claude"
            }
        ]
    }


# Create the react-flow elements based on the agent configuration
def create_elements_from_config():
    elements = []
    
    # Add manager node
    elements.append({
        "id": st.session_state.agents_config["manager"]["id"],
        # use display_name for user-facing label
        "data": {"label": st.session_state.agents_config["manager"]["display_name"]},
        "type": "input",
        "style": {"background": '#ffcc50', "width": 100},
        "position": {"x": 250, "y": 100}
    })
    
    # Add worker nodes, distributing them evenly across the width
    workers = st.session_state.agents_config["workers"]
    n = len(workers)
    total_width = 500  # must match flowStyles width
    node_width = 100
    margin = node_width // 2
    available_width = total_width - 2 * margin
    # compute x positions: for one worker, place at left margin; otherwise spread from left to right margin
    if n <= 1:
        x_positions = [margin]
    else:
        x_positions = [int(margin + (available_width * i / (n - 1))) for i in range(n)]
    for i, worker in enumerate(workers):
        elements.append({
            "id": worker["id"],
            # use display_name if available, otherwise internal name
            "data": {"label": worker.get("display_name", worker["name"])},
            "type": "output",
            "position": {"x": x_positions[i], "y": 250}
        })
        # Add connection from manager to worker
        elements.append({
            "id": f'e{st.session_state.agents_config["manager"]["id"]}-{worker["id"]}',
            "source": st.session_state.agents_config["manager"]["id"],
            "target": worker["id"],
            "animated": True
        })
    
    return elements

# Create agents based on configuration
def create_agents_from_config():
    model_map = {
        "claude": LiteLLMModel(model_id="anthropic/claude-3-7-sonnet-latest"),
    }
    
    # Create worker agents
    workers = {}
    for worker in st.session_state.agents_config["workers"]:
        # Agent internal name and human-readable description
        agent_name = worker.get("name")
        description = worker.get("description")
        if worker["type"] in ("agent", "codeagent"):
            workers[worker["id"]] = CodeAgent(
                tools=[],
                model=model_map.get(worker.get("model", "claude")),
                name=agent_name,
                description=description,
                add_base_tools=True
            )

    # Create manager agent orchestrating the workers
    manager = CodeAgent(
        tools=[],
        model=LiteLLMModel(model_id="anthropic/claude-3-7-sonnet-latest"),
        name="manager_agent",
        add_base_tools=True,
        managed_agents=list(workers.values())
    )
    return manager, workers

# Buttons to manually add or remove worker agents
col1, col2 = st.columns(2)
with col1:
    if st.button("Add Worker"):
        # compute new worker id as max existing worker id + 1
        worker_ids = [int(w["id"]) for w in st.session_state.agents_config["workers"]]
        new_id = str(max(worker_ids) + 1 if worker_ids else 2)
        # determine next ordinal label
        ordinals = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
        idx = len(st.session_state.agents_config["workers"])
        ordinal = ordinals[idx] if idx < len(ordinals) else str(idx + 1)
        label = f"agent_{ordinal}"
        st.session_state.agents_config["workers"].append({
            "id": new_id,
            "type": "agent",
            # internal identifier
            "name": label,
            # user-facing label
            "display_name": label,
            # optional role description
            "description": "A new hire in the office",
            "model": "claude"
        })
with col2:
    if st.button("Remove Worker"):
        if st.session_state.agents_config["workers"]:
            # remove worker with highest numeric id
            to_remove = max(st.session_state.agents_config["workers"], key=lambda w: int(w["id"]))
            st.session_state.agents_config["workers"].remove(to_remove)

# Allow editing of worker labels and descriptions
# Allow editing of worker internal name, display name, and description
with st.expander("Edit Worker Details", expanded=False):
    for w in st.session_state.agents_config["workers"]:
        st.write(f"Agent ID: {w['id']}")
        # Internal identifier for coding use
        internal_key = f"internal_{w['id']}"
        new_internal = st.text_input(
            f"Internal Name ({w['id']})", 
            w.get("name", ""), 
            key=internal_key
        )
        # User-facing label
        display_key = f"display_{w['id']}"
        new_display = st.text_input(
            f"Display Name ({w['id']})", 
            w.get("display_name", w.get("name", "")), 
            key=display_key
        )
        # Optional description
        desc_key = f"desc_{w['id']}"
        new_desc = st.text_area(
            f"Description ({w['id']})", 
            w.get("description", ""), 
            height=100,
            key=desc_key
        )
        # Update internal name if changed
        if new_internal != w.get("name"):
            clean = re.sub(r'\W|^(?=\d)', '_', new_internal).lower()
            if not clean or not clean.isidentifier():
                clean = f"agent_{w['id']}"
            w["name"] = clean
        # Update display name
        if new_display != w.get("display_name", w.get("name")):
            w["display_name"] = new_display
        # Update description
        if new_desc != w.get("description"):
            w["description"] = new_desc

# Create the flow visualization
elements = create_elements_from_config()
flowStyles = {"height": 400, "width": 800}

# Create manager and worker agents
manager, workers = create_agents_from_config()

# Handle graph updates from react-flow
if True:  # always enable graph editing
    graph_result = react_flow(
        "agent_hierarchy", 
        elements=elements, 
        flow_styles=flowStyles
    )
    
    # Update agent configuration based on graph changes
    if graph_result and "elements" in graph_result:
        updated_elements = graph_result["elements"]
        
        # Extract nodes and edges
        nodes = [e for e in updated_elements if "source" not in e and "target" not in e]
        edges = [e for e in updated_elements if "source" in e and "target" in e]
        
        # Update manager
        manager_node = next((n for n in nodes if n["type"] == "input"), None)
        if manager_node:
            # Update user-facing label from graph edit
            st.session_state.agents_config["manager"]["display_name"] = manager_node["data"]["label"]
        
        # Update workers - ensure valid Python identifiers for labels used as agent names
        worker_nodes = [n for n in nodes if n["type"] == "output"]
        for worker_node in worker_nodes:
            # Get updated display label from graph
            display_label = worker_node["data"]["label"]
            # Find existing worker config
            existing_worker = next(
                (w for w in st.session_state.agents_config["workers"] if w["id"] == worker_node["id"]),
                None
            )
            if existing_worker:
                # update only the user-facing label
                existing_worker["display_name"] = display_label
            else:
                # create new worker entry with display and internal names
                # sanitize display_label to internal identifier
                internal = re.sub(r'\W|^(?=\d)', '_', display_label).lower()
                if not internal or not internal.isidentifier():
                    internal = f"agent_{worker_node['id']}"
                st.session_state.agents_config["workers"].append({
                    "id": worker_node["id"],
                    "type": "agent",
                    "name": internal,
                    "display_name": display_label,
                    "description": "",
                    "model": "claude"
                })
        
        # Remove workers that are no longer in the graph
        worker_ids = [n["id"] for n in worker_nodes]
        st.session_state.agents_config["workers"] = [
            w for w in st.session_state.agents_config["workers"] if w["id"] in worker_ids
        ]
        
        # Recreate agents with updated configuration
        manager, workers = create_agents_from_config()
else:
    react_flow("agent_hierarchy", elements=elements, flow_styles=flowStyles)


# Multi-agent system interface
with st.expander("Multi-Agent System", expanded=True):
    prompt = st.text_area("Enter task for multi-agent system")
    if st.button("Run Multi-Agent") and prompt:
        final_answer = None
        run_gen = manager.run(prompt, stream=True)
        # Display chain of thought in a popover
        with st.popover("Chain of Thought"):
            for step_log in run_gen:
                for msg in pull_messages_from_step(step_log):
                    if isinstance(msg.content, dict):
                        mime = msg.content.get("mime_type", "")
                        path = msg.content.get("path", "")
                        if mime.startswith("image"):
                            st.image(path)
                        elif mime.startswith("audio"):
                            st.audio(path)
                        else:
                            st.write(msg.content)
                    else:
                        text = msg.content
                        match = re.match(r"```(\\w+)?\\n([\\s\\S]*?)```", text)
                        if match:
                            st.code(match.group(2), language=match.group(1) or None)
                        else:
                            st.write(text)
                if isinstance(step_log, FinalAnswerStep):
                    final_answer = step_log.final_answer
        # Display final answer
        st.markdown("**Final Answer:**")
        if isinstance(final_answer, AgentText):
            st.markdown(final_answer.to_string())
        elif isinstance(final_answer, AgentImage):
            st.image(final_answer.to_string())
        elif isinstance(final_answer, AgentAudio):
            st.audio(final_answer.to_string())
        else:
            st.write(final_answer)