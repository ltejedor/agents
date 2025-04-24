# AI Energy Usage Tracker

A Streamlit application that tracks and displays energy consumption of AI models during inference. This tool helps users understand the environmental impact of their AI interactions by measuring and visualizing energy usage in real-time.

## Overview

This project creates an interactive chat interface powered by the Mixtral-8x7B model while monitoring the energy consumption of each interaction. It provides transparency about the computational resources used during AI inference, helping users make more informed decisions about their AI usage.

## Features

- Real-time chat interface with an AI assistant
- Live energy consumption tracking in watt-hours (Wh)
- Cumulative energy usage statistics
- Support for text, code, image, and audio content
- Persistent chat history across sessions
- Markdown and code syntax highlighting

## Data Source

The energy consumption data and benchmarks are sourced from the [AI Energy Leaderboard](https://huggingface.co/spaces/AIEnergyScore/Leaderboard) on Hugging Face, which provides standardized measurements for various AI models.

## Requirements

- Python 3.8+
- Dependencies:
  - `streamlit` - For the web interface
  - `smolagents` - For agent-based interactions
  - `transformers` - For model loading and inference
  - `huggingface_hub` - For accessing Hugging Face models
  - `dotenv` - For environment variable management

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ltejedor/agents.git
cd agents/13-energy-ui
```

2. Install the required dependencies:
```bash
pip install -r ../requirements.txt
```

3. Create a `.env` file with your API keys (if needed):
```
HUGGINGFACE_API_KEY=your_huggingface_key_here
```

## Usage

Run the Streamlit application:
```bash
streamlit run main.py
```

The interface allows you to:
1. Enter tasks or questions in the chat input
2. View the AI's responses in real-time
3. Monitor energy consumption in the sidebar
4. Track cumulative energy usage across your session

## How It Works

1. The application initializes a Mixtral-8x7B model through the Hugging Face Inference API
2. When a user submits a prompt, the system:
   - Records the start time
   - Processes the request through the AI model
   - Streams the response to the UI
   - Calculates energy consumption based on inference duration
   - Updates the energy usage metric in the sidebar
3. Energy consumption is calculated using a predefined rate (615.39 Wh per hour) based on benchmarks for the Mixtral-8x7B model
4. The chat history and cumulative energy usage are maintained in the session state

## Why Energy Tracking Matters

AI models, especially large language models, can consume significant computational resources. By making this energy usage transparent, this tool helps:

- Raise awareness about the environmental impact of AI
- Encourage more efficient use of AI resources
- Provide data for comparing the efficiency of different models and approaches
- Support more sustainable AI development and deployment practices

## Customization

- To use a different model, modify the `model_id` variable
- To adjust the energy consumption rate, update the `ENERGY_WH_PER_HOUR` constant
- The UI can be customized using standard Streamlit components and styling