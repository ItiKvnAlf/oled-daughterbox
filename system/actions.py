import os
import RPi.GPIO as GPIO # type: ignore
import subprocess
from system.constants import DEVICE_MODE_FILE_PATH, REBOOT_SYSTEM, SHUTDOWN_SYSTEM
from utils.screen import blank_screen, display_screen
import display.config as config
from display.config import disp

def reboot_system():
    blank_screen()
    display_screen()
    disp.poweroff()
    GPIO.cleanup()
    try:
        command = REBOOT_SYSTEM
        subprocess.run(command, check=True, shell=True)
    except Exception as e:
        print(f"An error occurred while trying to reboot: {e}")

def shutdown_system():
    blank_screen()
    display_screen()
    disp.poweroff()
    GPIO.cleanup()
    try:
        command = SHUTDOWN_SYSTEM
        subprocess.run(command, check=True, shell=True)
    except Exception as e:
        print(f"An error occurred while trying to shutdown: {e}")

def change_mode():
    """
    Changes the mode of the device between 'AP' and 'STA' and reboots the system.
    """
    blank_screen()
    display_screen()
    disp.poweroff()
    GPIO.cleanup()
    try:
        current_mode = get_device_mode()
        set_device_mode(current_mode)
        reboot_system()
    except Exception as e:
        print(f"An error occurred while trying to change mode: {e}")

def get_device_mode() -> str:
    """
    Retrieves the mode from the file specified by the MODE_FILE_PATH environment variable.
    The mode can only be 'AP' or 'STA'.

    Returns:
        str: The mode ('AP' or 'STA').

    Raises:
        ValueError: If the mode is not 'AP' or 'STA'.
        FileNotFoundError: If the mode file does not exist.
    """

    if not os.path.exists(DEVICE_MODE_FILE_PATH):
        raise FileNotFoundError(f"Mode file not found at path: {DEVICE_MODE_FILE_PATH}")

    with open(DEVICE_MODE_FILE_PATH, 'r') as file:
        mode = file.read().strip()

    if mode not in ['AP', 'STA']:
        raise ValueError("Mode must be either 'AP' or 'STA'")

    print("Get mode result:",mode)
    return mode


def set_device_mode(mode: str):
    """
    Sets the mode in the file specified by the MODE_FILE_PATH environment variable.
    The mode can only be 'AP' or 'STA'.

    Args:
        new_mode (str): The new mode to set ('AP' or 'STA').

    Raises:
        ValueError: If the new mode is not 'AP' or 'STA'.
        FileNotFoundError: If the mode file does not exist.
    """

    if mode not in ['AP', 'STA']:
        raise ValueError("Mode must be either 'AP' or 'STA'")
    
    if mode == 'AP':
        new_mode = 'STA'
    elif mode == 'STA':
        new_mode = 'AP'

    if not os.path.exists(DEVICE_MODE_FILE_PATH):
        raise FileNotFoundError(f"Mode file not found at path: {DEVICE_MODE_FILE_PATH}")

    with open(DEVICE_MODE_FILE_PATH, 'w') as file:
        file.write(new_mode)

    