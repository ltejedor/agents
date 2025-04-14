
import gradio as gr
from sources import RSS_FEEDS
from fetch import fetch_articles, fetch_trending_repos, analyze_trends
from analyze import cluster_items

def get_combined_feed(source_choice, selected_news_sites):
    feed_items = []

    if "News" in source_choice and selected_news_sites:
        selected_feeds = {name: url for name, url in RSS_FEEDS.items() if name in selected_news_sites}
        feed_items += fetch_articles(selected_feeds, limit=6)
    
    if "GitHub" in source_choice:
        feed_items += [
            {
                "title": repo["name"],
                "link": repo["url"],
                "summary": repo["description"],
                "published": f"{repo['stars']} stars"
            }
            for repo in fetch_trending_repos(language="python", since="daily")[:5]
        ]
    
    feed_text = "\n\n".join([f"🔹 {item['title']} ({item['published']})\n{item['link']}" for item in feed_items])

    trends_text = cluster_items(feed_items)


    return feed_text, trends_text

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=1):
            source_selector = gr.CheckboxGroup(["News", "GitHub"], value=["News"], label="Select Sources")
            news_site_selector = gr.CheckboxGroup(list(RSS_FEEDS.keys()), value=["BBC", "Wired"], label="News Sites")
        with gr.Column(scale=2):
            feed_output = gr.Textbox(label="Aggregated Feed", lines=20)
        with gr.Column(scale=2):
            trend_output = gr.Textbox(label="Top Trends", lines=20)

    source_selector.change(fn=get_combined_feed, inputs=[source_selector, news_site_selector], outputs=[feed_output, trend_output])
    news_site_selector.change(fn=get_combined_feed, inputs=[source_selector, news_site_selector], outputs=[feed_output, trend_output])

demo.launch()
