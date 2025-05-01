using System;
using System.Threading;
using System.Threading.Tasks;
using Azure;
using Azure.AI.OpenAI;
using Azure.Core;
using System.Collections.Generic;
using OpenAI.Chat;
using Microsoft.Extensions.Configuration;
using Microsoft.Agents.Builder;
using Microsoft.Agents.Builder.App;
using Microsoft.Agents.Builder.State;
using Microsoft.Agents.Core.Models;

namespace HackathonAgent
{
    // An Agent that can stream chat responses and perform web searches
    public class HackathonAgent : AgentApplication
    {
        private readonly AzureOpenAIClient _openAiClient;
        private readonly ChatClient _chatClient;
        private readonly WebSearchPlugin _searchPlugin;

        public HackathonAgent(AgentApplicationOptions options,
                              AzureOpenAIClient openAiClient,
                              IConfiguration configuration,
                              WebSearchPlugin searchPlugin)
            : base(options)
        {
            _openAiClient = openAiClient;
            // Initialize chat client for Azure OpenAI
            var deployment = configuration["AIServices:AzureOpenAI:DeploymentName"];
            _chatClient = _openAiClient.GetChatClient(deployment);
            _searchPlugin = searchPlugin;

            // Greet new users
            OnConversationUpdate(ConversationUpdateEvents.MembersAdded, WelcomeMessageAsync);
            // Handle incoming messages
            OnActivity(ActivityTypes.Message, OnMessageAsync, rank: RouteRank.Last);
            // Global error handler
            OnTurnError(OnTurnErrorAsync);
        }

        private async Task WelcomeMessageAsync(ITurnContext turnContext, ITurnState turnState, CancellationToken cancellationToken)
        {
            foreach (var member in turnContext.Activity.MembersAdded)
            {
                if (member.Id != turnContext.Activity.Recipient.Id)
                {
                    await turnContext.SendActivityAsync(
                        "Welcome! Ask me anything, or type /search <query> to search the web.",
                        cancellationToken: cancellationToken);
                }
            }
        }

        private async Task OnMessageAsync(ITurnContext turnContext, ITurnState turnState, CancellationToken cancellationToken)
        {
            var text = turnContext.Activity.Text?.Trim();
            if (string.IsNullOrEmpty(text))
                return;

            // Log the incoming user message
            ConversationLogger.LogEvent(new
            {
                Timestamp = DateTime.UtcNow,
                Type = "UserMessage",
                ConversationId = turnContext.Activity.Conversation.Id,
                Text = text
            });

            // Handle search command
            const string searchCommand = "/search";
            if (text.StartsWith(searchCommand, StringComparison.OrdinalIgnoreCase))
            {
                var query = text.Length > searchCommand.Length ? text.Substring(searchCommand.Length).Trim() : string.Empty;
                if (string.IsNullOrEmpty(query))
                {
                    await turnContext.SendActivityAsync(MessageFactory.Text("Usage: /search <query>"), cancellationToken);
                }
                else
                {
                    await turnContext.SendActivityAsync(MessageFactory.Text($"Searching the web for '{query}'..."), cancellationToken);
                    try
                    {
                        // Log the tool invocation
                        ConversationLogger.LogEvent(new
                        {
                            Timestamp = DateTime.UtcNow,
                            Type = "ToolInvocation",
                            ConversationId = turnContext.Activity.Conversation.Id,
                            Tool = "WebSearch",
                            Query = query
                        });
                        var results = await _searchPlugin.SearchAsync(query);
                        // Log the tool result
                        ConversationLogger.LogEvent(new
                        {
                            Timestamp = DateTime.UtcNow,
                            Type = "ToolResult",
                            ConversationId = turnContext.Activity.Conversation.Id,
                            Tool = "WebSearch",
                            Results = results
                        });
                        await turnContext.SendActivityAsync(MessageFactory.Text(results), cancellationToken);
                    }
                    catch (Exception ex)
                    {
                        await turnContext.SendActivityAsync(MessageFactory.Text($"Search failed: {ex.Message}"), cancellationToken);
                    }
                }
                return;
            }

            await turnContext.SendActivityAsync(
                MessageFactory.Text("Thinking..."),
                cancellationToken);

            // Build chat messages using role-specific message types
            var messages = new List<ChatMessage>
            {
                new SystemChatMessage("You are a helpful assistant."),
                new UserChatMessage(text)
            };

            // Chat completion options (customize if desired)
            var chatOptions = new ChatCompletionOptions();

            // Invoke chat completion
            var chatResponse = await _chatClient.CompleteChatAsync(
                messages,
                chatOptions,
                cancellationToken);
            var chatCompletion = chatResponse.Value;
            // Convert ChatMessageContent to string by concatenating parts
            var sb = new System.Text.StringBuilder();
            foreach (var part in chatCompletion.Content)
            {
                // Each part may contain a Text property
                if (!string.IsNullOrEmpty(part.Text))
                {
                    sb.Append(part.Text);
                }
            }
            var result = sb.ToString();
            // Log the outgoing bot message
            ConversationLogger.LogEvent(new
            {
                Timestamp = DateTime.UtcNow,
                Type = "BotMessage",
                ConversationId = turnContext.Activity.Conversation.Id,
                Text = result
            });

            await turnContext.SendActivityAsync(
                MessageFactory.Text(result),
                cancellationToken);
        }

        private async Task OnTurnErrorAsync(ITurnContext turnContext, ITurnState turnState, Exception exception, CancellationToken cancellationToken)
        {
            // Clear conversation state on error
            await turnState.Conversation.DeleteStateAsync(turnContext, cancellationToken);

            var eoc = Activity.CreateEndOfConversationActivity();
            eoc.Code = EndOfConversationCodes.Error;
            eoc.Text = exception.Message;
            await turnContext.SendActivityAsync(eoc, cancellationToken);
        }
    }
}