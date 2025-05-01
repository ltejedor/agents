using System;
using System.Net.Http;
using System.Threading.Tasks;
using Microsoft.Extensions.Options;

namespace HackathonAgent
{
    // A simple plugin to perform web searches via Bing Search API
    public class WebSearchPlugin
    {
        private readonly HttpClient _httpClient;
        private readonly string _endpoint;
        private readonly string _apiKey;

        public WebSearchPlugin(HttpClient httpClient, IOptions<BingSearchOptions> options)
        {
            _httpClient = httpClient;
            _endpoint = options.Value.Endpoint;
            _apiKey = options.Value.ApiKey;
        }

        // Perform a web search and return raw JSON results (for simplicity)
        public async Task<string> SearchAsync(string query)
        {
            var request = new HttpRequestMessage(HttpMethod.Get,
                $"{_endpoint}?q={Uri.EscapeDataString(query)}&mkt=en-US&count=5");
            request.Headers.Add("Ocp-Apim-Subscription-Key", _apiKey);

            var response = await _httpClient.SendAsync(request);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadAsStringAsync();
        }
    }
}