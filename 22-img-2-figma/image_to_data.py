"""
Module for parsing whiteboard images into structured elements.
"""
from typing import List, Dict

def parse_whiteboard(image_path: str) -> List[Dict]:
    """
    Parse a whiteboard image and return a list of elements describing
    stickies and connectors. Each element is a dict with a 'type' key.

    Example output:
        [
            { 'type': 'sticky', 'text': 'Idea', 'x': 100, 'y': 200 },
            { 'type': 'sticky', 'text': 'Next', 'x': 300, 'y': 200 },
            { 'type': 'connector', 'start_id': '0', 'end_id': '1' }
        ]

    Args:
        image_path: Path to the whiteboard image file.

    Returns:
        A list of element dicts.
    """
    # TODO: implement image processing (e.g., OCR, layout analysis)
    # For now, return an empty list.
    return []