from pocketflow import Flow
from nodes import (
    IngestNewsFromRSS,
    SummarizeNewsArticles,
    GenerateBusinessIdea,
    ConductMarketResearch,
    ProjectManagerAgent,
    PitchAgent,
    PushToDatabase
)

def create_news_to_pitch_flow():
    # Create node/agent instances
    rss_node = IngestNewsFromRSS()
    summarize_node = SummarizeNewsArticles()
    idea_node = GenerateBusinessIdea()
    market_node = ConductMarketResearch()
    pm_agent = ProjectManagerAgent()        
    pitch_agent = PitchAgent()
    db_push_node = PushToDatabase()            

    # Chain the nodes sequentially:
    rss_node >> summarize_node >> idea_node >> market_node >> pm_agent >> pitch_agent >> db_push_node

    return Flow(start=rss_node)