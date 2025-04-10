from pocketflow import Node
import feedparser
import yaml
import re
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
            for entry in feed.entries[:1]:  # Limit to top 5 per feed
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


class GenerateBusinessIdea(Node):
    def prep(self, shared):
        return shared.get("summarized_articles", [])
    
    def exec(self, articles):
        business_ideas = []
        for article in articles:
            prompt = f"""
Generate a high-level business idea based on the following news summary.
Include:
- The target user
- The key problem being solved
- A brief description of the idea

Title: {article['title']}
Summary: {article['summary']}

Format your response as follows:
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

class PitchAndInvest(Node):
    def prep(self, shared):
        return shared.get("developed_ideas", [])
    
    def exec(self, ideas):
        final_results = []
        for idea in ideas:
            prompt = f"""
You are an expert pitch creator and investment simulator.
Based on the following business idea and market research, create a compelling pitch.
Then, simulate feedback from a panel of 5 investors – each investor will decide on an investment amount between $0 and $10,000,000.
Sum all the amounts from the 5 investors to calculate a final total investment amount.

Business Idea and Research:
{idea['developed_idea']}

Output your response in YAML format exactly as follows:
~~~yaml
pitch: <The pitch text>
investment_amount: <Total investment amount as a number>
~~~
            """
            response = call_llm(prompt)
            try:
                # Look for a YAML block enclosed in triple backticks with "yaml"
                # (If you prefer backticks, you can revert; using tildes here avoids markdown interference.)
                yaml_block =  re.search(r"yaml(.*?)", response, re.DOTALL)
                if yaml_block:
                    yaml_content = yaml_block.group(1).strip()
                else:
                    yaml_content = response.strip()
                parsed = yaml.safe_load(yaml_content)
                pitch = parsed.get("pitch", "")
                inv_raw = parsed.get("investment_amount", 0)
                # Convert investment_amount to integer if it is a string with commas.
                if isinstance(inv_raw, str):
                    try:
                        investment_amount = int(inv_raw.replace(",", ""))
                    except ValueError:
                        investment_amount = 0
                else:
                    investment_amount = inv_raw
            except Exception as e:
                pitch = response
                investment_amount = 0

            idea["pitch"] = pitch
            idea["investment_amount"] = investment_amount
            final_results.append(idea)
        return final_results



    def post(self, shared, prep_res, exec_res):
        shared["final_ideas"] = exec_res
        # Save each idea to the database with the investment amount
        for idea in exec_res:
            supabase.table("startup_ideas").insert({
                "title": idea["title"],
                "business_idea": idea["business_idea"],
                "developed_idea": idea["developed_idea"],
                "pitch": idea["pitch"],
                "investment_amount": idea["investment_amount"],
                "source_url": idea.get("link", ""),
                "published_at": idea.get("published", None),
            }).execute()
        print("\n===== FINAL PITCHES AND INVESTMENTS =====\n")
        for idea in exec_res:
            print(f"Title: {idea['title']}")
            print(f"Pitch: {idea['pitch']}")
            print(f"Investment Amount: {idea['investment_amount']}\n")
        return "default"