<!-- 25-designer: Multi-agent system for design language generation -->
# Design Language Multi-Agent System

This multi-agent system that defines and generates a coherent design language (color schemes, typography, and a design system webpage) based a project description and target user.

## Architecture
A manager agent orchestrates several specialized sub-agents:
1. **user_researcher**: Gathers insights on target audience needs
2. **trend_researcher**: Identifies modern design trends and inspirations
3. **best_practices_bot**: Reviews accessibility, contrast, and usability guidelines
4. **visual_designer**: Proposes color palettes and typography options, then renders an HTML design system page
5. **final_presentation_creator**: Assembles and writes the final HTML output to disk

Under the hood, each sub-agent is a `CodeAgent` (from smolagents) with its own tools and prompts. The manager coordinates them in a pipeline to refine the design direction and produce the final deliverable.

## Tools Provided
- **select_color_scheme**: Normalizes a JSON or comma-separated color list into a palette structure
- **pick_font**: Generates a Google Fonts `@import` rule for any specified font name
- **generate_design_webpage**: Builds an HTML page visualizing the chosen colors and typography
- **create_file**: Writes text or HTML content into a file on disk

## Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the agent:
   ```bash
   python main.py
   ```
3. When prompted, enter a project brief. For example:
   ```text
   create 3 possible design language directions for a flower delivery company with a focus on millennials
   ```
4. The manager agent will coordinate research, trend analysis, and visual design. Resulting HTML file(s) will be saved via the `create_file` tool (check your working directory for output files).

## Example Session
```
Enter project description (or 'exit' to quit): create a bold, playful branding direction for a mobile gaming app targeting Gen Z
Starting design workflow...
... (agents collaborating) ...
File created at designs/branding_direction_1.html
File created at designs/branding_direction_2.html
File created at designs/branding_direction_3.html
```

## Extending the System
- Add or refine tools in `main.py` by decorating new functions with `@tool`
- Adjust agent prompts, descriptions, or add new sub-agents to customize the workflow

Leverage this framework to rapidly prototype and validate design directions in code-driven, agent-assisted workflows.