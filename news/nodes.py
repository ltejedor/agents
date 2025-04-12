# news/nodes.py
from pocketflow import Node
import feedparser
import yaml
import re
from utils.llm import call_llm
from utils.supabase_client import supabase

### Existing Nodes

class IngestNewsFromRSS(Node):
    def prep(self, shared):
        # Define the RSS feed URLs (you can add more or make this dynamic)
        return [
            # General world news - BBC
            #"http://feeds.bbci.co.uk/news/rss.xml",
            
            # U.S. national and international headlines - NYTimes
           # "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
            
            # Technology - Wired
            #"https://www.wired.com/feed/rss",
            
            
            # Business/Finance - CNBC Top News
            #"https://www.cnbc.com/id/100003114/device/rss/rss.html"

            # the guardian
            #"https://www.theguardian.com/world/rss",

            # Wall street journal
            #"https://feeds.a.dj.com/rss/RSSWorldNews.xml",

            # Altpress - music
            #"https://www.altpress.com/feed/"

            #"https://fortune.com/feed/fortune-feeds/?id=3230629",

            #"https://www.nerdwallet.com/blog/feed/"
            
            #"http://feeds.mashable.com/Mashable"

            #"https://www.theverge.com/rss/index.xml"

            #"https://www.atlasobscura.com/feeds/latest"
            #"https://hacks.mozilla.org/feed/"
            #"https://www.cnet.com/rss/news/"
            #"https://www.inc.com/rss/"

            #"https://rss.nytimes.com/services/xml/rss/nyt/FashionandStyle.xml"
            #"https://www.youtube.com/feeds/videos.xml?user=Bloomberg"
            #"https://blog.google/rss/"
            #"https://stackoverflow.blog/feed/"
            #"https://feeds2.feedburner.com/SmallBusinessTrends"
            #"https://www.theguardian.com/uk/travel/rss"
            #"https://www.smashingmagazine.com/feed"
            #"https://www.nasa.gov/news-release/feed/"
            #"https://sciencebasedmedicine.org/feed/"
        ]
    
    def exec(self, feed_urls):
        all_articles = []
        for url in feed_urls:
            feed = feedparser.parse(url)
            for entry in feed.entries[:2]:  # Limit to one article per feed for testing
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
            print(article['link'], "\n")
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

class GenerateBusinessIdea(Node):
    def prep(self, shared):
        return shared.get("summarized_articles", [])
    
    def exec(self, articles):
        business_ideas = []
        for article in articles:
            prompt = f"""
Generate a high-level business idea based on the following news summary.
Include:
- The startup's name
- The target user
- The key problem being solved
- A brief description of the idea

Title: {article['title']}
Summary: {article['summary']}

Format your response as follows:
Startup: <startup name>
User: <target user>
Problem: <problem statement>
Idea: <brief description>
"""
            idea_text = call_llm(prompt)
            business_ideas.append({
                "title": article["title"],
                "business_idea": idea_text,
                "link": article["link"],
                "published": article["published"]
            })
        return business_ideas
    
    def post(self, shared, prep_res, exec_res):
        shared["business_ideas"] = exec_res
        print("\n===== GENERATED BUSINESS IDEAS =====\n")
        for idea in exec_res:
            print(f"Title: {idea['title']}")
            print(f"Idea: {idea['business_idea']}\n")
        return "default"


class CompetitorSearchTerm(Node):
    """
    For each developed business idea, generate a competitor search term using an LLM.
    This node simply generates and outputs a search term (or empty string) for competitor analysis.
    """
    def prep(self, shared: dict) -> dict:
        developed_ideas = shared.get("developed_ideas", [])
        current_index = shared.get("current_idea_index", 0)
        if current_index >= len(developed_ideas):
            raise ValueError("No more ideas left for competitor search.")
        idea = developed_ideas[current_index]
        business_idea = idea.get("business_idea", "Unknown business idea")
        return {"business_idea": business_idea}
    
    def exec(self, inputs: dict) -> dict:
        business_idea = inputs["business_idea"]
        prompt = f"""
Business Idea: {business_idea}
Generate a concise competitor search term that would be useful for retrieving competitor information.
Return your answer in YAML format as follows:

```yaml
search_term: <search term, or an empty string if none>
```"""
        response = call_llm(prompt)
        print("CompetitorSearchTerm response:", response)
        try:
            yaml_str = response.split("```yaml")[1].split("```")[0].strip()
            result = yaml.safe_load(yaml_str)
        except Exception as e:
            print(f"Error parsing YAML in CompetitorSearchTerm: {e}")
            raise ValueError("Failed to parse CompetitorSearchTerm response.")
        if "search_term" not in result:
            raise ValueError("search_term not found in CompetitorSearchTerm response.")
        return result
    
    def post(self, shared: dict, prep_res, exec_res: dict) -> str:
        shared["competitor_search_term"] = exec_res.get("search_term", "")
        return "default"


class SearchCompetitors(Node):
    """
    Performs a DuckDuckGo search for competitor information using the provided search term.
    Returns raw search results (a list of dictionaries).
    """
    def prep(self, shared: dict) -> str:
        search_term = shared.get("competitor_search_term", "")
        return search_term
    
    def exec(self, search_term: str) -> list:
        from utils.search import search_web  # Lazy import.
        if not search_term:
            print("No competitor search term provided. Skipping search.")
            return []
        print("Performing competitor search with term:", search_term)
        results = search_web(search_term, raw=True)
        print("Raw competitor search results:", results)
        return results
    
    def post(self, shared: dict, prep_res, exec_res: list) -> str:
        shared["raw_competitor_results"] = exec_res
        return "default"


class FilterCompetitorResults(Node):
    """
    Processes raw search results using an LLM to extract/summarize competitor information.
    Returns a plain string of competitor names and updates the current idea.
    """
    def prep(self, shared: dict) -> dict:
        raw_results = shared.get("raw_competitor_results", [])
        developed_ideas = shared.get("developed_ideas", [])
        current_index = shared.get("current_idea_index", 0)
        business_idea = developed_ideas[current_index].get("business_idea", "Unknown business idea")
        return {"raw_results": raw_results, "business_idea": business_idea}
    
    def exec(self, inputs: dict) -> str:
        raw_results = inputs["raw_results"]
        business_idea = inputs["business_idea"]
        prompt = f"""
Business Idea: {business_idea}
Raw Search Results (in JSON format): {raw_results}
Extract and summarize any competitor information relevant to this business idea.
Return your answer as a plain string containing only the competitor names (no extra explanation).
"""
        response = call_llm(prompt)
        print("FilterCompetitorResults response:", response)
        return response.strip()
    
    def post(self, shared: dict, prep_res, exec_res: str) -> str:
        developed_ideas = shared.get("developed_ideas", [])
        current_index = shared.get("current_idea_index", 0)
        developed_ideas[current_index]["competitor_info"] = exec_res
        print("Updated competitor info for idea", current_index, ":", exec_res)
        return "default"



class ProjectManagerAgent(Node):
    def prep(self, shared):
        # Use the ideas produced by the market research node.
        return shared.get("developed_ideas", [])
    
    def exec(self, ideas):
        updated_ideas = []
        for idea in ideas:
            prompt = f"""
You are an experienced project manager. Given the following business idea, estimate how long it would take to build a Minimum Viable Product (MVP).
Are there any regulations or infrastructure requirements that will hold things up? Or could a developer put out something live in a few days?
Business Idea: {idea['business_idea']}
Format your answer as a single sentence. Start with the time it would take and then an explanation, such as: 
2-3 Weeks, [reason]
"""
            mvp_estimate = call_llm(prompt)
            idea["mvp_estimate"] = mvp_estimate
            updated_ideas.append(idea)
        return updated_ideas
    
    def post(self, shared, prep_res, exec_res):
        shared["ideas_with_pm"] = exec_res
        print("\n===== MVP TIMELINE ESTIMATES =====\n")
        for idea in exec_res:
            print(f"Title: {idea['title']}")
            print(f"MVP Estimate: {idea['mvp_estimate']}\n")
        return "default"



class ConductMarketResearch(Node):
    def prep(self, shared):
        return shared.get("business_ideas", [])
    
    def exec(self, ideas):
        developed_ideas = []
        for idea in ideas:
            prompt = f"""
You are a market research expert. Further develop the following business idea by providing detailed market research.
Include information about potential competitors, market size, growth opportunities, and key challenges.
Business Idea: {idea['business_idea']}

Provide your response in a clear, structured summary.
"""
            market_research = call_llm(prompt)
            idea["developed_idea"] = market_research
            developed_ideas.append(idea)
        return developed_ideas
    
    def post(self, shared, prep_res, exec_res):
        shared["developed_ideas"] = exec_res
        print("\n===== DEVELOPED BUSINESS IDEAS WITH MARKET RESEARCH =====\n")
        for idea in exec_res:
            print(f"Title: {idea['title']}")
            print(f"Developed Idea: {idea['developed_idea']}\n")
        return "default"

class PitchAgent(Node):
    def prep(self, shared):
        return shared.get("ideas_with_pm", [])
    
    def exec(self, ideas):
        final_results = []
        for idea in ideas:
            prompt = f"""
You are an expert pitch creator.
Based on the following business idea, TAM research, market research, and MVP timeline, create a compelling pitch.
Business Idea and Research:
{idea.get('developed_idea', idea.get('business_idea'))}
MVP Timeline: {idea.get('mvp_estimate', 'N/A')}

Output your pitch as a single line that begins with "Pitch:".
"""
            response = call_llm(prompt)
            # Assume the response is something like: "Pitch: <pitch text>"
            if "Pitch:" in response:
                pitch = response.split("Pitch:")[1].strip()
            else:
                pitch = response.strip()
            idea["pitch"] = pitch
            final_results.append(idea)
        return final_results
    
    def post(self, shared, prep_res, exec_res):
        shared["ideas_with_pitch"] = exec_res
        print("\n===== FINAL PITCHES =====\n")
        for idea in exec_res:
            print(f"Title: {idea['title']}")
            print(f"Pitch: {idea['pitch']}\n")
        return "default"


class PushToDatabase(Node):
    def prep(self, shared):
        # Retrieve final ideas from previous node (typically PitchAgent)
        return shared.get("ideas_with_pitch", [])
    
    def exec(self, ideas):
        # Iterate over each idea and insert it into the Supabase database
        for idea in ideas:
            supabase.table("startup_ideas").insert({
                "title": idea["title"],
                "business_idea": idea["business_idea"],
                "mvp_estimate": idea.get("mvp_estimate", ""),
                "developed_idea": idea.get("developed_idea", idea["business_idea"]),
                "pitch": idea.get("pitch", ""),
                "source_url": idea.get("link", ""),
                "published_at": idea.get("published", None),
                "competitors": idea.get("competitor_info", "")
            }).execute()
        # Return the ideas (or a success confirmation) for logging purposes
        return ideas
    
    def post(self, shared, prep_res, exec_res):
        shared["final_ideas"] = exec_res
        print("\n===== FINAL IDEAS PUSHED TO DATABASE =====\n")
        for idea in exec_res:
            print(f"Title: {idea['title']}")
            print(f"Pitch: {idea.get('pitch', '')}\n")
        return "default"