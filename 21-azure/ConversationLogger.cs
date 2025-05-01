using System;
using System.IO;
using System.Text.Json;

namespace HackathonAgent
{
    /// <summary>
    /// Simple line-delimited JSON logger for conversation events.
    /// Each event is serialized as one JSON object per line (NDJSON).
    /// </summary>
    public static class ConversationLogger
    {
        private static readonly object _sync = new object();
        private static readonly string _logFilePath;

        static ConversationLogger()
        {
            _logFilePath = Environment.GetEnvironmentVariable("LOG_FILE_PATH")
                ?? "conversation.jsonl";
        }

        /// <summary>
        /// Logs an event object as a JSON line.
        /// </summary>
        /// <param name="evt">Anonymous or typed object containing event data.</param>
        public static void LogEvent(object evt)
        {
            try
            {
                var options = new JsonSerializerOptions
                {
                    WriteIndented = false
                };
                // Use runtime type for correct property serialization
                string json = JsonSerializer.Serialize(evt, evt.GetType(), options);
                lock (_sync)
                {
                    File.AppendAllText(_logFilePath, json + Environment.NewLine);
                }
            }
            catch
            {
                // Swallow logging errors to not disrupt the agent
            }
        }
    }
}