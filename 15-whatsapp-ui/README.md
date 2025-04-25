# WhatsApp UI Agent

This project provides a Streamlit-based web interface for interacting with WhatsApp using Claude's AI capabilities. It builds on the WhatsApp MCP (Machine-Callable Programs) server to create an intuitive UI for managing WhatsApp conversations, sending messages, and performing various WhatsApp operations through natural language instructions.

## Features

- **Web-based Interface**: Access your WhatsApp through a browser using Streamlit
- **Group Chat Selection**: Browse and select from your WhatsApp group chats
- **AI-powered Assistance**: Use natural language to instruct the agent to:
  - Send messages to groups
  - Summarize conversations
  - Search for specific content
  - Analyze chat patterns
  - Perform other WhatsApp operations
- **Chat History**: View your interaction history with the agent
- **Media Support**: Handle various media types (images, videos, documents, audio)

## Prerequisites

- Python 3.10 or higher
- Go (for the WhatsApp bridge)
- FFmpeg (optional - for audio message conversion)
- Anthropic API key (for Claude)

## Installation

### 1. Clone this repository

```bash
git clone https://github.com/yourusername/whatsapp-ui.git
cd whatsapp-ui
```

### 2. Install Python dependencies

```bash
# from repository root:
pip install -r requirements.txt
```

### 3. Set up the WhatsApp MCP server

The WhatsApp MCP server should already be set up in the `mcp-servers/whatsapp-mcp` directory. If not, follow these steps:

```bash
git clone https://github.com/lharries/whatsapp-mcp.git mcp-servers/whatsapp-mcp
```

### 4. Run the WhatsApp bridge

Navigate to the WhatsApp bridge directory and run the Go application:

```bash
cd mcp-servers/whatsapp-mcp/whatsapp-bridge
go run main.go
```

The first time you run it, you'll be prompted to scan a QR code with your WhatsApp mobile app to authenticate. Your session should remain active for approximately 20 days before requiring re-authentication.

### 5. Set up environment variables

Create a `.env` file in the `15-whatsapp-ui` directory with the following variables:

```
ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

### Starting the UI

Run the Streamlit application:

```bash
cd 15-whatsapp-ui
streamlit run main.py
```

This will start the Streamlit server and open the UI in your default web browser.

### Using the Interface

1. **Select a Group Chat**: When you first open the application, you'll see a list of your WhatsApp group chats. Click on one to select it.

2. **Interact with the Agent**: Once a group is selected, you can type natural language instructions in the chat input field, such as:
   - "Send a message to this group saying I'll be 10 minutes late"
   - "Summarize the last 20 messages in this group"
   - "Find all messages mentioning the project deadline"
   - "Who has been most active in this group in the last week?"

3. **View Results**: The agent will process your request and display the results in the chat interface.

## Architecture

This application consists of three main components:

1. **Streamlit UI** (this project): A web interface built with Streamlit that provides a user-friendly way to interact with WhatsApp
2. **Python MCP Server** (whatsapp-mcp-server): Implements the Model Context Protocol, providing standardized tools for interacting with WhatsApp
3. **Go WhatsApp Bridge** (whatsapp-bridge): Connects to WhatsApp's web API, handles authentication, and stores message history in SQLite

The UI uses Claude 3.7 Sonnet via the LiteLLMModel interface to process natural language instructions and convert them into appropriate WhatsApp operations.

## Available WhatsApp Tools

The agent has access to the following WhatsApp tools through the MCP server:

- `search_contacts`: Search for contacts by name or phone number
- `list_messages`: Retrieve messages with optional filters and context
- `list_chats`: List available chats with metadata
- `get_chat`: Get information about a specific chat
- `get_direct_chat_by_contact`: Find a direct chat with a specific contact
- `get_contact_chats`: List all chats involving a specific contact
- `get_last_interaction`: Get the most recent message with a contact
- `get_message_context`: Retrieve context around a specific message
- `send_message`: Send a WhatsApp message to a specified phone number or group JID
- `send_file`: Send a file (image, video, raw audio, document) to a specified recipient
- `send_audio_message`: Send an audio file as a WhatsApp voice message
- `download_media`: Download media from a WhatsApp message and get the local file path

## Troubleshooting

### Authentication Issues

- **QR Code Not Displaying**: Check if your terminal supports displaying QR codes. Try restarting the authentication script.
- **WhatsApp Already Logged In**: If your session is active, the Go bridge will reconnect automatically without showing a QR code.
- **Device Limit Reached**: WhatsApp limits the number of linked devices. Remove an existing device from WhatsApp on your phone (Settings > Linked Devices).
- **No Messages Loading**: After initial authentication, it can take several minutes for your message history to load, especially with many chats.
- **WhatsApp Out of Sync**: If messages get out of sync, delete both database files (whatsapp-bridge/store/messages.db and whatsapp-bridge/store/whatsapp.db) and restart the bridge to re-authenticate.

### Common Errors

- **ModuleNotFoundError**: Make sure you've installed all required dependencies with `pip install -r requirements.txt`
- **Connection Errors**: Ensure the WhatsApp bridge is running before starting the Streamlit application
- **API Key Errors**: Verify your Anthropic API key is correctly set in the .env file
- **Streamlit Interface Issues**: If the interface doesn't load properly, try clearing your browser cache or using a different browser

## Limitations

- The WhatsApp connection relies on the WhatsApp Web API, which has certain limitations imposed by WhatsApp
- Group chat functionality is limited to groups you are already a member of
- Media handling capabilities depend on the underlying WhatsApp bridge implementation
- The agent's understanding and capabilities are limited by the Claude model being used

## Acknowledgments

This project uses the [WhatsApp MCP server](https://github.com/lharries/whatsapp-mcp) by Luke Harries, which provides the underlying functionality for connecting to WhatsApp.