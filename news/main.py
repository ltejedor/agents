from flow import create_news_to_startup_flow

# share store design
# shared = {
#     "news_articles": [],         # Raw RSS data
#     "summarized_articles": [],   # Short LLM-generated summaries
#     "startup_ideas": []          # List of LLM-generated ideas
# }

def main():
    shared = {}

    print("\n=== Starting News → Startup Idea Workflow ===\n")

    flow = create_news_to_startup_flow()
    flow.run(shared)

    print("\n=== Workflow Complete ===\n")
    print(f"Total ideas generated: {len(shared.get('startup_ideas', []))}")

if __name__ == "__main__":
    main()