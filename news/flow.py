from pocketflow import Flow
from nodes import (
    IngestNewsFromRSS,
    SummarizeNewsArticles,
    GenerateBusinessIdea,
    ConductMarketResearch,
    CompetitorSearchTerm,   # Updated competitor node
    SearchCompetitors,
    FilterCompetitorResults,
    ProjectManagerAgent,
    PitchAgent,
    PushToDatabase
)

def create_news_to_pitch_flow() -> Flow:
    """
    Create and return the complete workflow. The competitor branch is now a linear workflow.
    """
    # Create initial nodes.
    rss_node = IngestNewsFromRSS()
    summarize_node = SummarizeNewsArticles()
    idea_node = GenerateBusinessIdea()
    market_node = ConductMarketResearch()
    
    # Competitor branch in a linear sequence.
    competitor_search = CompetitorSearchTerm()
    search_competitors = SearchCompetitors()
    filter_results = FilterCompetitorResults()
    
    # Remaining nodes.
    pm_agent = ProjectManagerAgent()
    pitch_agent = PitchAgent()
    db_push_node = PushToDatabase()

    # Chain the nodes.
    rss_node >> summarize_node >> idea_node >> market_node >> competitor_search >> search_competitors >> filter_results >> pm_agent >> pitch_agent >> db_push_node

    return Flow(start=rss_node)
