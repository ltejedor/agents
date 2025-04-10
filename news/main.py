from flow import create_news_to_pitch_flow

def main():
    shared = {}
    print("\n=== Starting News → Business Pitch Workflow ===\n")
    flow = create_news_to_pitch_flow()
    flow.run(shared)
    print("\n=== Workflow Complete ===\n")
    final_ideas = shared.get("final_ideas", [])
    print(f"Total Ideas Processed: {len(final_ideas)}")
    
if __name__ == "__main__":
    main()