# news/utils/visualizer.py
from pocketflow import Flow, Node, BatchNode
import requests
import base64
from io import BytesIO
from PIL import Image  # You'll need to pip install pillow

def build_mermaid(start):
    """
    Generate a Mermaid diagram for a PocketFlow graph.
    
    Args:
        start: The starting node or flow of the graph
        
    Returns:
        str: Mermaid syntax for the graph visualization
    """
    ids, visited, lines = {}, set(), ["graph LR"]
    ctr = 1
    
    def get_id(n):
        nonlocal ctr
        return ids[n] if n in ids else (ids.setdefault(n, f"N{ctr}"), (ctr := ctr + 1))[0]
    
    def link(a, b):
        lines.append(f"    {a} --> {b}")
    
    def walk(node, parent=None):
        if node in visited:
            if parent:  # Only link if parent exists
                return link(parent, get_id(node))
            return
        
        visited.add(node)
        if isinstance(node, Flow):
            #print(f"Node {node} has properties: {', '.join(dir(node))}")
            
            # Handle parent-start linking separately
            if node.start and parent:
                link(parent, get_id(node.start))
            
            lines.append(f"\n    subgraph sub_flow_{get_id(node)}[{type(node).__name__}]")
            
            # Simply call walk on start if it exists
            if node.start:
                walk(node.start)
                
            # Process successors with proper conditionals
            for nxt in node.successors.values():
                if node.start:
                    walk(nxt, get_id(node.start))
                elif parent:
                    link(parent, get_id(nxt))
                    walk(nxt)
                else:
                    walk(nxt)
                    
            lines.append("    end\n")
        else:
            nid = get_id(node)
            lines.append(f"    {nid}['{type(node).__name__}']")
            if parent:
                link(parent, nid)
            
            # Check if node has successors attribute before trying to access it
            if hasattr(node, 'successors'):
                for nxt in node.successors.values():
                    walk(nxt, nid)
    
    walk(start)
    return "\n".join(lines)

def save_as_image(flow, output_path="flow_diagram.png"):
    """
    Save a flow diagram as an image using the mermaid.ink service.
    
    Args:
        flow: The PocketFlow flow to visualize
        output_path: The output image file path
    """
    # Generate the Mermaid diagram
    diagram = build_mermaid(flow)
    
    # First save the Mermaid diagram to a file for reference
    with open("flow_diagram.mmd", "w") as f:
        f.write(diagram)
    
    print(f"Mermaid diagram saved to flow_diagram.mmd")
    
    # Encode the diagram for the mermaid.ink API
    encoded_diagram = base64.b64encode(diagram.encode('utf-8')).decode('utf-8')
    
    # Use the mermaid.ink service to generate the image
    image_url = f"https://mermaid.ink/img/{encoded_diagram}"
    
    # Download the image
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            # Save the image
            img = Image.open(BytesIO(response.content))
            img.save(output_path)
            print(f"Flow diagram image saved to {output_path}")
            return True
        else:
            print(f"Failed to download image: HTTP {response.status_code}")
            print("You can manually get the image by visiting:")
            print(image_url)
            return False
    except Exception as e:
        print(f"Error saving image: {e}")
        print("\nAlternatively, you can:")
        print(f"1. Visit https://mermaid.live/ and paste the diagram from flow_diagram.mmd")
        print("2. Use the 'Export' button to save as PNG, SVG, or PDF")
        return False