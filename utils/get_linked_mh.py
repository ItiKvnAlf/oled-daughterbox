import subprocess
import time
import display.config as config
from system.constants import NMCLI_SCAN_WIFI_NETWORKS
from views.loading import loading_mh_info_view

def get_linked_mh():
    """
    Returns the SSID and signal strength (RSSI) of the currently linked Wi-Fi network.

    Returns:
        data (dict): A dictionary containing the SSID and RSSI of the linked network.
    """
    # Display the loading MH info view if the current state is info_db
    if config.data['current_state'] == "info_db":
        loading_mh_info_view()
        time.sleep(0.5)

    try:
        # Run nmcli command to list active Wi-Fi connections
        command = NMCLI_SCAN_WIFI_NETWORKS
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        
        # Check for errors
        if result.returncode != 0:
            raise Exception(result.stderr.strip())
        
        # Parse the output to find the active connection
        for line in result.stdout.strip().split('\n'):
            if line.startswith("yes:"):  # Active connection starts with 'yes:'
                _, ssid, signal = line.split(':', 2)
                config.data['mh'] = {"ssid": ssid, "rssi": f"{signal}"}
                return {"ssid": ssid, "rssi": f"{signal}"}
        
        # If no active connection is found
        config.data['mh'] = {"ssid": ssid, "rssi": f"{signal}"}
        return {"ssid": None, "rssi": None}
    
    except Exception as e:
        return {"error": str(e)}