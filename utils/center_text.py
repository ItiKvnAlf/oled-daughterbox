import display.config as config
from display.config import draw, width

def center_text(text: str):
    """
    Center text on the display.
    Args:
        text (str): The text to center.
    """
    return (width - draw.textlength(text)) // 2
