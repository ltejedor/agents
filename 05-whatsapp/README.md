# WhatsApp Agent

This project allows you to interact with WhatsApp through a command-line interface using Claude's AI capabilities. It integrates with the WhatsApp Model Context Protocol (MCP) server to search and read messages, interact with contacts, send messages, and handle media files.

## Features

- Search and read your WhatsApp messages (including media)
- Search contacts and manage chats
- Send messages to individuals or groups
- Send and receive various media types (images, videos, documents, audio)
- Leverage Claude's AI capabilities for natural language WhatsApp interaction

## Prerequisites

- Python 3.10 or higher
- Go (for the WhatsApp bridge)
- FFmpeg (optional - for audio message conversion)

## Installation

### 1. Clone this repository

```bash
git clone https://github.com/ltejedor/05-whatsapp.git
cd whatsapp-agent
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up the WhatsApp MCP server

Clone the WhatsApp MCP repository inside your project directory:

```bash
git clone https://github.com/lharries/whatsapp-mcp.git
```

### 4. Run the WhatsApp bridge

Navigate to the WhatsApp bridge directory and run the Go application:

```bash
cd whatsapp-mcp/whatsapp-bridge
go run main.go
```

The first time you run it, you'll be prompted to scan a QR code with your WhatsApp mobile app to authenticate. Your session should remain active for approximately 20 days before requiring re-authentication.

### 5. Set up environment variables (optional)

If you want to use your own Anthropic API key, you can set it as an environment variable:

```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

Run the main script to start the WhatsApp agent:

```bash
python main.py
```

This will initialize the agent and connect to your WhatsApp account through the MCP server. You'll see a list of available tools that can be used to interact with WhatsApp.

### Interactive Commands

Once the agent is running, you can enter natural language commands to interact with your WhatsApp. For example:

- "Show me my recent conversations"
- "Send a message to John saying I'll be late for the meeting"
- "Search my chat with Sarah for messages about the project"
- "Download the image from my last chat with the design team"

Type 'exit' or 'quit' to end the session.

## Available MCP Tools

The agent has access to the following WhatsApp tools:

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

## Media Handling

### Sending Media

You can send various media types to your WhatsApp contacts:

- **Images, Videos, Documents**: Use the `send_file` tool to share any supported media type.
- **Voice Messages**: Use the `send_audio_message` tool to send audio files as playable WhatsApp voice messages.
  - For optimal compatibility, audio files should be in .ogg Opus format.
  - With FFmpeg installed, the system will automatically convert other audio formats (MP3, WAV, etc.) to the required format.
  - Without FFmpeg, you can still send raw audio files using the `send_file` tool, but they won't appear as playable voice messages.

### Receiving Media

By default, only metadata of media is stored in the local database. To access the actual media content:

1. Use the `list_messages` tool to find messages containing media
2. Note the `message_id` and `chat_jid` of the message with media
3. Use the `download_media` tool with these parameters to download the media
4. The tool will return a file path that can be used for further operations

## Architecture

This application consists of three main components:

1. **Python WhatsApp Agent** (this project): A command-line interface that integrates with Claude and the MCP server
2. **Python MCP Server** (whatsapp-mcp-server): Implements the Model Context Protocol, providing standardized tools for interacting with WhatsApp
3. **Go WhatsApp Bridge** (whatsapp-bridge): Connects to WhatsApp's web API, handles authentication, and stores message history in SQLite

## Troubleshooting

### Authentication Issues

- **QR Code Not Displaying**: Check if your terminal supports displaying QR codes. Try restarting the authentication script.
- **WhatsApp Already Logged In**: If your session is active, the Go bridge will reconnect automatically without showing a QR code.
- **Device Limit Reached**: WhatsApp limits the number of linked devices. Remove an existing device from WhatsApp on your phone (Settings > Linked Devices).
- **No Messages Loading**: After initial authentication, it can take several minutes for your message history to load, especially with many chats.
- **WhatsApp Out of Sync**: If messages get out of sync, delete both database files (whatsapp-bridge/store/messages.db and whatsapp-bridge/store/whatsapp.db) and restart the bridge to re-authenticate.

### Common Errors

- **ModuleNotFoundError**: Make sure you've installed all required dependencies with `pip install -r requirements.txt`
- **Connection Errors**: Ensure the WhatsApp bridge is running before starting the main script
- **API Key Errors**: If you're using your own Anthropic API key, verify it's correctly set in the environment variables


This project uses the [WhatsApp MCP server](https://github.com/lharries/whatsapp-mcp) by Luke Harries, which provides the underlying functionality for connecting to WhatsApp.

