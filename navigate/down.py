import display.config as config
from display.menu import display_current_menu

def navigate_down():
    """Navigate down in the menu."""
    current_state = config.data['current_state']
    selected_digit_index = config.data['selected_digit_index']
    selected_button = config.data['selected_button']
    temp_ip = config.data['temp_ip']
    temp_netmask = config.data['temp_netmask']
    temp_password = config.data['temp_password']
    networks = config.data['networks']
    
    if current_state == "menu":
        if len(networks) > 0:
            config.data['current_state'] = "networks_info"
        else:
            config.data['current_state'] = "no_networks"
    elif current_state == "info_mh":
        config.data['current_state'] = "info_db_wlan_ip"
    elif current_state == "config":
        if selected_digit_index == 0:
            if selected_button < len(config.data['system_config_options']) - 1:
                config.data['selected_button'] += 1
            else:
                config.data['selected_button'] = 0
    elif current_state == "networks_info":
        config.data['current_index'] = 0
        config.data['current_state'] = "networks_detected"
    elif current_state == "config_network":
        if selected_digit_index == 0 and selected_button < 2:
            config.data['selected_button'] += 1
    elif current_state == "config":
        config.data['current_state'] = "menu"
    elif current_state == "change_ip":
        if selected_digit_index == 12 and selected_button == 0:
            config.data['selected_button'] += 1
        elif selected_digit_index < 12:
            octet_index = selected_digit_index // 3  # Determine which octet the selected digit belongs to
            digit_in_octet = selected_digit_index % 3  # Position within the octet

            # Only allow valid IP configurations
            if digit_in_octet == 0:  # First digit in the octet
                if temp_ip[selected_digit_index] > 0:
                    config.data['temp_ip'][selected_digit_index] -= 1
                else:
                    config.data['temp_ip'][selected_digit_index] = 2  # Reset to 2 if it goes below 0
            elif digit_in_octet == 1:  # Second digit in the octet
                # If the first digit is 2, limit this digit to 5
                if temp_ip[octet_index * 3] == 2 and temp_ip[selected_digit_index] == 0:
                    config.data['temp_ip'][selected_digit_index] = 5
                else:
                    config.data['temp_ip'][selected_digit_index] -= 1
                    if temp_ip[selected_digit_index] < 0:
                        config.data['temp_ip'][selected_digit_index] = 9
            elif digit_in_octet == 2:  # Third digit in the octet
                # If the first two digits form a number starting with "25", limit this digit to 5
                if temp_ip[octet_index * 3] == 2 and temp_ip[octet_index * 3 + 1] == 5 and temp_ip[selected_digit_index] == 0:
                    config.data['temp_ip'][selected_digit_index] = 5
                else:
                    config.data['temp_ip'][selected_digit_index] -= 1
                    if temp_ip[selected_digit_index] < 0:
                        config.data['temp_ip'][selected_digit_index] = 9
    elif current_state == "netmask":
        if selected_digit_index == 1 and selected_button == 0:
            config.data['selected_button'] += 1
        elif selected_digit_index == 0:
            if temp_netmask > 0:
                config.data['temp_netmask'] -= 1
            else:
                config.data['temp_netmask'] = 32
    elif current_state == "link_mh":
        if selected_digit_index == 8 and selected_button == 0:
            config.data['selected_button'] += 1
        elif selected_digit_index < 8:
            config.data['temp_password'][selected_digit_index] -= 1
            if temp_password[selected_digit_index] < 0:
                config.data['temp_password'][selected_digit_index] = 9
    display_current_menu()