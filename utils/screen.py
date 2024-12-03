import display.config as config
from display.config import draw, width, height, disp, image

def blank_screen():
    """
    Blank the screen.
    """
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

def display_screen():
    """
    Display the screen.
    """
    disp.image(image)
    disp.show()