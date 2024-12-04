import time
import RPi.GPIO as GPIO # type: ignore
from system.constants import ETHERNET_CONNECTION, WIRELESS_INTERFACE
from utils.refresh import refresh_networks
from display.menu import display_current_menu
from network.ip import get_mask
from network.update import update_ethernet_ip, update_wlan_ip
from network.hostname import get_hostname, update_hostname
from inputs.buttons import handle_buttons, setup_buttons
from utils.screen import blank_screen, display_screen
from utils.threading import start_thread
from utils.get_ip import get_ip_address, get_wireless_ip_address
from utils.get_linked_mh import get_linked_mh
from views.loading import initial_screen_view
import display.config as config
from display.config import disp

# GPIO Button Pins (Up, Down, Left, Right, Middle) using BCM numbering
U_BTN, D_BTN, L_BTN, R_BTN, M_BTN = 5, 6, 13, 19, 26

# Setup GPIO
setup_buttons(U_BTN, D_BTN, L_BTN, R_BTN, M_BTN)

# Display initial screen
initial_screen_view()
time.sleep(2)

# Update global data
config.data['db'] = {
    'ip': get_ip_address(ETHERNET_CONNECTION),
    'wlan_ip': get_wireless_ip_address(WIRELESS_INTERFACE),
    'mask': get_mask(ETHERNET_CONNECTION),
    'name': get_hostname(),
}
config.data['temp_ip'] = [int(digit) for digit in "".join(part.zfill(3) for part in get_ip_address(ETHERNET_CONNECTION).split('.'))]
config.data['temp_mask'] = get_mask(ETHERNET_CONNECTION)

# Main loop
try:
    refresh_networks()
    display_current_menu()

    # Start threads
    start_thread(update_ethernet_ip)
    start_thread(update_wlan_ip)
    start_thread(update_hostname)
    start_thread(get_linked_mh)

    while True:
        time.sleep(0.1)
        handle_buttons(U_BTN, D_BTN, L_BTN, R_BTN, M_BTN)

except Exception as e:
    GPIO.cleanup()
    blank_screen()
    display_screen()
    disp.poweroff()
    print("An error occurred:", e)
