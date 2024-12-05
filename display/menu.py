import time
import display.config as config
from display.icons import draw_icons_bottom_right
from utils.screen import blank_screen, display_screen
from views.available_networks import networks_detected_view, networks_info_view, no_networks_view
from views.confirm import confirm_view
from views.detected_mh import failure_link_detected_mh_view, incorrect_password_view, link_detected_mh_view, no_router_view, success_link_detected_mh_view
from views.devices_info import daughter_info_view, daughter_wlan_info_view, mother_info_view
from views.known_network import failure_known_autolink_view, failure_known_delete_view, failure_known_link_view, failure_known_unlink_view, known_network_config_view, success_known_autolink_view, success_known_delete_view, success_known_link_view, success_known_unlink_view
from views.main_menu import menu_view
from views.system_config import ip_applied_view, same_ip_view, system_change_mask_view, system_change_ip_view, system_config_view, system_info_ip_view

def display_current_menu():
    """
    Display the current menu on the screen.
    """
    blank_screen()
    draw_icons_bottom_right()

    current_state = config.data['current_state']
    if current_state == "menu":
        menu_view()
    elif current_state == "info_db":
        time.sleep(0.1)
        daughter_info_view()
    elif current_state == "info_db_wlan_ip":
        time.sleep(0.1)
        daughter_wlan_info_view()
    elif current_state == "info_mh":
        mother_info_view()
    elif current_state == "config":
        system_config_view(config.data['system_config_options'])
    elif current_state == "system_change_ip":
        system_info_ip_view()
    elif current_state == "change_ip":
        system_change_ip_view()
    elif current_state == "netmask":
        system_change_mask_view()
    elif current_state == "same_ip":
        same_ip_view()
    elif current_state == "ip_applied":
        ip_applied_view()
    elif current_state == "system_reboot" or current_state == "system_shutdown" or current_state == "system_change_mode" or current_state == "confirm_change_mode" or current_state == "confirm_unlinking" or current_state == "confirm_ip":
        confirm_view()
    elif current_state == "networks_info":
        networks_info_view()
    elif current_state == "networks_detected":
        time.sleep(0.1)
        networks_detected_view()
    elif current_state == "link_mh":
        link_detected_mh_view()
    elif current_state == "link_success":
        success_link_detected_mh_view()
    elif current_state == "failed_linking":
        failure_link_detected_mh_view()
    elif current_state == "incorrect_password":
        incorrect_password_view()
    elif current_state == "no_router":
        no_router_view()
    elif current_state == "no_networks":
        no_networks_view()
    elif current_state == "config_network":
        known_network_config_view()
    elif current_state == "confirm_known_link" or current_state == "confirm_known_unlink" or current_state == "confirm_autolink" or current_state == "confirm_delete":
        confirm_view()
    elif current_state == "link_known_network_successful":
        success_known_link_view()
    elif current_state == "unlink_known_network_successful" or current_state == "unlinked":
        success_known_unlink_view()
    elif current_state == "autolink_known_network_successful":
        success_known_autolink_view()
    elif current_state == "delete_known_network_successful":
        success_known_delete_view()
    elif current_state == "failed_link_known_network":
        failure_known_link_view()
    elif current_state == "failed_unlink_known_network" or current_state == "failed_unlinking":
        failure_known_unlink_view()
    elif current_state == "failed_autolink_known_network":
        failure_known_autolink_view()
    elif current_state == "failed_delete_known_network":
        failure_known_delete_view()

    if current_state != "networks_detected" and current_state != "info_mh" and current_state != "info_db":
        display_screen()
