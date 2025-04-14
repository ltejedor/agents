# General world news - BBC
# "http://feeds.bbci.co.uk/news/rss.xml",

# U.S. national and international headlines - NYTimes
# "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",

# Technology - Wired
# "https://www.wired.com/feed/rss",


# Business/Finance - CNBC Top News
# "https://www.cnbc.com/id/100003114/device/rss/rss.html"

# the guardian
# "https://www.theguardian.com/world/rss",

# Wall street journal
# "https://feeds.a.dj.com/rss/RSSWorldNews.xml",

# Altpress - music
# "https://www.altpress.com/feed/"

# "https://fortune.com/feed/fortune-feeds/?id=3230629",

# "https://www.nerdwallet.com/blog/feed/"

# "http://feeds.mashable.com/Mashable"

# "https://www.theverge.com/rss/index.xml"

# "https://www.atlasobscura.com/feeds/latest"
# "https://hacks.mozilla.org/feed/"
# "https://www.cnet.com/rss/news/"
# "https://www.inc.com/rss/"

# "https://rss.nytimes.com/services/xml/rss/nyt/FashionandStyle.xml"
# "https://www.youtube.com/feeds/videos.xml?user=Bloomberg"
# "https://blog.google/rss/"
# "https://stackoverflow.blog/feed/"
# "https://feeds2.feedburner.com/SmallBusinessTrends"
# "https://www.theguardian.com/uk/travel/rss"
# "https://www.smashingmagazine.com/feed"
# "https://www.nasa.gov/news-release/feed/"
# "https://sciencebasedmedicine.org/feed/"


import feedparser
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from html.parser import HTMLParser

import requests
from bs4 import BeautifulSoup
import feedparser

def extract_from_rss(url):
    feed = feedparser.parse(url)
    news_items = []
    for entry in feed.entries:
        news_items.append({
            'title': entry.get('title', ''),
            'link': entry.get('link', ''),
            'summary': entry.get('summary', entry.get('description', ''))
        })
    return news_items

def extract_from_html(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.content, 'html.parser')
        elements = soup.find_all(['h1', 'h2', 'h3', 'p'], limit=30)
        return [{'title': tag.get_text(strip=True), 'link': url, 'summary': ''} for tag in elements if len(tag.get_text(strip=True)) > 20]
    except Exception as e:
        return [{'title': f'Failed to parse HTML: {e}', 'link': url, 'summary': ''}]

def extract_news(url):
    try:
        if any(x in url.lower() for x in ['rss', 'feed', '.xml']):
            print("🔎 Detected RSS feed...")
            news = extract_from_rss(url)
            if news:
                return news
        print("🌐 Falling back to HTML content...")
        return extract_from_html(url)
    except Exception as e:
        return [{'title': f'General failure: {e}', 'link': url, 'summary': ''}]

# 🧪 Example usage:
if __name__ == "__main__":
    test_url = input("Enter any RSS or website URL: ").strip()
    results = extract_news(test_url)
    for i, item in enumerate(results[:10], 1):
        print(f"\n[{i}] {item['title']}\n{item['link']}")

