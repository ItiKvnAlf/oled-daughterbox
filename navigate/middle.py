import display.config as config
from display.menu import display_current_menu
from network.ip import apply_ip, calculate_netmask_prefix, format_ip_address, get_mask
from system.constants import ETHERNET_CONNECTION
from utils.get_ip import get_ip_address
from network.actions import autolink_known_network, delete_known_network, link_known_network, unlink_from_hub, unlink_known_network
from network.autoconnect import check_autoconnect
from network.mother import link_to_detected_mh
from utils.refresh import refresh_networks
from system.actions import change_mode, reboot_system, shutdown_system

def push_button():
    """Handle button press."""

    # Get the current state and other necessary data
    current_state = config.data['current_state']
    selected_button = config.data['selected_button']
    selected_confirm_button = config.data['selected_confirm_button']
    selected_digit_index = config.data['selected_digit_index']
    current_index = config.data['current_index']
    networks = config.data['networks']
    temp_ip = config.data['temp_ip']
    temp_netmask = config.data['temp_netmask']
    
    # Check the current state and update the system accordingly
    if current_state == "menu":
        config.data['selected_digit_index'] = 0
        config.data['current_state'] = "config"
    elif current_state == "config":
        if selected_digit_index == 0:
            if selected_button == 0:
                config.data['current_state'] = "system_change_ip"
            elif selected_button == 1:
                config.data['current_state'] = "system_reboot"
            elif selected_button == 2:  
                config.data['current_state'] = "system_shutdown"
            elif selected_button == 3:
                config.data['current_state'] = "system_change_mode"
        elif selected_digit_index == 1:
            config.data['current_state'] = "menu"
        config.data['selected_button'] = 0
        config.data['selected_digit_index'] = 0
    elif current_state == "system_change_ip":
        if selected_digit_index == 1:
            config.data['current_state'] = "change_ip"
            config.data['temp_ip'] = [int(digit) for digit in "".join(part.zfill(3) for part in get_ip_address(ETHERNET_CONNECTION).split('.'))]
            config.data['selected_digit_index'] = 0
        elif selected_digit_index == 0:
            config.data['current_state'] = "config"
            config.data['selected_digit_index'] = 0
    elif current_state == "system_reboot":
        if selected_confirm_button == 1:
            reboot_system()
        elif selected_confirm_button == 0:
            config.data['current_state'] = "config"
            config.data['selected_button'] = 1
    elif current_state == "system_shutdown":
        if selected_confirm_button == 1:
            shutdown_system()   
        elif selected_confirm_button == 0:
            config.data['current_state'] = "config"
            config.data['selected_button'] = 2
    elif current_state == "system_change_mode":
        if selected_confirm_button == 1:
            config.data['current_state'] = "confirm_change_mode"
            config.data['selected_confirm_button'] = 0
        elif selected_confirm_button == 0:
            config.data['current_state'] = "config"
            config.data['selected_button'] = 3
    elif current_state == "confirm_change_mode":
        if selected_confirm_button == 1:
            change_mode()
        elif selected_confirm_button == 0:
            config.data['selected_confirm_button'] = 0
            config.data['current_state'] = "system_change_mode"
    elif current_state == "info_mh":
        ssid = config.data['mh'].get('ssid', None)
        rssi = config.data['mh'].get('rssi', None)

        if ssid is not None and rssi is not None:
            config.data['current_state'] = "confirm_unlinking"
        else:
            if len(networks) > 0:
                config.data['current_state'] = "networks_info"
            else:
                config.data['current_state'] = "no_networks"
    elif current_state == "change_ip":
        if selected_digit_index == 12 and selected_button == 0:
            config.data['current_state'] = "system_change_ip"
            config.data['selected_digit_index'] = 0
            config.data['temp_ip'] = [int(digit) for digit in "".join(part.zfill(3) for part in get_ip_address(ETHERNET_CONNECTION).split('.'))]
        elif selected_digit_index == 12 and selected_button == 1:
            config.data['current_state'] = "netmask"
            config.data['temp_netmask'] = calculate_netmask_prefix()
            config.data['selected_digit_index'] = 0
            config.data['selected_button'] = 0
    elif current_state == "netmask":
        current_ip = get_ip_address(ETHERNET_CONNECTION)
        current_mask = get_mask(ETHERNET_CONNECTION)
        if selected_digit_index == 1 and selected_button == 0:
            config.data['current_state'] = "change_ip"
            config.data['selected_digit_index'] = 0
        elif selected_digit_index == 1 and selected_button == 1:
            if temp_ip == [int(digit) for digit in "".join(part.zfill(3) for part in current_ip.split('.'))] and temp_netmask == current_mask:
                config.data['current_state'] = "same_ip"
            else:
                config.data['current_state'] = "confirm_ip"
            config.data['selected_digit_index'] = 0
            config.data['selected_button'] = 0
    elif current_state == "same_ip":
        config.data['current_state'] = "system_change_ip"
    elif current_state == "ip_applied":
        config.data['current_state'] = "menu"
    elif current_state == "confirm_ip":
        if selected_confirm_button == 0:
            config.data['selected_button'] = 0
            config.data['temp_ip'] = [int(digit) for digit in "".join(part.zfill(3) for part in get_ip_address(ETHERNET_CONNECTION).split('.'))]
            config.data['current_state'] = "change_ip"
        elif selected_confirm_button == 1:
            # Format the IP address and subnet mask
            connection_name = ETHERNET_CONNECTION
            ip = f"{format_ip_address(temp_ip)}"
            netmask = temp_netmask

            # Temporarily save the IP address and netmask
            apply_ip(connection_name, ip, netmask)
            config.data['selected_button'] = 0
            config.data['selected_confirm_button'] = 0
    elif current_state == "confirm_unlinking":
        if selected_confirm_button == 0:
            config.data['selected_button'] = 0
            config.data['current_state'] = "info_mh"
        elif selected_confirm_button == 1:
            unlink_from_hub()
            config.data['selected_button'] = 0
            config.data['selected_confirm_button'] = 0
    elif current_state == "unlinked":
        config.data['current_state'] = "menu"
    elif current_state == "failed_unlinking":
        config.data['current_state'] = "info_mh"
    elif current_state == "networks_info":
        refresh_networks()
    elif current_state == "no_networks":
        refresh_networks()
    elif current_state == "networks_detected":
        item = networks[current_index]
        known = item["known"]
        if known:
            config.data['selected_button'] = 0
            config.data['selected_digit_index'] = 0
            config.data['current_state'] = "config_network"
        else:
            config.data['selected_hub'] = networks[current_index]
            config.data['temp_password'] = [0] * 8
            config.data['current_state'] = "link_mh"
    elif current_state == "config_network":
        if selected_digit_index == 1:
            config.data['current_state'] = "networks_detected"
            config.data['selected_digit_index'] = 0
            config.data['selected_button'] = 0
        elif selected_digit_index == 0:
            if selected_button == 0:
                item = networks[current_index]
                if item["linked"]:
                    config.data['current_state'] = "confirm_known_unlink"
                else:
                    config.data['current_state'] = "confirm_known_link"
            elif selected_button == 1:
                config.data['current_state'] = "confirm_delete"
            elif selected_button == 2:
                config.data['current_state'] = "confirm_autolink"
    elif current_state == "confirm_known_link":
        item = networks[current_index]
        ssid = item["ssid"]
        if selected_confirm_button == 0:
            config.data['selected_button'] = 0
            config.data['current_state'] = "config_network"
        elif selected_confirm_button == 1:
            link_known_network(ssid)
            config.data['networks'][current_index]["linked"] = True
            config.data['selected_button'] = 0
            config.data['selected_confirm_button'] = 0
    elif current_state == "confirm_known_unlink":
        item = networks[current_index]
        ssid = item["ssid"]
        if selected_confirm_button == 0:
            config.data['selected_button'] = 0
            config.data['current_state'] = "config_network"
        elif selected_confirm_button == 1:
            unlink_known_network(ssid)
            config.data['networks'][current_index]["linked"] = False
            config.data['selected_button'] = 0
            config.data['selected_confirm_button'] = 0
    elif current_state == "confirm_autolink":
        item = networks[current_index]
        ssid = item["ssid"]
        current_autolink = check_autoconnect(ssid)
        if selected_confirm_button == 0:
            config.data['selected_button'] = 0
            if current_autolink != "No":
                autolink_known_network(ssid,"no")
            else:
                config.data['current_state'] = "config_network"
        elif selected_confirm_button == 1:
            config.data['selected_button'] = 0
            selected_confirm_button = 0
            if current_autolink != "Yes":
                autolink_known_network(ssid,"yes")
            else:
                config.data['current_state'] = "config_network"
    elif current_state == "confirm_delete":
        item = networks[current_index]
        ssid = item["ssid"]
        if selected_confirm_button == 0:
            config.data['selected_button'] = 0
            config.data['current_state'] = "config_network"
        elif selected_confirm_button == 1:
            delete_known_network(ssid)
            config.data['networks'][current_index]["known"] = False
            config.data['selected_button'] = 0
            config.data['selected_digit_index'] = 0
    elif current_state == "link_mh":
        if selected_digit_index == 8 and selected_button == 0:
            config.data['current_state'] = "networks_detected"
            config.data['selected_digit_index'] = 0
        elif selected_digit_index == 8 and selected_button == 1:
            config.data['selected_digit_index'] = 0
            config.data['selected_button'] = 0
            link_to_detected_mh()
    elif current_state == "link_success":
        config.data['current_state'] = "menu"
    elif current_state == "link_known_network_successful":
        refresh_networks()
        config.data['selected_button'] = 0
        config.data['selected_confirm_button'] = 0
        config.data['selected_digit_index'] = 0
        config.data['current_index'] = 0
        config.data['current_state'] = "networks_detected"
    elif current_state == "unlink_known_network_successful" or current_state == "autolink_known_network_successful" or current_state == "delete_known_network_successful":
        config.data['selected_button'] = 0
        config.data['selected_confirm_button'] = 0
        config.data['selected_digit_index'] = 0
        config.data['current_index'] = 0
        config.data['current_state'] = "networks_detected"
    elif current_state == "failed_link_known_network" or current_state == "failed_unlink_known_network" or current_state == "failed_autolink_known_network" or current_state == "failed_delete_known_network":
        config.data['selected_button'] = 0
        config.data['selected_confirm_button'] = 0
        config.data['selected_digit_index'] = 0
        config.data['current_state'] = "config_network"
    elif current_state == "incorrect_password" or current_state == "failed_linking":
        config.data['temp_password'] = [0] * 8
        config.data['current_state'] = "link_mh"
    display_current_menu()