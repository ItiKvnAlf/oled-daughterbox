import time
import subprocess
import display.config as config
from network.actions import delete_known_network
from system.constants import NMCLI_LINK_TO_NEW_AP
from utils.refresh import refresh_networks
from views.loading import linking_to_mh_view
    
def link_to_detected_mh():
    """
    Connects to a Mother Hub with the specified SSID and password.
    This function should be called when the user confirms the connection request.

    Parameters:
    ssid (str): The SSID of the Mother Hub to connect to.
    password (str): The password for the Mother Hub network.
    """

    if config.data['current_state'] == "link_mh":
        linking_to_mh_view()
        time.sleep(1)

    mh = config.data['selected_hub']
    
    mh_ssid = mh["ssid"]
    password = "".join(map(str, config.data['temp_password']))

    try:
        # Execute the nmcli command
        command = NMCLI_LINK_TO_NEW_AP.format(mh_ssid, password)
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        
        # Check if the connection was successful
        if result.returncode == 0:
            config.data['mh']['ssid'] = mh["ssid"]
            config.data['mh']['rssi'] = mh["rssi"]
            refresh_networks()
            config.data['current_state'] = "link_success"
        else:
            # Analyze the error message
            error_message = result.stderr.lower()
            incorrect_password_error = "error: connection activation failed: secrets were required, but not provided."
            no_router_error = "error: connection activation failed: ip configuration could not be reserved (no available address, timeout, etc.)."
            no_ssid_error = f"error: no network with ssid '{mh["ssid"]}' found."
            print("Error message:", error_message, flush=True)
            if incorrect_password_error in error_message:
                delete_known_network(mh["ssid"])
                config.data['current_state'] = "incorrect_password"
            elif no_router_error in error_message:
                delete_known_network(mh["ssid"])
                config.data['current_state'] = "no_router"
            elif no_ssid_error.lower() in error_message:
                delete_known_network(mh['ssid'])
                config.data['current_state'] = "no_ssid_found"
            else:
                delete_known_network(mh["ssid"])
                config.data['current_state'] = "failed_linking"
    
    except Exception as e:
        print(f"An error occurred while trying to connect: {e}")