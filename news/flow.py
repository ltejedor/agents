from pocketflow import Flow
from nodes import IngestNewsFromRSS, SummarizeNewsArticles, GenerateStartupIdeas

def create_news_to_startup_flow():
    rss_node = IngestNewsFromRSS()
    summarize_node = SummarizeNewsArticles()
    idea_node = GenerateStartupIdeas()

    # Connect the nodes
    rss_node >> summarize_node >> idea_node

    return Flow(start=rss_node)
