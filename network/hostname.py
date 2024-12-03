import socket
import time
import display.config as config

def get_hostname():
    """Get the hostname of the device."""
    return socket.gethostname()

def update_hostname():
    while True:
        current_hostname = get_hostname()
        # Update hostname in db if it has changed
        if config.data['db']["name"] != current_hostname:
            config.data['db']["name"] = current_hostname
        time.sleep(10)  # Check every 10 seconds for changes