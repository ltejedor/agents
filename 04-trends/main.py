# today
# bring in another tranding source 
# put together with news in gradio
# with trends in the middle (generalizeable function in between)

from sources import RSS_FEEDS
from fetch import fetch_articles, fetch_trending_repos

def show_news():
    print("\n===== NEWS ARTICLES =====\n")
    articles = fetch_articles(RSS_FEEDS, limit=2)
    for i, article in enumerate(articles):
        print(f"{i+1}. {article['title']} ({article['published']})")
        print(article['link'])
        print()

def show_github():
    print("\n===== TRENDING GITHUB REPOS =====\n")
    repos = fetch_trending_repos(language="python", since="daily")
    for i, repo in enumerate(repos[:10]):
        print(f"{i+1}. {repo['name']} ({repo['stars']} stars)")
        print(repo['description'])
        print(repo['url'])
        print()

if __name__ == "__main__":
    show_news()
    show_github()