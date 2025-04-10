from pocketflow import Flow
from nodes import (
    IngestNewsFromRSS,
    SummarizeNewsArticles,
    GenerateBusinessIdea,
    ConductMarketResearch,
    PitchAndInvest,
)

def create_news_to_pitch_flow():
    # Node instances for each step in the workflow
    rss_node = IngestNewsFromRSS()
    summarize_node = SummarizeNewsArticles()
    idea_node = GenerateBusinessIdea()
    market_node = ConductMarketResearch()
    pitch_node = PitchAndInvest()

    # Chain the nodes sequentially:
    # Ingest RSS → Summarize Articles → Generate Business Idea →
    # Conduct Market Research → Pitch Generation & Investment Simulation
    rss_node >> summarize_node >> idea_node >> market_node >> pitch_node

    return Flow(start=rss_node)