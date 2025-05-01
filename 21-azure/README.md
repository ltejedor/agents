# Azure OpenAI Chatbot Agent

This project demonstrates a chatbot agent built with the Microsoft Bot Framework and Azure OpenAI. The agent can answer questions and perform web searches using Bing Search.

## Features

- Conversational AI powered by Azure OpenAI
- Web search capabilities using Bing Search API
- Built with .NET 8 and Microsoft Bot Framework
- Conversation logging to JSONL files

## Prerequisites

- [.NET 8 SDK](https://dotnet.microsoft.com/download/dotnet/8.0)
- [Bot Framework Emulator](https://github.com/microsoft/BotFramework-Emulator/releases/latest)
- Azure subscription with access to Azure OpenAI and Bing Search services

## Azure Setup

### 1. Create an Azure OpenAI Resource

1. Go to the [Azure Portal](https://portal.azure.com/#home)
2. Click on "Create a resource" and search for "Azure OpenAI"
3. Select "Azure OpenAI" and click "Create"
4. Fill in the required details:
   - Subscription: Your Azure subscription
   - Resource group: Create new or select existing
   - Region: Choose a supported region
   - Name: Give your resource a unique name
   - Pricing tier: Select appropriate tier
5. Click "Review + create" and then "Create"

### 2. Create a Model Deployment

1. Once your Azure OpenAI resource is created, go to its overview page
2. Click on "Go to Azure OpenAI Studio"
3. Navigate to "Deployments" in the left sidebar
4. Click "Create new deployment"
5. Select a model (e.g., GPT-4, GPT-3.5-Turbo)
6. Give your deployment a name (you'll need this for the configuration)
7. Set the deployment options and click "Create"

### 3. Set Up Bing Search API (Optional, for search functionality)

1. Go to the [Azure Portal](https://portal.azure.com/#home)
2. Click on "Create a resource" and search for "Bing Search"
3. Select "Bing Search" and click "Create"
4. Fill in the required details and create the resource
5. Once created, go to the "Keys and Endpoint" section to get your API key

## Configuration

Update the `appsettings.json` file with your Azure OpenAI and Bing Search credentials:

```json
{
  "AIServices": {
    "AzureOpenAI": {
      "Endpoint": "https://your-openai-resource.openai.azure.com/",
      "ApiKey": "your-openai-api-key",
      "DeploymentName": "your-model-deployment-name"
    },
    "BingSearch": {
      "Endpoint": "https://api.bing.microsoft.com/v7.0/search",
      "ApiKey": "your-bing-search-api-key"
    }
  }
}
```

## Building and Running

1. Build the project:
   ```
   dotnet build
   ```

2. Run the project:
   ```
   dotnet run
   ```

The bot will start listening on `http://localhost:3978`.

## Connecting with Bot Framework Emulator

1. Open the Bot Framework Emulator
2. Click on "Open Bot"
3. Enter the bot URL: `http://localhost:3978/api/messages`
4. Leave the Microsoft App ID and Microsoft App Password fields empty for local testing
5. Click "Connect"

## Using the Bot

- Type any message to chat with the bot
- Use `/search <query>` to perform a web search (e.g., `/search latest AI news`)

## Conversation Logging

Conversations are logged to a file named `conversation.jsonl` in the application directory. You can change the log file path by setting the `LOG_FILE_PATH` environment variable.