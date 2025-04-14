from sentence_transformers import SentenceTransformer
import hdbscan

model = SentenceTransformer("all-MiniLM-L6-v2")

def cluster_items(items, min_cluster_size=2):
    texts = [item["title"] for item in items]
    if not texts:
        return []

    embeddings = model.encode(texts)
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, metric="euclidean")
    labels = clusterer.fit_predict(embeddings)

    clusters = {}
    for label, text in zip(labels, texts):
        if label == -1:
            continue
        clusters.setdefault(label, []).append(text)

    cluster_text = []
    for i, titles in clusters.items():
        cluster_text.append(f"🔸 Cluster {i} ({len(titles)} items):")
        cluster_text.extend(f"- {t}" for t in titles)
        cluster_text.append("")  # add space between clusters

    return "\n".join(cluster_text) or "No meaningful clusters found."
