import streamlit as st
import re
from smolagents import CodeAgent, LiteLLMModel, InferenceClientModel
from smolagents.gradio_ui import pull_messages_from_step
from smolagents.agent_types import AgentText, AgentImage, AgentAudio
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from transformers import AutoModelForCausalLM, AutoTokenizer
import os
from smolagents.agent_types import AgentText
import time


load_dotenv()

model_id = "mistralai/Mixtral-8x7B-v0.1"

client = InferenceClientModel(model=model_id)
# Energy usage tracking: estimated GPU energy consumption rate for Mixtral-8x7B-v0.1 (Wh per hour)
ENERGY_WH_PER_HOUR = 615.39

# model_id = "openai-community/gpt2"
# client = InferenceClient(model=model_id, token=os.getenv("HUGGINGFACE_API_KEY"))

# def custom_model(messages, stop_sequences=["Task"], grammar=None):
#     #prompt = "\n".join([m["content"] for m in messages])
#     prompt = messages[-1]['content'][0]['text']  # Get the latest user message
#     response = client.text_generation(
#         prompt=prompt,
#         max_new_tokens=800,
#         stop=stop_sequences
#     )
#     print(response)
#     return AgentText(response)

#model = InferenceClientModel(model_id="google/gemma-2-2b")
#model = LiteLLMModel(model_id="huggingface/HuggingFaceTB/SmolLM2-1.7B-Instruct")

agent = CodeAgent(
    tools=[],
    model=client,
    add_base_tools=True
)

# Title and initialize UI
st.title("Agent")

# Initialize chat history and energy usage
if "messages" not in st.session_state:
    st.session_state.messages = []
if "energy" not in st.session_state:
    # total energy consumed in Wh
    st.session_state.energy = 0.0
# Display energy usage in sidebar with updatable placeholder
st.sidebar.header("Usage")
energy_metric = st.sidebar.empty()
energy_metric.metric("Energy consumed (Wh)", f"{st.session_state.energy:.2f}")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input and stream chain-of-thought inline as separate assistant messages
if prompt := st.chat_input("Give me a task..."):
    # Add and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Stream agent steps and display each message inline
    # Measure inference duration
    start_time = time.time()
    for step_log in agent.run(prompt, stream=True):
        for msg in pull_messages_from_step(step_log):
            content = msg.content
            # Display content in a new assistant message bubble
            with st.chat_message("assistant"):
                if isinstance(content, dict):
                    mime = content.get("mime_type", "")
                    path = content.get("path", "")
                    if mime.startswith("image"):
                        st.image(path)
                    elif mime.startswith("audio"):
                        st.audio(path)
                    else:
                        st.write(content)
                else:
                    text = content
                    match = re.match(r"```(\w+)?\n([\s\S]*?)```", text)
                    if match:
                        st.code(match.group(2), language=match.group(1) or None)
                    else:
                        st.write(text)
            # Append to chat history
            if isinstance(content, dict):
                mime = content.get("mime_type", "")
                path = content.get("path", "")
                if mime.startswith("image"):
                    hist = f"![Image]({path})"
                elif mime.startswith("audio"):
                    hist = f"[Audio]({path})"
                else:
                    hist = str(content)
            else:
                hist = str(content)
            st.session_state.messages.append({"role": "assistant", "content": hist})
    # Compute elapsed time and update energy consumption
    duration_sec = time.time() - start_time
    # Convert seconds to hours and multiply by rate to get Wh
    energy_used = (duration_sec / 3600.0) * ENERGY_WH_PER_HOUR
    st.session_state.energy += energy_used
    # Update sidebar metric immediately
    energy_metric.metric("Energy consumed (Wh)", f"{st.session_state.energy:.2f}")