from flow import create_news_to_pitch_flow
from utils.visualizer import save_as_image


def main():
    shared = {}
    print("\n=== Starting News → Business Pitch Workflow ===\n")
    flow = create_news_to_pitch_flow()

    # Generate and save the flow visualization
    save_as_image(flow, "news_flow_diagram.png")
    
    flow.run(shared)
    print("\n=== Workflow Complete ===\n")
    final_ideas = shared.get("final_ideas", [])
    print(f"Total Ideas Processed: {len(final_ideas)}")
    
if __name__ == "__main__":
    main()