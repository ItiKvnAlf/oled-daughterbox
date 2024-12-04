import display.config as config
from display.menu import display_current_menu
from utils.get_linked_mh import get_linked_mh

def navigate_right():
    """Navigate right in the menu."""

    # Get the current state and other necessary data
    current_state = config.data['current_state']
    selected_digit_index = config.data['selected_digit_index']
    selected_confirm_button = config.data['selected_confirm_button']
    current_index = config.data['current_index']
    networks = config.data['networks']
    
    # Check the current state and update the system accordingly
    if current_state == "menu":
        config.data['current_state'] = "info_db"
    elif current_state == "config":
        if selected_digit_index == 0:
            config.data['selected_digit_index'] = 1
    elif current_state == "system_change_ip":
        if selected_digit_index == 0:
            config.data['selected_digit_index'] = 1
    elif current_state == "system_reboot" or current_state == "system_shutdown" or current_state == "system_change_mode" or current_state == "confirm_change_mode":
        if selected_confirm_button == 0:
            config.data['selected_confirm_button'] += 1
    elif current_state == "info_db":
        config.data['mh'] = get_linked_mh()
        config.data['current_state'] = "info_mh"
    elif current_state == "networks_detected":
        config.data['current_index'] = (current_index + 1) % len(networks)
    elif current_state == "config_network":
        if selected_digit_index == 0:
            config.data['selected_digit_index'] = 1
    elif current_state == "change_ip":
        if selected_digit_index == 12:
            config.data['selected_digit_index'] = 0
        elif selected_digit_index < 12:
            config.data['selected_digit_index'] += 1
    elif current_state == "netmask":
        if selected_digit_index == 1:
            config.data['selected_digit_index'] = 0
        elif selected_digit_index < 1:
            config.data['selected_digit_index'] += 1
    elif current_state == "confirm_ip" or current_state == "confirm_unlinking" or current_state == "confirm_known_link" or current_state == "confirm_known_unlink" or current_state == "confirm_autolink" or current_state == "confirm_delete":
        if selected_confirm_button == 0:
            config.data['selected_confirm_button'] += 1
        else:
            config.data['selected_confirm_button'] -= 1
    elif current_state == "link_mh":
        if selected_digit_index == 8:
            config.data['selected_digit_index'] = 0
        elif selected_digit_index < 8:
            config.data['selected_digit_index'] += 1
    display_current_menu()