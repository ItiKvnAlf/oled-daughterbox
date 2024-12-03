import subprocess
import time
import display.config as config
from system.config import get_env_variable
from system.constants import NMCLI_DELETE_KNOWN_WIFI_CONNECTION, NMCLI_LINK_TO_KNOWN_WIFI_CONNECTION, NMCLI_SET_AUTOCONNECT_TO_WIFI_CONNECTION, NMCLI_UNLINK_FROM_WIFI_CONNECTION, WIRELESS_INTERFACE
from utils.get_ip import get_wireless_ip_address
from utils.get_linked_mh import get_linked_mh
from utils.refresh import refresh_networks
from views.loading import linking_to_known_network_view, unlinking_from_known_network_view, unlinking_from_mh_view

def link_known_network(ssid: str):
    """
    Link to a known network with the specified SSID.
    This function should be called when the user confirms the link request.
    Args:
        ssid (str): The SSID of the known network to link to.
    """

    # Check if the current state is confirm_known_link and display the loading view
    if config.data['current_state'] == "confirm_known_link":
        linking_to_known_network_view(ssid)
        time.sleep(1)

    # Try to link to the known network
    try:
        command = NMCLI_LINK_TO_KNOWN_WIFI_CONNECTION.format(ssid)
        result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True)
        
        config.data['db']['wlan_ip'] = get_wireless_ip_address(get_env_variable(WIRELESS_INTERFACE))
        config.data['mh'] = get_linked_mh()
        
        if result.returncode == 0:
            config.data['current_state'] = "link_known_network_successful"
        else:
            config.data['current_state'] = "failed_link_known_network"
    except Exception as e:
        print(f"An error occurred while trying to link known network: {e}")

def unlink_known_network(ssid: str):
    """
    Unlink from a known network with the specified SSID.
    This function should be called when the user confirms the unlink request.
    Args:
        ssid (str): The SSID of the known network to unlink from.
    """
    # Check if the current state is confirm_known_unlink and display the loading view
    if config.data['current_state'] == "confirm_known_unlink":
        unlinking_from_known_network_view(ssid)
        time.sleep(1)

    # Try to unlink from the known network
    try:
        command = NMCLI_UNLINK_FROM_WIFI_CONNECTION.format(ssid)
        result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True)
        
        config.data['db']['wlan_ip'] = get_wireless_ip_address(get_env_variable(WIRELESS_INTERFACE))
        config.data['mh'] = get_linked_mh()
        refresh_networks()

        if result.returncode == 0:
            config.data['current_state'] = "unlink_known_network_successful"
        else:
            config.data['current_state'] = "failed_unlink_known_network"
    except Exception as e:
        print(f"An error occurred while trying to unlink known network: {e}")

def delete_known_network(ssid: str):
    """
    Delete a known network from the system.
    Args:
        ssid (str): The SSID of the network to delete.
    """
    # Try to delete the known network
    try:
        command = NMCLI_DELETE_KNOWN_WIFI_CONNECTION.format(ssid)
        result = subprocess.run(command, check=True, shell=True)

        # Check if the command was successful
        if result.returncode == 0:
            config.data['current_state'] = "delete_known_network_successful"
        # If the command failed
        else:
            config.data['current_state'] = "failed_delete_known_network"
    except Exception as e:
        print(f"An error occurred while trying set delete {ssid}: {e}")

def autolink_known_network(ssid: str, value: str):
    """
    Set the autolink value for a known network.
    Args:
        ssid (str): The SSID of the known network.
        value (str): The value to set ("yes" or "no").
    """
    # Try to set the autolink value for the known network
    try:
        command = NMCLI_SET_AUTOCONNECT_TO_WIFI_CONNECTION.format(ssid, value)
        result = subprocess.run(command, check=True, shell=True)
        
        # Check if the command was successful
        if result.returncode == 0:
            config.data['current_state'] = "autolink_known_network_successful"
        # If the command failed
        else:
            config.data['current_state'] = "failed_autolink_known_network"
    except Exception as e:
        print(f"An error occurred while trying set autolink value: {e}")

def unlink_from_hub():
    """
    Disconnects from the currently linked Mother Hub.
    This function should be called when the user confirms the unlink request.
    """
    # Check if the current state is confirm_unlinking and display the loading view
    if config.data['current_state'] == "confirm_unlinking":
        unlinking_from_mh_view()
        time.sleep(1)

    try:
        ssid = config.data['mh']['ssid']
        
        # Execute the nmcli command
        command = NMCLI_UNLINK_FROM_WIFI_CONNECTION.format(ssid)
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        config.data['mh'] = get_linked_mh()
        config.data['db']["wlan_ip"] = get_wireless_ip_address(get_env_variable(WIRELESS_INTERFACE))
        refresh_networks()
        # Check if the disconnection was successful
        if result.returncode == 0:
            config.data['current_state'] = "unlinked"
        else:
            config.data['current_state'] = "failed_unlinking"
    
    except Exception as e:
        print(f"An error occurred while trying to unlink: {e}")