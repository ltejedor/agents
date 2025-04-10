from pocketflow import Node
import feedparser
from utils.llm import call_llm
from utils.supabase_client import supabase


class IngestNewsFromRSS(Node):
    def prep(self, shared):
        # Define the RSS feed URLs (you can add more or make this dynamic)
        return [
            "http://feeds.bbci.co.uk/news/rss.xml",
            "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
        ]
    
    def exec(self, feed_urls):
        all_articles = []

        for url in feed_urls:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:  # Limit to top 5 per feed
                article = {
                    "title": entry.title,
                    "link": entry.link,
                    "summary": entry.summary,
                    "published": entry.get("published", "")
                }
                all_articles.append(article)

        return all_articles

    def post(self, shared, prep_res, exec_res):
        shared["news_articles"] = exec_res

        print("\n===== INGESTED NEWS ARTICLES =====\n")
        for i, article in enumerate(exec_res):
            print(f"{i+1}. {article['title']} ({article['published']})")
            print(article['link'])
            print()
        print("==================================\n")

        return "default"


class SummarizeNewsArticles(Node):
    def prep(self, shared):
        return shared.get("news_articles", [])
    
    def exec(self, articles):
        summarized_articles = []

        for article in articles:
            prompt = f"""
Summarize the following news article in 3-4 sentences using clear and neutral language.

Title: {article['title']}
Summary Snippet: {article['summary']}

Only use the information given above. Do not make anything up.
"""
            summary = call_llm(prompt)
            summarized_articles.append({
                "title": article["title"],
                "link": article["link"],
                "summary": summary,
                "published": article["published"]
            })

        return summarized_articles

    def post(self, shared, prep_res, exec_res):
        shared["summarized_articles"] = exec_res

        print("\n===== SUMMARIZED ARTICLES =====\n")
        for article in exec_res:
            print(f"📰 {article['title']}")
            print(f"📅 {article['published']}")
            print(f"🔗 {article['link']}")
            print(f"📝 {article['summary']}\n")
        print("=================================\n")

        return "default"

class GenerateStartupIdeas(Node):
    def prep(self, shared):
        return shared.get("summarized_articles", [])
    
    def exec(self, summaries):
        startup_ideas = []
        for article in summaries:
            prompt = f"""
Given the news article titled "{article['title']}" summarized as:

{article['summary']}

Generate one creative and feasible startup idea that responds to this trend or issue. 
Format:
- Name: <Startup Name>
- Idea: <Description of what the startup does and why it matters>
"""
            idea_text = call_llm(prompt)
            startup_ideas.append({
                "title": article["title"],
                "summary": article["summary"],
                "link": article["link"],
                "published": article["published"],
                "idea": idea_text
            })
        return startup_ideas

    def post(self, shared, prep_res, exec_res):
        shared["startup_ideas"] = exec_res

        for idea in exec_res:
            supabase.table("startup_ideas").insert({
                "title": idea["title"],
                "summary": idea["summary"],
                "idea_name": "TODO: parse name from idea text",
                "idea_description": idea["idea"],
                "source_url": idea.get("link", ""),
                "published_at": idea.get("published", None),
            }).execute()

        print("\n===== GENERATED STARTUP IDEAS =====\n")
        for idea in exec_res:
            print(f"📰 {idea['title']}\n💡 {idea['idea']}\n")
        print("===================================\n")

        return "default"
