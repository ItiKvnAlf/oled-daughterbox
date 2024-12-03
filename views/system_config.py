from display.icons import set_icon_center
from network.ip import format_ip_address, validate_ip_digit_list
import display.config as config
from utils.center_text import center_text
from display.config import draw, width, font

def system_config_view(options: list):
    """
    Display the system configuration view.

    Args:
        options (list): List of options to display.
    """
    num_options = len(options)

    # Check if selected_digit_index is within bounds
    if config.data['selected_digit_index'] < num_options:
        selected_option = options[config.data['selected_button']]
    else:
        selected_option = options[0]  # Default to the first option

    # Draw icons and selected option text
    if config.data['selected_digit_index'] == 0:
        set_icon_center('right')  # Draw right icon for active selection

        # Draw the selected option only
        option_text = selected_option

        # Draw selected option with a white background and black text
        width_option = (width // 2 - draw.textlength(option_text)) // 2
        draw.rectangle((width_option - 2, 10, width_option + draw.textlength(option_text), 20), fill=255)
        draw.text((width_option, 10), option_text, font=font, fill=0)

        # Draw "BACK" button
        text4 = "BACK"
        width4 = (width - draw.textlength(text4) - 10)
        draw.text((width4, 10), text4, font=font, fill=255)

        # Draw up and down icons for navigation
        set_icon_center('up')
        set_icon_center('down')

    else:
        # If the first button is not selected, draw all buttons with transparent background
        set_icon_center('left')

        # Transparent background for all options when none are selected
        option_text = selected_option

        # Draw selected option with a white background and black text
        width_option = (width // 2 - draw.textlength(option_text)) // 2
        draw.text((width_option, 10), option_text, font=font, fill=255)

        # "BACK" remains in the same position
        text4 = "BACK"
        width4 = (width - draw.textlength(text4) - 10)
        draw.rectangle((width4 - 2, 10, width4 + draw.textlength(text4), 20), fill=255)
        draw.text((width4, 10), text4, font=font, fill=0)

def system_info_ip_view():
    """
    Display the system information IP view.
    """
    text1 = "DB IP (ETHERNET)"
    text2 = f"{config.data['db']['ip']}"
    draw.text((center_text(text1), 0), text1, font=font, fill=255)
    draw.text((center_text(text2), 10), text2, font=font, fill=255)
    if config.data['selected_digit_index'] == 0:
        draw.rectangle(((width - draw.textlength("CANCEL")) // 4 - 2, 22, draw.textlength("CANCEL") + 22, 31), fill=255)
        draw.text(((width - draw.textlength("CANCEL")) // 4, 21), "CANCEL", font=font, fill=0)
        draw.text((center_text("CHANGE") + ((width - draw.textlength("CHANGE")) // 4), 21), "CHANGE", font=font, fill=255)
    else:
        width1 = center_text("CHANGE") + (width - draw.textlength("CHANGE")) // 4
        draw.rectangle((width1 - 2, 22, width1 + draw.textlength("CHANGE") - 1, 31), fill=255)
        draw.text(((width - draw.textlength("CANCEL")) // 4, 21), "CANCEL", font=font, fill=255)
        draw.text((width1, 21), "CHANGE", font=font, fill=0)

def system_change_ip_view(x_start=0, y_start=0, digit_spacing=6):
    """
    Display the system change IP view.
    Args:
        x_start (int): The starting X position for the screen.
        y_start (int): The starting Y position for the screen.
        digit_spacing (int): The spacing between each digit.
    """
    x_position, y_position = x_start, y_start

    # Validate the digit list based on IP rules before displaying
    validate_ip_digit_list()

    for i in range(4):  # Loop through the four octets
        # Get the current octet's three digits
        for j in range(3):
            digit_index = i * 3 + j
            digit = config.data['temp_ip'][digit_index]
            
            # Check if the current digit is the selected one
            if digit_index == config.data['selected_digit_index']:
                # Position arrows for selected digit
                base_x = x_position
                up_icon = [(base_x + 2, y_position + 4), (base_x, y_position + 8), (base_x + 4, y_position + 8)]
                down_icon = [(base_x + 2, y_position + 26), (base_x, y_position + 22), (base_x + 4, y_position + 22)]
                
                draw.polygon(up_icon, fill=255)  # Up arrow
                draw.text((x_position, y_position + 10), str(digit), font=font, fill=255)  # Draw selected digit
                draw.polygon(down_icon, fill=255)  # Down arrow
            else:
                draw.text((x_position, y_position + 10), str(digit), font=font, fill=255)  # Draw digit normally
            
            x_position += digit_spacing  # Move to the next position

        # Draw '.' except after the last octet
        if i < 3:
            draw.text((x_position, y_position + 10), ".", font=font, fill=255)
            x_position += digit_spacing

    # Draw "BACK" and "NEXT" buttons at the end of the IP address
    button_x, button_y = x_position + 10, y_position + 5

    # Draw and position the buttons with arrow indicators as before
    if config.data['selected_digit_index'] == 12 and config.data['selected_button'] == 0:
        draw.rectangle((button_x - 2, button_y + 2, button_x + 24, button_y + 10), fill=255)
        draw.text((button_x, button_y), "BACK", font=font, fill=0)
    else:
        draw.text((button_x, button_y), "BACK", font=font, fill=255)
    
    if config.data['selected_digit_index'] == 12 and config.data['selected_button'] == 1:
        draw.rectangle((button_x - 2, button_y + 12, button_x + 24, button_y + 19), fill=255)
        draw.text((button_x, button_y + 10), "NEXT", font=font, fill=0)
    else:
        draw.text((button_x, button_y + 10), "NEXT", font=font, fill=255)

    if config.data['selected_digit_index'] == 12:
        up_icon_buttons = [(button_x + 11, button_y - 3), (button_x + 9, button_y - 1), (button_x + 13, button_y - 1)]
        down_icon_buttons = [(button_x + 11, button_y + 24), (button_x + 9, button_y + 22), (button_x + 13, button_y + 22)]
        
        draw.polygon(up_icon_buttons, fill=255)  # Up arrow
        draw.polygon(down_icon_buttons, fill=255)  # Down arrow

def system_change_mask_view(x_start=0, y_start=0):
    """
    Display the system change mask view.
    Args:
        x_start (int): The starting X position for the screen.
        y_start (int): The starting Y position for the screen.
    """
    base_x = x_start + 70
    if config.data['temp_netmask'] > 9:
        base_x += 3
    up_icon = [(base_x + 2, y_start + 4), (base_x, y_start + 8), (base_x + 4, y_start + 8)]
    down_icon = [(base_x + 2, y_start + 26), (base_x, y_start + 22), (base_x + 4, y_start + 22)]
    
    if config.data['selected_digit_index'] == 0:
        draw.polygon(up_icon, fill=255)  # Up arrow
        draw.text((x_start + 10, y_start + 10), "NETMASK: /" + str(config.data['temp_netmask']), font=font, fill=255)  # Draw selected digit
        draw.polygon(down_icon, fill=255)  # Down arrow
    else:
        draw.text((x_start + 10, y_start + 10), "NETMASK: /" + str(config.data['temp_netmask']), font=font, fill=255)

    # Draw "BACK" and "SAVE" buttons at the end of the IP address
    button_x, button_y = x_start + 100, y_start + 5

    # Draw and position the buttons with arrow indicators as before
    if config.data['selected_digit_index'] == 1 and config.data['selected_button'] == 0:
        draw.rectangle((button_x - 2, button_y + 2, button_x + 24, button_y + 10), fill=255)
        draw.text((button_x, button_y), "BACK", font=font, fill=0)
    else:
        draw.text((button_x, button_y), "BACK", font=font, fill=255)

    if config.data['selected_digit_index'] == 1 and config.data['selected_button'] == 1:
        draw.rectangle((button_x - 2, button_y + 12, button_x + 24, button_y + 19), fill=255)
        draw.text((button_x, button_y + 10), "SAVE", font=font, fill=0)
    else:
        draw.text((button_x, button_y + 10), "SAVE", font=font, fill=255)

    if config.data['selected_digit_index'] == 1:
        up_icon_buttons = [(button_x + 11, button_y - 3), (button_x + 9, button_y - 1), (button_x + 13, button_y - 1)]
        down_icon_buttons = [(button_x + 11, button_y + 24), (button_x + 9, button_y + 22), (button_x + 13, button_y + 22)]
        
        draw.polygon(up_icon_buttons, fill=255)
        draw.polygon(down_icon_buttons, fill=255)

def confirm_system_change_ip_view():
    """
    Display the confirm system change IP view.
    """
    ip_text = f"({format_ip_address(config.data['temp_ip'])}/{config.data['temp_netmask']})"
    text1 = "Confirm changes?"
    text2 = ip_text
    draw.text((center_text(text1), 0), text1, font=font, fill=255)
    draw.text((center_text(text2), 10), text2, font=font, fill=255)

def confirm_system_reboot_view():
    """
    Display the confirm system reboot view.
    """
    text1 = "REBOOT this device?"
    draw.text((center_text(text1), 5), text1, font=font, fill=255)

def confirm_system_shutdown_view():
    """
    Display the confirm system shutdown view.
    """
    text1 = "Confirm SHUTDOWN?"
    draw.text((center_text(text1), 5), text1, font=font, fill=255)

def system_change_mode_view():
    """
    Display the confirm system change mode view.
    """
    text1 = "Change MODE to"
    text2 = "MOTHER BOX?"
    draw.text((center_text(text1), 0), text1, font=font, fill=255)
    draw.text((center_text(text2), 10), text2, font=font, fill=255)

def confirm_system_change_mode_view():
    """
    Display the confirm system change mode view.
    """
    text1 = "The system will"
    text2 = "REBOOT. Proceed?"
    draw.text((center_text(text1), 0), text1, font=font, fill=255)
    draw.text((center_text(text2), 10), text2, font=font, fill=255)

def same_ip_view():
    text1 = "Same IP address"
    text2 = "entered"
    text3 = "Push to go back"
    draw.text((center_text(text1), 0), text1, font=font, fill=255)
    draw.text((center_text(text2), 10), text2, font=font, fill=255)
    draw.text((center_text(text3), 20), text3, font=font, fill=255)

def ip_applied_view():
    text1 = "IP address"
    text2 = "applied"
    text3 = "Push to continue"
    draw.text((center_text(text1), 0), text1, font=font, fill=255)
    draw.text((center_text(text2), 10), text2, font=font, fill=255)
    draw.text((center_text(text3), 20), text3, font=font, fill=255)