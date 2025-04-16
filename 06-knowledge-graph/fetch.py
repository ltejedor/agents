import feedparser
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

def fetch_articles(feed_urls, limit=5):
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


def analyze_trends(items):
    """Dummy trend analyzer: count word frequencies in titles."""
    text = " ".join(item["title"] for item in items)
    words = re.findall(r'\b\w{4,}\b', text.lower())  # 4+ letter words
    common = Counter(words).most_common(10)
    return common
