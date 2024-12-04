import display.config as config
import time

from system.constants import ETHERNET_CONNECTION, WIRELESS_INTERFACE
from utils.get_ip import get_ip_address, get_wireless_ip_address

def update_ethernet_ip():
    """
    Update the IP address of the Ethernet interface in the global data.
    """
    # Continuously check for changes in the ethernet IP address
    while True:
        current_eth_ip = get_ip_address(ETHERNET_CONNECTION)
        # Update IP in db if it has changed
        if config.data['db']["ip"] != current_eth_ip:
            config.data['db']["ip"] = current_eth_ip
        time.sleep(10)  # Check every 10 seconds for changes

def update_wlan_ip():
    """
    Update the IP address of the WLAN interface in the global data.
    """
    # Continuously check for changes in the wlan IP address
    while True:
        current_wlan_ip = get_wireless_ip_address(WIRELESS_INTERFACE)
        # Update IP in db if it has changed
        if config.data['db']["wlan_ip"] != current_wlan_ip:
            config.data['db']["wlan_ip"] = current_wlan_ip
        time.sleep(10)  # Check every 10 seconds for changes