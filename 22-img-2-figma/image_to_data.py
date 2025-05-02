"""
Module for parsing whiteboard images into structured elements.
"""
from typing import List, Dict, Any

def parse_whiteboard(image_path: str) -> List[Dict[str, Any]]:
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
    # Perform local OCR to detect text regions as 'sticky' elements
    try:
        import cv2
        import pytesseract
    except ImportError:
        raise RuntimeError(
            "Local OCR parsing requires 'opencv-python' and 'pytesseract'. "
            "Install via: pip install opencv-python pytesseract"
        )
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        raise RuntimeError(f"Failed to load image '{image_path}'")
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Run OCR to get bounding boxes and text
    ocr_data = pytesseract.image_to_data(
        gray, output_type=pytesseract.Output.DICT
    )
    elements: List[Dict[str, Any]] = []
    n_boxes = len(ocr_data.get('text', []))
    for i in range(n_boxes):
        text = ocr_data['text'][i].strip()
        conf = ocr_data.get('conf', [])[i]
        try:
            conf_val = int(conf)
        except Exception:
            conf_val = -1
        # Filter out low-confidence or empty results
        if text and conf_val > 60:
            x = int(ocr_data['left'][i])
            y = int(ocr_data['top'][i])
            elements.append({
                'type': 'sticky',
                'text': text,
                'x': x,
                'y': y,
            })
    return elements