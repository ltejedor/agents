import gradio as gr
import networkx as nx
import spacy
import plotly.graph_objects as go

from sources import RSS_FEEDS
from fetch import fetch_articles

# Imports for the LLM knowledge graph transformer
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_experimental.graph_transformers import LLMGraphTransformer

# Load the spaCy model (kept for other tasks if needed)
nlp = spacy.load("en_core_web_sm")

def build_interactive_knowledge_graph(feed_items):
    """
    Build an interactive knowledge graph from aggregated RSS feed text using an LLM.
    
    Steps:
      1. Combine the title and summary of all feed items.
      2. Create a Document and split it into chunks.
      3. Use ChatOpenAI and LLMGraphTransformer to get graph information.
      4. Merge nodes and relationships into a directed NetworkX graph.
      5. Compute a spring layout and convert the graph to a Plotly figure.
      6. Compute node hover text showing all outgoing/incoming connections.
      7. Re-add arrow annotations to indicate direction (with no extra text).
      8. Return the Plotly figure.
    """
    # 1. Combine all feed items into one aggregated text.
    combined_text = "\n\n".join([f"{item['title']}. {item['summary']}" for item in feed_items])
    
    # 2. Create a Document and split it.
    doc = Document(page_content=combined_text)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents([doc])
    
    # 3. Initialize the LLM and transformer.
    llm = ChatOpenAI(temperature=0, model="gpt-4o")
    llm_transformer = LLMGraphTransformer(llm=llm)
    graph_documents = llm_transformer.convert_to_graph_documents(docs)
    
    # 4. Build a directed NetworkX graph.
    G = nx.DiGraph()
    for graph_doc in graph_documents:
        # Convert the Pydantic model to a dictionary.
        gdoc = graph_doc.model_dump()
        nodes = gdoc.get("nodes", [])
        # In these documents, relationships are stored under "relationships".
        relationships = gdoc.get("relationships", [])
        
        # Add nodes.
        for node in nodes:
            node_id = node.get("id") or node.get("name")
            if node_id:
                G.add_node(node_id)
        
        # Add relationships as directed edges.
        for rel in relationships:
            source_obj = rel.get("source", {})
            target_obj = rel.get("target", {})
            source = source_obj.get("id")
            target = target_obj.get("id")
            rel_type = rel.get("type", "")
            if source and target:
                if G.has_edge(source, target):
                    if "relation_types" in G[source][target]:
                        if rel_type not in G[source][target]["relation_types"]:
                            G[source][target]["relation_types"].append(rel_type)
                    else:
                        G[source][target]["relation_types"] = [rel_type]
                    G[source][target]["weight"] += 1
                else:
                    G.add_edge(source, target, weight=1, relation_types=[rel_type])
    
    # 5. Compute positions using a spring layout.
    pos = nx.spring_layout(G, k=1.2)
    #pos = nx.kamada_kawai_layout(G)
    
    # 6. Prepare node hover text.
    # For each node, list all outgoing and incoming connection details.
    node_hover = {}
    for node in G.nodes():
        outgoing = []
        for u, v, data in G.out_edges(node, data=True):
            rels = ", ".join(data.get("relation_types", []))
            outgoing.append(f"Out: {node} - {rels} -> {v}")
        incoming = []
        for u, v, data in G.in_edges(node, data=True):
            rels = ", ".join(data.get("relation_types", []))
            incoming.append(f"In: {u} - {rels} -> {node}")
        details = outgoing + incoming
        if details:
            node_hover[node] = "<br>".join(details)
        else:
            node_hover[node] = node  # Fallback if there are no connections.
    
    # 7. Create node trace using calculated positions and hover text.
    node_x = []
    node_y = []
    node_text = []         # Displayed text is just the node name.
    node_hover_list = []   # Custom hover info with connection details.
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        node_hover_list.append(node_hover.get(node, node))
        
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="top center",
        hoverinfo='text',
        hovertext=node_hover_list,
        marker=dict(
            size=10,
            color='#1f78b4'
        )
    )
    
    # 8. Create edge traces: one trace per edge.
    edge_traces = []
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace = go.Scatter(
            x=[x0, x1],
            y=[y0, y1],
            mode='lines',
            line=dict(width=1, color='#888'),
            hoverinfo='none'
        )
        edge_traces.append(edge_trace)
    
    # 9. Build the interactive Plotly figure.
    fig = go.Figure(
        data=edge_traces + [node_trace],
        layout=go.Layout(
            title='<br>Interactive Knowledge Graph (LLM-derived)',
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            width=1200,   # wider figure
            height=800,   # taller figure
            dragmode='pan'
        )
    )
    
    # 10. Re-add arrow annotations for each edge (without hover text).
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        fig.add_annotation(
            x=x1,
            y=y1,
            ax=x0,
            ay=y0,
            xref='x',
            yref='y',
            axref='x',
            ayref='y',
            showarrow=True,
            arrowhead=3,
            arrowcolor='#888',
            arrowwidth=2,
            text="",  # No text; rely on node hover for details.
        )
    
    return fig

def get_combined_feed(source_choice, selected_news_sites):
    """
    Create an aggregated feed from selected RSS sources
    and build an interactive Plotly knowledge graph.
    """
    feed_items = []
    
    # Fetch articles from selected news sites.
    if "News" in source_choice and selected_news_sites:
        selected_feeds = {name: url for name, url in RSS_FEEDS.items() if name in selected_news_sites}
        feed_items += fetch_articles(selected_feeds, limit=6)
    
    # Aggregate feed text.
    feed_text = "\n\n".join([f"🔹 {item['title']} ({item['published']})\n{item['link']}" for item in feed_items])
    
    # Build an interactive knowledge graph using Plotly.
    graph_fig = build_interactive_knowledge_graph(feed_items)
    
    return feed_text, graph_fig

# Define the Gradio interface with a button to trigger processing.
with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            source_selector = gr.CheckboxGroup(
                ["News"], value=["News"], label="Select Sources"
            )
            news_site_selector = gr.CheckboxGroup(
                list(RSS_FEEDS.keys()), value=["BBC", "Wired"], label="News Sites"
            )
        with gr.Column():
            feed_output = gr.Textbox(label="Aggregated Feed", lines=20)
    with gr.Row():
        with gr.Column():
            graph_output = gr.Plot(label="Interactive Knowledge Graph")
    
    # Button to trigger graph generation.
    generate_button = gr.Button("Generate Graph")
    generate_button.click(
        fn=get_combined_feed,
        inputs=[source_selector, news_site_selector],
        outputs=[feed_output, graph_output]
    )

demo.launch()
