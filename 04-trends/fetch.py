import feedparser
import requests
from bs4 import BeautifulSoup

def fetch_articles(feed_urls, limit=2):
    all_articles = []
    for name, url in feed_urls.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:limit]:
                article = {
                    "title": entry.title,
                    "link": entry.link,
                    "summary": entry.get("summary", "No summary"),
                    "published": entry.get("published", "No date")
                }
                all_articles.append(article)
        except Exception as e:
            print(f"Error parsing {url}: {e}")
    return all_articles


def fetch_trending_repos(language=None, since="daily"):
    base_url = "https://github.com/trending"
    url = f"{base_url}/{language or ''}?since={since}"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    repo_elements = soup.select("article.Box-row")

    trending = []
    for repo in repo_elements:
        title = repo.h2.get_text(strip=True).replace(" ", "")
        description_tag = repo.find("p")
        description = description_tag.get_text(strip=True) if description_tag else "No description"
        stars = repo.select_one("a[href$='/stargazers']").get_text(strip=True)
        repo_url = f"https://github.com/{title}"
        trending.append({
            "name": title,
            "description": description,
            "stars": stars,
            "url": repo_url
        })

    return trending

from collections import Counter
import re

def analyze_trends(items):
    """Dummy trend analyzer: count word frequencies in titles."""
    text = " ".join(item["title"] for item in items)
    words = re.findall(r'\b\w{4,}\b', text.lower())  # 4+ letter words
    common = Counter(words).most_common(10)
    return common
