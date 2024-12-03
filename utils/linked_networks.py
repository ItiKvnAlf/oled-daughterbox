import subprocess

from system.constants import NMCLI_SCAN_WIFI_NETWORKS

def network_linked_list():
    """Check if the network is currently linked."""
    try:
        command = NMCLI_SCAN_WIFI_NETWORKS
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

        linked = result.stdout.strip().split("\n")
        return linked
    except Exception as e:
        print(f"Error checking network connection: {e}")
        return False
    
def is_network_linked(ssid: str, linked_networks: list):
    """
    Check if the network is currently linked.
    Args:
        ssid (str): The SSID of the network.
        linked_networks (list): A list of linked network SSIDs.
    """
    for line in linked_networks:
        parts = line.split(":")
        active = parts[0]
        network_ssid = parts[1]
        if network_ssid == ssid and active == "yes":
            return True
    return False