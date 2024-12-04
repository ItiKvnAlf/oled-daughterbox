import time
import subprocess
import display.config as config
from system.constants import NMCLI_GET_IP4_ADDRESS, NMCLI_SET_IP4_ADDRESS
from utils.refresh import refresh_networks
from views.loading import applying_ip_view

def get_mask(connection: str):
    """
    Retrieves the netmask of a specific network interface using nmcli.
    Args:
        connection: The network interface to check (e.g. ETH, WLAN).
    """
    try:
        # Run the nmcli command to get the IP address of the interface
        command = NMCLI_GET_IP4_ADDRESS.format(connection)
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        # Process the command output to extract the mask
        for line in result.stdout.splitlines():
            # Check if the line contains the IP address
            if "IP4.ADDRESS" in line:
                mask = int(line.split(":")[1].strip().split('/')[1])  # Extract the mask
                return mask
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    return None

def calculate_netmask_prefix():
    """
    Calculates an appropriate netmask prefix for an IP address represented by a list of 12 digits.
    The function returns the netmask prefix notation (e.g., /8, /16, /24).

    Parameters:
    temp_ip (list): List of 12 integers, representing the IP address in 4 octets.

    Returns:
    int: The netmask prefix notation.
    """
    # Convert the 12-digit list into standard IP octet format
    octet1 = int("".join(map(str, config.data['temp_ip'][0:3])))
    octet2 = int("".join(map(str, config.data['temp_ip'][3:6])))
    
    # Determine the mask prefix based on IP address class and private IP ranges
    if 1 <= octet1 <= 126:
        # Class A (public or private)
        return 8
    elif 128 <= octet1 <= 191:
        # Class B (public or private in the range 172.16.x.x to 172.31.x.x)
        if octet1 == 172 and 16 <= octet2 <= 31:
            return 16  # Class B private
        else:
            return 8  # General Class B fallback
    elif 192 <= octet1 <= 223:
        # Class C (public or private in the range 192.168.x.x)
        if octet1 == 192 and octet2 == 168:
            return 24  # Class C private
        else:
            return 16  # General Class C fallback
    else:
        # Default to Class A for other IPs
        return 8
    
def validate_ip_digit_list():
    """Validates the IP address represented by a list of 12 digits.
    - If the first digit of an octet is '2', the next digits should limit the octet to a maximum of 255.
    - If the first two digits are '25', the last digit should be limited to 5.
    - Ensures that the last octet is not 255 or 0.
    """
    for i in range(0, 12, 3):  # Iterate over each octet in steps of 3
        first_digit = config.data['temp_ip'][i]
        second_digit = config.data['temp_ip'][i + 1]
        third_digit = config.data['temp_ip'][i + 2]
        
        # Case where the first digit of the octet is '2'
        if first_digit == 2:
            # Limit the entire octet to 255
            if second_digit > 5:
                second_digit = 5
            if second_digit == 5 and third_digit > 5:
                third_digit = 5
        
        # Case where the octet starts with '25'
        elif first_digit == 2 and second_digit == 5:
            if third_digit > 5:
                third_digit = 5

        # Special validation for the last octet (avoid 255 or 0)
        if i == 9:  # Last octet starts at index 9
            octet_value = first_digit * 100 + second_digit * 10 + third_digit
            if octet_value == 255:  # Adjust from 255 to 254
                third_digit = 4
            elif octet_value == 0:  # Adjust from 0 to 1
                third_digit = 1

        # Update the digit list with validated values
        config.data['temp_ip'][i] = first_digit
        config.data['temp_ip'][i + 1] = second_digit
        config.data['temp_ip'][i + 2] = third_digit

def format_ip_address(ip_digits: list):
    """
    Formats a list of 12 integers into a standard IP address format with octets separated by dots.

    Args:
        ip_digits (list): List of 12 integers representing an IP address (e.g., [1, 9, 2, 1, 6, 8, 0, 0, 1, 0, 0, 1])

    Returns:
        octets (str): IP address in standard dotted format (e.g., "192.168.0.1")
    """
    # Convert each group of 3 digits into an octet
    octets = [str(int("".join(map(str, ip_digits[i:i+3])))) for i in range(0, 12, 3)]
    # Join the octets with dots
    return ".".join(octets)

def apply_ip(connection: str, ip: str, mask: str):
    """
    Apply the IP address and mask to the Ethernet interface.

    Args:
        connection (str): The connection interface to apply the IP address to.
        ip (str): The IP address to apply.
        mask (str): The mask to apply.
    """
    # Display the applying IP view
    if config.data['current_state'] == "confirm_ip":
        applying_ip_view()
        time.sleep(1)

    # Apply the IP address and mask to the Ethernet interface
    try:
        # Run the command to apply the IP address
        command = NMCLI_SET_IP4_ADDRESS.format(connection, ip, mask)
        result = subprocess.run(command, shell=True, check=True)

        # Check if the command was successful
        if result.returncode == 0:
            refresh_networks()
            config.data['db']["ip"] = ip
            config.data['db']["mask"] = mask
            config.data['current_state'] = "ip_applied"
    except subprocess.CalledProcessError as e:
        print("Error applying IP:", e)
