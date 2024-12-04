import display.config as config
from views.system_config import confirm_system_change_ip_view, confirm_system_change_mode_view, confirm_system_reboot_view, confirm_system_shutdown_view, system_change_mode_view
from views.known_network import confirm_known_autolink_view, confirm_known_delete_view, confirm_known_link_view, confirm_known_unlink_view, confirm_unlinking_mh_view
from display.config import draw, font

def confirm_view():
    """Display the confirm view."""

    # Get confirm view based on the current state
    if config.data['current_state'] == "confirm_ip":
        confirm_system_change_ip_view()
    elif config.data['current_state'] == "system_reboot":
        confirm_system_reboot_view()
    elif config.data['current_state'] == "system_shutdown":
        confirm_system_shutdown_view()
    elif config.data['current_state'] == "system_change_mode":
        system_change_mode_view()
    elif config.data['current_state'] == "confirm_change_mode":
        confirm_system_change_mode_view()
    elif config.data['current_state'] == "confirm_unlinking":
        confirm_unlinking_mh_view()
    elif config.data['current_state'] == "confirm_known_link":
        confirm_known_link_view()
    elif config.data['current_state'] == "confirm_known_unlink":
        confirm_known_unlink_view()
    elif config.data['current_state'] == "confirm_autolink":
        confirm_known_autolink_view()
    elif config.data['current_state'] == "confirm_delete":
        confirm_known_delete_view()

    # Buttons for confirmation

    # Check if "NO" button is selected
    if config.data['selected_confirm_button'] == 0:
        # Draw "NO" button as selected (white background, black text)
        draw.rectangle((39, 21, 57, 29), fill=255)
        draw.text((41, 20), "NO", font=font, fill=0)
    else:
        # Draw "NO" button as normal (black background, white text)
        draw.text((41, 20), "NO", font=font, fill=255)
    
    # Check if "YES" button is selected
    if config.data['selected_confirm_button'] == 1:
        # Draw "YES" button as selected (white background, black text)
        draw.rectangle((68, 21, 90, 29), fill=255)
        draw.text((70, 20), "YES", font=font, fill=0)
    else:
        # Draw "YES" button as normal (black background, white text)
        draw.text((70, 20), "YES", font=font, fill=255)