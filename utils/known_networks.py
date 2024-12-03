import subprocess
from system.constants import NMCLI_GET_WIFI_CONNECTIONS

def get_network_known_list():
    """Check if a network is saved/known in the system."""
    try:
        command = NMCLI_GET_WIFI_CONNECTIONS
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

        known = result.stdout.strip().split("\n")
        return known
    except Exception as e:
        print(f"Error checking known networks: {e}")
        return False
    
def is_network_known(ssid: str, known_networks: list):
    """
    Check if a network is saved/known in the system.
    Args:
        ssid (str): The SSID of the network.
        known_networks (list): A list of known network SSIDs.
    """
    return ssid in known_networks