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
            "http://feeds.bbci.co.uk/news/rss.xml",
            
            # U.S. national and international headlines - NYTimes
            "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
            
            # Technology - Wired
            "https://www.wired.com/feed/rss",
            
            
            # Business/Finance - CNBC Top News
            "https://www.cnbc.com/id/100003114/device/rss/rss.html"
        ]
    
    def exec(self, feed_urls):
        all_articles = []
        for url in feed_urls:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:  # Limit to one article per feed for testing
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


class ProjectManagerAgent(Node):
    def prep(self, shared):
        # Use the ideas produced by the market research node.
        return shared.get("developed_ideas", [])
    
    def exec(self, ideas):
        updated_ideas = []
        for idea in ideas:
            prompt = f"""
You are an experienced project manager. Given the following business idea, estimate how long it would take to build a Minimum Viable Product (MVP).
Include key milestones (design, development, testing, launch) in a concise statement.
Business Idea: {idea['business_idea']}
Format your answer as a single sentence, for example:
"Estimated MVP timeline: 8-10 weeks."
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


class InvestmentAgent(Node):
    def prep(self, shared):
        return shared.get("ideas_with_pitch", [])
    
    def exec(self, ideas):
        final_results = []
        for idea in ideas:
            prompt = f"""
You are an expert investment simulator.
Based on the following business idea pitch, simulate feedback from a panel of investors which will decide on an investment amount between $0 and $10,000,000.
Return the total investment amount.
Pitch:
{idea.get('pitch', '')}

Output your answer as a single line beginning with "Investment:" followed by the total investment amount.
"""
            response = call_llm(prompt)
            # Debug output:
            print("InvestmentAgent LLM response:", response)
            
            # Update the regex to allow for an optional '$'
            match = re.search(r"Investment:\s*\$?([\d,]+)", response, re.IGNORECASE)
            if match:
                inv_str = match.group(1)
                try:
                    investment_amount = int(inv_str.replace(",", ""))
                except ValueError:
                    investment_amount = 0
            else:
                try:
                    investment_amount = int(response.strip().replace("$", "").replace(",", ""))
                except ValueError:
                    investment_amount = 0

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
                "mvp_estimate": idea.get("mvp_estimate", ""),
                "developed_idea": idea.get("developed_idea", idea["business_idea"]),
                "pitch": idea.get("pitch", ""),
                "investment_amount": idea["investment_amount"],
                "source_url": idea.get("link", ""),
                "published_at": idea.get("published", None),
            }).execute()
        print("\n===== FINAL PITCHES AND INVESTMENTS =====\n")
        for idea in exec_res:
            print(f"Title: {idea['title']}")
            print(f"Pitch: {idea.get('pitch', '')}")
            print(f"Investment Amount: {idea['investment_amount']}\n")
        return "default"
