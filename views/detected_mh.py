import display.config as config
from utils.center_text import center_text
from display.config import draw, font

def link_detected_mh_view(x_start=36, y_start=0, digit_spacing=6):
    """
    Display the link to detected MOTHER HUB screen.

    Args:
        x_start (int): The starting X position for the screen.
        y_start (int): The starting Y position for the screen.
        digit_spacing (int): The spacing between each digit.
    """
    x_position, y_position = x_start, y_start

    draw.text((2, 10), f"PASS:", font=font, fill=255)

    for i in range(8):  # Loop through the eight digits of the password
        # Get the current digit{
        digit = config.data['temp_password'][i]

        if i == config.data['selected_digit_index']:
            # Position arrows for selected digit
            base_x = x_position
            up_icon = [(base_x + 2, y_position + 4), (base_x, y_position + 8), (base_x + 4, y_position + 8)]
            down_icon = [(base_x + 2, y_position + 26), (base_x, y_position + 22), (base_x + 4, y_position + 22)]
            
            draw.polygon(up_icon, fill=255)
            draw.text((x_position, y_position + 10), str(digit), font=font, fill=255)
            draw.polygon(down_icon, fill=255)
        else:
            draw.text((x_position, y_position + 10), str(digit), font=font, fill=255)
        
        x_position += digit_spacing

    # Draw "BACK" and "NEXT" buttons at the end of the IP address
    button_x, button_y = x_position + 16, y_position + 5

    # Draw and position the buttons with arrow indicators as before
    if config.data['selected_digit_index'] == 8 and config.data['selected_button'] == 0:
        draw.rectangle((button_x - 5, button_y + 2, button_x + 23, button_y + 9), fill=255)
        draw.text((button_x - 4, button_y), "BACK", font=font, fill=0)
    else:
        draw.text((button_x - 4, button_y), "BACK", font=font, fill=255)
    
    if config.data['selected_digit_index'] == 8 and config.data['selected_button'] == 1:
        draw.rectangle((button_x - 5, button_y + 12, button_x + 23, button_y + 19), fill=255)
        draw.text((button_x - 3, button_y + 10), "NEXT", font=font, fill=0)
    else:
        draw.text((button_x - 3, button_y + 10), "NEXT", font=font, fill=255)

    if config.data['selected_digit_index'] == 8:
        up_icon_buttons = [(button_x + 9, button_y - 3), (button_x + 7, button_y - 1), (button_x + 11, button_y - 1)]
        down_icon_buttons = [(button_x + 9, button_y + 24), (button_x + 7, button_y + 22), (button_x + 11, button_y + 22)]
        
        draw.polygon(up_icon_buttons, fill=255)  # Up arrow
        draw.polygon(down_icon_buttons, fill=255)  # Down arrow

def success_link_detected_mh_view():
    """Display the success link detected MOTHER HUB screen."""
    text1 = "LINKED to"
    text2 = config.data['selected_hub']["ssid"]
    text3 = "Push to continue"
    draw.text((center_text(text1), 0), text1, font=font, fill=255)
    draw.text((center_text(text2), 10), text2, font=font, fill=255)
    draw.text((center_text(text3), 20), text3, font=font, fill=255)

def failure_link_detected_mh_view():
    """Display the failure link detected MOTHER HUB screen."""
    text1 = "Failed to LINK"
    text2 = "Push to retry"
    draw.text((center_text(text1), 0), text1, font=font, fill=255)
    draw.text((center_text(text2), 10), text2, font=font, fill=255)

def incorrect_password_view():
    """Display the incorrect password screen."""
    text1 = "Incorrect password"
    text2 = "Push to retry"
    draw.text((center_text(text1), 5), text1, font=font, fill=255)
    draw.text((center_text(text2), 15), text2, font=font, fill=255)

def no_router_view():
    """Display the no router screen."""
    text1 = "No router connected"
    text2 = "to the MOTHER HUB"
    text3 = "Push to retry"
    draw.text((center_text(text1), 0), text1, font=font, fill=255)
    draw.text((center_text(text2), 10), text2, font=font, fill=255)
    draw.text((center_text(text3), 20), text3, font=font, fill=255)

