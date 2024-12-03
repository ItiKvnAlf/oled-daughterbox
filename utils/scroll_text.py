import threading
import time
import display.config as config
from utils.screen import display_screen
from display.config import draw, font

def scroll_text(state: str, index: int, text: str, max_width: int, x_pos: int, y_pos: int, delay: float):
    """
    Scrolls text horizontally if it exceeds the maximum display width.

    :param text: The text to display.
    :param max_width: The maximum allowed width (in pixels) of the display.
    :param x_pos: The horizontal position on the screen to draw the text
    :param y_pos: The vertical position on the screen to draw the text.
    :param delay: The delay (in seconds) between each scroll step.
    """
    text_width = draw.textlength(text)

    if text_width <= max_width:
        # If the text fits within the screen width, draw it directly.
        draw.text((x_pos, y_pos), text, font=font, fill=255)
        display_screen()
    else:
        # Scroll the text horizontally if it exceeds the screen width.
        scroll_position = 0
        text = text + ((" ") * len(text))
        while state == config.data['current_state'] and index == config.data['current_index']:  # Infinite loop for continuous scrolling

            # Create the scrolling text by cycling characters.
            display_text = text[scroll_position:] + text[:scroll_position]
            
            # Clear the text area before drawing the next frame.
            draw.rectangle((x_pos, y_pos, x_pos + max_width, y_pos + 10), outline=0, fill=0)
            draw.text((x_pos, y_pos), display_text[:len(text)], font=font, fill=255)

            # Update the scroll position.
            scroll_position += 1
            if scroll_position > len(text) + (max_width // font.getlength(' ')):  # Wait until the entire text is off the screen
                scroll_position = 0

            display_screen()
            # Pause before the next update.
            time.sleep(delay)

def start_scrolling_text(state: str, index: int, text: str, max_width: int, x_pos: int, y_pos: int, delay: float = 0.15):
    scroll_thread = threading.Thread(target=scroll_text, args=(state, index, text, max_width, x_pos, y_pos, delay))
    scroll_thread.daemon = True  # This makes the thread exit when the main program exits
    scroll_thread.start()