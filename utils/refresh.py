import subprocess
import time
import display.config as config
from system.constants import NMCLI_REFRESH
from views.loading import scanning_networks_view
from utils.known_networks import get_network_known_list, is_network_known
from utils.linked_networks import network_linked_list, is_network_linked

def refresh_networks():
    """
    Refresh the list of available Wi-Fi networks.
    """
    # Display the scanning networks view if the current state is networks_info or no_networks
    if config.data['current_state'] == "networks_info" or config.data['current_state'] == "no_networks" or config.data['current_state'] == "link_known_network_successful":
        scanning_networks_view()
        time.sleep(1)

    # Get the list of known and linked networks
    config.data['known_networks'] = get_network_known_list()
    config.data['linked_networks'] = network_linked_list()

    try:
        # Run the nmcli command to scan for available networks
        command = NMCLI_REFRESH
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        
        # Check if the command executed successfully
        if result.returncode == 0:
            # Process the command output to extract the network list
            network_list = result.stdout.replace("\\", "").splitlines()
            # Filter networks containing the target MAC prefix
            filtered_output = [line for line in network_list if ":B8:27:EB" in line]

            config.data['networks'] = []
            # Parse filtered networks into SSID and RSSI
            for network in filtered_output:
                try:
                    # Split the network string by colon ':'
                    parts = network.split(":")
                    
                    # Extract the SSID and RSSI
                    ssid = parts[7]  # The SSID is the 7th element

                    if not ssid:
                        ssid = "<Hidden>"

                    rssi = parts[11]  # The RSSI is the 11th element

                    # Check if the network is known
                    known = is_network_known(ssid, config.data['known_networks'])
                    linked = is_network_linked(ssid, config.data['linked_networks'])
                    
                    # Add to the networks list
                    config.data['networks'].append({"ssid": ssid, "rssi": rssi, "known": known, "linked": linked})
                except (IndexError, ValueError):
                    # Handle unexpected line formats
                    print(f"Unexpected line format: {network}. Could not extract SSID and RSSI.")

            # Sort the networks list: linked first, then known, then the rest
            config.data['networks'] = sorted(
                config.data['networks'], 
                key=lambda x: (not x["linked"], not x["known"])
            )
            
            if config.data['current_state'] == "no_networks" and len(config.data['networks']) > 0:
                config.data['current_state'] = "networks_info"
            elif config.data['current_state'] == "networks_info" and len(config.data['networks']) == 0:
                config.data['current_state'] = "no_networks"
        else:
            print("The nmcli command failed.")
    
    except Exception as e:
        print(f"An error occurred while trying to refresh networks: {e}")