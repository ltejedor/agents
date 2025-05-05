import os
import random
import json
from smolagents import CodeAgent, tool, LiteLLMModel

@tool
def create_file(path: str, content: str) -> str:
    """
    Creates a file at the specified path with the given content.

    Args:
        path: The filesystem path where the file will be created.
        content: The text content to write into the file.

    Returns:
        A message indicating success or describing the error.
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"File created at {path}"
    except Exception as e:
        return f"Error creating file: {e}"

@tool
def select_color_scheme(palette_input: str) -> str:
    """
    Accepts a JSON string or comma-separated list of color values provided by the agent.
    Returns a standardized JSON color palette.

    Args:
        palette_input: A JSON string representing a color palette or a comma-separated list of hex color codes.

    Returns:
        A JSON string of the standardized palette (list or dict of colors).
    """
    try:
        palette = json.loads(palette_input)
        return json.dumps(palette)
    except json.JSONDecodeError:
        colors = [c.strip() for c in palette_input.split(',') if c.strip()]
        return json.dumps({"colors": colors})

@tool
def pick_font(font_name: str) -> str:
    """
    Generates a CSS import statement for the specified font name.
    Returns a JSON string with keys: title and css_import.

    Args:
        font_name: The name of the Google Font to import (e.g., 'Roboto').

    Returns:
        A JSON string containing the font title and the CSS @import rule.
    """
    try:
        import urllib.parse
        family = urllib.parse.quote_plus(font_name)
        css = f"@import url('https://fonts.googleapis.com/css2?family={family}:wght@400;700&display=swap');"
        return json.dumps({"title": font_name, "css_import": css})
    except Exception:
        return json.dumps({"title": font_name, "css_import": ""})

@tool
def pick_header_font(font_name: str) -> str:
    """
    Picks a header font based on the provided font name.

    Args:
        font_name: The Google Font name for headings (e.g., 'Roboto').

    Returns:
        A JSON string containing the font title and CSS @import rule.
    """
    return pick_font(font_name)

@tool
def pick_body_font(font_name: str) -> str:
    """
    Picks a body font based on the provided font name.

    Args:
        font_name: The Google Font name for body text (e.g., 'Open Sans').

    Returns:
        A JSON string containing the font title and CSS @import rule.
    """
    return pick_font(font_name)

@tool
def generate_design_webpage(color_scheme_json: str, header_font_json: str, body_font_json: str) -> str:
    """
    Generates an HTML page showcasing the design system with sample elements.

    Args:
        color_scheme_json: JSON string containing color variables (primary, secondary, accent).
        header_font_json: JSON string with header font title and CSS import rule.
        body_font_json: JSON string with body font title and CSS import rule.

    Returns:
        A string of the complete HTML page to display the design system.
    """
    cs = json.loads(color_scheme_json)
    hf = json.loads(header_font_json)
    bf = json.loads(body_font_json)
    # support both 'css_import' and 'import' keys
    hf_import = hf.get('css_import') or hf.get('import') or ''
    bf_import = bf.get('css_import') or bf.get('import') or ''
    hf_family = hf.get('title', '')
    bf_family = bf.get('title', '')
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Design System Overview</title>
  <style>
    {hf_import}
    {bf_import}
    :root {{
      --color-primary: {cs['primary']};
      --color-secondary: {cs['secondary']};
      --color-accent: {cs['accent']};
    }}
    h1, h2, h3, h4, h5, h6 {{
      font-family: '{hf_family}', sans-serif;
      margin: 0.5em 0;
    }}
    body, p, button {{
      font-family: '{bf_family}', sans-serif;
      background-color: var(--color-secondary);
      color: #333;
      padding: 1rem;
    }}
    .swatch {{
      width: 80px; height: 80px;
      display: inline-block; margin: 0.5rem;
      border-radius: 4px;
    }}
    button {{
      padding: 0.5rem 1rem;
      background-color: var(--color-primary);
      border: none; color: #fff;
      border-radius: 4px; cursor: pointer;
    }}
    button:hover {{ background-color: var(--color-accent); }}
  </style>
</head>
<body>
  <h1>Heading Level 1</h1>
  <h2>Heading Level 2</h2>
  <h3>Heading Level 3</h3>
  <section>
    <h2>Color Palette</h2>
    <div class="swatch" style="background-color: var(--color-primary);"></div>
    <div class="swatch" style="background-color: var(--color-secondary);"></div>
    <div class="swatch" style="background-color: var(--color-accent);"></div>
  </section>
  <section>
    <h2>Typography & Buttons</h2>
    <p>The quick brown fox jumps over the lazy dog.</p>
    <button>Example Button</button>
  </section>
</body>
</html>
"""
    return html

def main():
    model = LiteLLMModel(model_id="anthropic/claude-3-7-sonnet-latest")

    visual_designer = CodeAgent(
        model=model,
        tools=[select_color_scheme, pick_font, generate_design_webpage, create_file],
        name="visual_designer",
        description="Design language specialist who selects color schemes, typography, and generates design system webpage",
        add_base_tools=True,
        additional_authorized_imports=["json"]
    )

    best_practices_bot = CodeAgent(
        model=model,
        tools=[],
        name="best_practices_bot",
        description="Expert in design best practices ensuring accessibility and usability of design choices",
        add_base_tools=True
    )

    user_researcher = CodeAgent(
        model=model,
        tools=[],
        name="user_researcher",
        description="Conducts user research to inform design decisions based on target audience needs",
        add_base_tools=True
    )

    trend_researcher = CodeAgent(
        model=model,
        tools=[],
        name="trend_researcher",
        description="Researches current design trends to suggest modern and relevant visual styles",
        add_base_tools=True
    )

    final_presentation_creator = CodeAgent(
        model=model,
        tools=[generate_design_webpage, create_file],
        name="final_presentation_creator",
        description="Compiles and finalizes the design system into a presentation-ready HTML page",
        add_base_tools=True,
        additional_authorized_imports=["os", "posixpath", "json"]
    )

    manager_agent = CodeAgent(
        model=model,
        tools=[create_file],
        add_base_tools=True,
        additional_authorized_imports=["time", "json"],
        managed_agents=[user_researcher, trend_researcher, best_practices_bot, visual_designer, final_presentation_creator],
        max_steps=100
    )

    while True:
        project_desc = input("Enter project description (or 'exit' to quit): ")
        if project_desc.lower() in ("exit", "quit"):
            break
        print("Starting design workflow...")
        result = manager_agent.run(project_desc)
        print(result)

if __name__ == "__main__":
    main()
