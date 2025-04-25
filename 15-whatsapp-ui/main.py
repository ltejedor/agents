"""
Streamlit-based UI for interacting with WhatsApp via the SmolAgents MCP server.

Features:
1. List WhatsApp group chats and select one.
2. Display recent chat history for the selected group.
3. Send instructions to the agent (e.g., send messages, summaries) which will run via the CodeAgent.
"""
import os
import streamlit as st
import json
from dotenv import load_dotenv
from smolagents import ToolCollection, CodeAgent, LiteLLMModel
from mcp import StdioServerParameters
import time
import re

load_dotenv()

model = LiteLLMModel(model_id="anthropic/claude-3-7-sonnet-latest")

# Set up the MCP server parameters for WhatsApp
current_dir = os.path.dirname(os.path.abspath(__file__))
# After reorganizing MCP servers, locate WhatsApp MCP under mcp-servers
whatsapp_mcp_dir = os.path.abspath(
    os.path.join(current_dir, "..", "mcp-servers", "whatsapp-mcp", "whatsapp-mcp-server")
)

server_parameters = StdioServerParameters(
    command="python",
    args=["main.py"],
    env=os.environ,
    cwd=whatsapp_mcp_dir,
)

st.title("📱 WhatsApp Agent")

# Create a tool collection from the MCP server
with ToolCollection.from_mcp(server_parameters, trust_remote_code=True) as tool_collection:
    # Initialize the agent with tools from the MCP server and the client as the model
    agent = CodeAgent(
        tools=[*tool_collection.tools], 
        model=model,
        additional_authorized_imports=["json"],
        add_base_tools=True
    )

    
    # Initialize chat history with a welcome message listing recent group chats
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.chat_map = {}
        # Hidden prompt to agent to list recent WhatsApp group chats
        try:
            hidden_prompt = (
                "List all recent WhatsApp group chats as a JSON array of objects, search for them by looping for page in range(n), chats_data = list_chats(query='', limit=1, page=page, include_last_message=True, sort_by='last_active')"
                "Return only a list of JSON objects each with 'chat_jid' and 'name'. Tell the user to then select which one it wants to create a bot for."
            )
            raw_response = agent.run(hidden_prompt, stream=False)
            # Extract JSON content from response
            match = re.search(r"(\[.*\])", raw_response, flags=re.S)
            if match:
                chats = json.loads(match.group(1))
            else:
                chats = json.loads(raw_response)
            # Filter to group chats (JIDs ending with '@g.us')
            group_chats = [c for c in chats if c.get("chat_jid", "").endswith("@g.us")]
            if not group_chats:
                group_chats = chats
            # Store mapping of chat_jid to name
            for chat in group_chats:
                jid = chat.get("chat_jid")
                name = chat.get("name") or jid
                st.session_state.chat_map[jid] = name
            # Build display content
            content = "📋 **Recent WhatsApp Group Chats:**\n\n"
            #for jid, name in st.session_state.chat_map.items():
                #content += f"- {name}\n"
        except Exception as e:
            content = f"📋 Unable to fetch group chats: {e}"
        st.session_state.messages.append({"role": "assistant", "content": content})

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # If no group chat selected, show buttons to select one
    if "selected_chat_jid" not in st.session_state:
        st.write("### Select a group chat to create a bot for:")
        for jid, name in st.session_state.chat_map.items():
            if st.button(name, key=f"select_{jid}"):
                st.session_state.selected_chat_jid = jid
                st.session_state.selected_chat_name = name
                st.session_state.messages.append({"role": "user", "content": f"Selected group chat: {name} ({jid})"})
    else:
        # Accept user input for the selected group chat and display final agent response only
        if prompt := st.chat_input(f"Give me a task for group '{st.session_state.selected_chat_name}'..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            try:
                result = agent.run(f'for group chat {st.session_state.selected_chat_jid}: {prompt}', stream=False)
                content = str(result)
            except Exception as e:
                content = f"Error: {e}"

            with st.chat_message("assistant"):
                st.markdown(content)
            st.session_state.messages.append({"role": "assistant", "content": content})