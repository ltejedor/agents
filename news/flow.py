from pocketflow import Flow
from nodes import (
    IngestNewsFromRSS,
    SummarizeNewsArticles,
    GenerateBusinessIdea,
    ConductMarketResearch,
    ProjectManagerAgent,
    PitchAgent,
    InvestmentAgent,
)

def create_news_to_pitch_flow():
    # Create node/agent instances
    rss_node = IngestNewsFromRSS()
    summarize_node = SummarizeNewsArticles()
    idea_node = GenerateBusinessIdea()
    market_node = ConductMarketResearch()
    pm_agent = ProjectManagerAgent()         # New agent: Project management/MVP estimation
    pitch_agent = PitchAgent()               # New agent: Responsible solely for generating the pitch
    invest_agent = InvestmentAgent()         # New agent: Responsible solely for simulating investor feedback

    # Chain the nodes sequentially:
    # RSS ingestion → Summarization → Business idea generation → TAM research →
    # Market research → MVP timeline estimation → Pitch creation → Investment simulation
    rss_node >> summarize_node >> idea_node >> market_node >> pm_agent >> pitch_agent >> invest_agent

    return Flow(start=rss_node)