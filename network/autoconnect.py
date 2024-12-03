import subprocess

from system.constants import NMCLI_GET_AUTOCONNECT

def check_autoconnect(ssid: str):
    """
    Check if a Wi-Fi network is set to autoconnect.

    Args:
        ssid (str): The SSID of the Wi-Fi network.

    Returns:
        value (str): "Yes" if the network is set to autoconnect, "No" otherwise.
    """
    try:
        # Run the nmcli command to get connection details
        command = NMCLI_GET_AUTOCONNECT.format(ssid)
        result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True)
        
        # Check if the output contains the line with connection.autoconnect
        if f'connection.autoconnect:yes' in result.stdout.replace(" ",""):
            return "Yes"
        else:
            return "No"
    except subprocess.CalledProcessError as e:
        print(f"Error while checking the connection: {e}")
        return None
    
