using System;
using Azure.AI.OpenAI;
using Azure;
using Azure.Core;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Configuration;
using Microsoft.Agents.Builder;
using Microsoft.Agents.Hosting.AspNetCore;
using Microsoft.Agents.Storage;
using HackathonAgent;
using System.Threading;

var builder = WebApplication.CreateBuilder(args);

// In development, you can store secrets locally with user-secrets
if (builder.Environment.IsDevelopment())
{
    builder.Configuration.AddUserSecrets<Program>();
}

 builder.Services.AddControllers();
 builder.Services.AddHttpClient();
 builder.Logging.AddConsole();
 // Configure Bing search plugin settings and register plugin
 builder.Services.Configure<BingSearchOptions>(builder.Configuration.GetSection("AIServices:BingSearch"));
 builder.Services.AddSingleton<WebSearchPlugin>();

// Register Azure OpenAI client (for chat completions with built-in Bing grounding tool)
builder.Services.AddSingleton(sp =>
{
    var cfg = sp.GetRequiredService<IConfiguration>();
    var endpoint = new Uri(cfg["AIServices:AzureOpenAI:Endpoint"]);
    var apiKey = cfg["AIServices:AzureOpenAI:ApiKey"];
    return new AzureOpenAIClient(endpoint, new AzureKeyCredential(apiKey));
});

// (Optional) Add ASP.NET authentication if deploying to Azure
// builder.Services.AddAgentAspNetAuthentication(builder.Configuration);

// Register Agent, storage, and options
builder.AddAgentApplicationOptions();
builder.AddAgent<HackathonAgent.HackathonAgent>();
builder.Services.AddSingleton<IStorage, MemoryStorage>();

var app = builder.Build();

app.UseRouting();

app.MapPost("/api/messages", async (HttpRequest request, HttpResponse response, IAgentHttpAdapter adapter, IAgent agent, CancellationToken ct) =>
{
    await adapter.ProcessAsync(request, response, agent, ct);
})
// Allow anonymous for local testing
.AllowAnonymous();

// Set the listening URL (for local testing)
app.Urls.Add("http://localhost:3978");
app.Run();