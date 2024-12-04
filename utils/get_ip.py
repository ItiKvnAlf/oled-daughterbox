import subprocess

from system.constants import NMCLI_GET_IP4_ADDRESS, NMCLI_GET_IP4_ADDRESS_WIRELESS

def get_ip_address(connection: str):
    """
    Get the IP address of a specific network interface using nmcli.
    :param connection: The network connection to check (e.g. eth0, wlan0).
    :return: IP address as a string, or None if not found.
    """
    try:
        # Run the nmcli command to get the IP address of the interface
        command = NMCLI_GET_IP4_ADDRESS.format(connection)
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        # Process the command output to extract the IP address
        for line in result.stdout.splitlines():
            # Check if the line contains the IP address
            if "IP4.ADDRESS" in line:
                ip = line.split(":")[1].strip().split('/')[0]  # Extract only the IP
                return ip
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    return None

def get_wireless_ip_address(interface: str = "wlan0"):
    """
    Get the IP address of the wireless network interface.
    :return: IP address as a string, or None if not found.
    """
    try:
        # Run the nmcli command to get the IP address of the interface
        command = NMCLI_GET_IP4_ADDRESS_WIRELESS.format(interface)
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        # Process the command output to extract the IP address
        for line in result.stdout.splitlines():
            # Check if the line contains the IP address
            if "IP4.ADDRESS" in line:
                ip = line.split()[-1].split('/')[0]  # Extract only the IP
                return ip
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    return None