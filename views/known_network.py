import display.config as config
from network.autoconnect import check_autoconnect
from utils.center_text import center_text
from display.icons import set_icon_center
from display.config import draw, width, font

def known_network_config_view():
    """Display the known network configuration."""
    item = config.data['networks'][config.data['current_index']]
    linked = item["linked"]

    if config.data['selected_digit_index'] == 0:
        set_icon_center('right')
        if config.data['selected_button'] == 0:
            # If the selected button is "UNLINK" or "LINK"
            if linked:
                text1 = "UNLINK"
            else:
                text1 = "LINK"
            width1 = (width // 2 - draw.textlength(text1)) // 2 
            draw.rectangle((width1 - 2, 0, width1 + draw.textlength(text1), 10), fill=255)  # White background
            draw.text((width1, 0), text1, font=font, fill=0)  # Black text
            set_icon_center('down')
        else:
            # Transparent background for other buttons
            text1 = "UNLINK" if linked else "LINK"
            draw.text(((width // 2 - draw.textlength(text1)) // 2, 0), text1, font=font, fill=255)

        if config.data['selected_button'] == 1:
            # If the selected button is "DELETE"
            text2 = "DELETE"
            width2 = (width // 2 - draw.textlength(text2)) // 2 
            draw.rectangle((width2 - 2, 10, width2 + draw.textlength(text2), 20), fill=255)  # White background
            draw.text((width2, 10), text2, font=font, fill=0)  # Black text
            set_icon_center('up')
            set_icon_center('down')
        else:
            # Transparent background for other buttons
            text2 = "DELETE"
            draw.text(((width // 2 - draw.textlength(text2)) // 2 , 10), text2, font=font, fill=255)

        if config.data['selected_button'] == 2:
            # If the selected button is "AUTOLINK"
            text3 = "AUTOLINK"
            width3 = (width // 2 - draw.textlength(text3)) // 2 
            draw.rectangle((width3 - 2, 20, width3 + draw.textlength(text3), 30), fill=255)  # White background
            draw.text((width3, 20), text3, font=font, fill=0)  # Black text
            set_icon_center('up')
        else:
            # Transparent background for other buttons
            text3 = "AUTOLINK"
            draw.text(((width // 2 - draw.textlength(text3)) // 2, 20), text3, font=font, fill=255)

        text4 = "BACK"
        draw.text(((width - draw.textlength(text4) - 10), 10), text4, font=font, fill=255)

    else:
        # If the first button is not selected, draw all buttons with transparent background
        set_icon_center('left')

        text1 = "UNLINK" if linked else "LINK"
        draw.text(((width // 2 - draw.textlength(text1)) // 2, 0), text1, font=font, fill=255)

        text2 = "DELETE"
        draw.text(((width // 2 - draw.textlength(text2)) // 2, 10), text2, font=font, fill=255)

        text3 = "AUTOLINK"
        draw.text(((width // 2 - draw.textlength(text3)) // 2, 20), text3, font=font, fill=255)

        text4 = "BACK"
        width4 = (width - draw.textlength(text4) - 10)
        draw.rectangle((width4 - 2, 10, width4 + draw.textlength(text4), 20), fill=255)  # White background
        draw.text((width4, 10), text4, font=font, fill=0)

def confirm_unlinking_mh_view():
    """Display the confirm unlinking view."""
    text1 = "Confirm UNLINKING"
    text2 = "from this MOTHER HUB?"
    draw.text((center_text(text1), 0), text1, font=font, fill=255)
    draw.text((center_text(text2), 10), text2, font=font, fill=255)

def confirm_known_link_view():
    """Display the confirm known link view."""
    item = config.data['networks'][config.data['current_index']]
    ssid = item["ssid"]
    text1 = "Confirm LINKING to"
    text2 = f"{ssid}?"
    draw.text((center_text(text1), 0), text1, font=font, fill=255)
    draw.text((center_text(text2), 10), text2, font=font, fill=255)

def success_known_link_view():
    """Display the success known link view."""
    text1 = "LINKED"
    text2 = "Push to continue"
    draw.text((center_text(text1), 5), text1, font=font, fill=255)
    draw.text((center_text(text2), 15), text2, font=font, fill=255)

def failure_known_link_view():
    """Display the failure known link view."""
    text1 = "Failed to"
    text2 = "LINK"
    text3 = "Push to go back"
    draw.text((center_text(text1), 0), text1, font=font, fill=255)
    draw.text((center_text(text2), 10), text2, font=font, fill=255)
    draw.text((center_text(text3), 20), text3, font=font, fill=255)

def confirm_known_unlink_view():
    """Display the confirm known unlink view."""
    item = config.data['networks'][config.data['current_index']]
    ssid = item["ssid"]
    text1 = "UNLINK from"
    text2 = f"{ssid}?"
    draw.text((center_text(text1), 0), text1, font=font, fill=255)
    draw.text((center_text(text2), 10), text2, font=font, fill=255)

def success_known_unlink_view():
    """Display the success known unlink view."""
    text1 = "UNLINKED"
    text2 = "Push to continue"
    draw.text((center_text(text1), 5), text1, font=font, fill=255)
    draw.text((center_text(text2), 15), text2, font=font, fill=255)

def failure_known_unlink_view():
    """Display the failure known unlink view."""
    text1= "Failed to"
    text2 = "UNLINK"
    text3 = "Push to go back"
    draw.text((center_text(text1), 0), text1, font=font, fill=255)
    draw.text((center_text(text2), 10), text2, font=font, fill=255)
    draw.text((center_text(text3), 20), text3, font=font, fill=255)

def confirm_known_autolink_view():
    """Display the confirm known autolink view."""
    item = config.data['networks'][config.data['current_index']]
    ssid = item["ssid"]
    autolink = check_autoconnect(ssid)
    text1 = "AUTOLINK to this MH?"
    text2 = f"(Current: {autolink})"
    draw.text((center_text(text1), 0), text1, font=font, fill=255)
    draw.text((center_text(text2), 10), text2, font=font, fill=255)

def success_known_autolink_view():
    """Display the success known autolink view."""
    text1 = "Changes to AUTOLINK"
    text2 = "applied"
    text3 = "Push to continue"
    draw.text((center_text(text1), 0), text1, font=font, fill=255)
    draw.text((center_text(text2), 10), text2, font=font, fill=255)
    draw.text((center_text(text3), 20), text3, font=font, fill=255)

def failure_known_autolink_view():
    """Display the failure known autolink view."""
    text1 = "Failed to apply"
    text2 = "AUTOLINK changes"
    text3 = "Push to continue"
    draw.text((center_text(text1), 0), text1, font=font, fill=255)
    draw.text((center_text(text2), 10), text2, font=font, fill=255)
    draw.text((center_text(text3), 20), text3, font=font, fill=255)

def confirm_known_delete_view():
    """Display the confirm known delete view."""
    item = config.data['networks'][config.data['current_index']]
    ssid = item["ssid"]
    text1 = "Confirm DELETION of"
    text2 = f"{ssid}?"
    draw.text((center_text(text1), 0), text1, font=font, fill=255)
    draw.text((center_text(text2), 10), text2, font=font, fill=255)

def success_known_delete_view():
    """Display the success known delete view."""
    item = config.data['networks'][config.data['current_index']]
    text1 = item["ssid"]
    text2 = "DELETED"
    text3 = "Push to continue"
    draw.text((center_text(text1), 0), text1, font=font, fill=255)
    draw.text((center_text(text2), 10), text2, font=font, fill=255)
    draw.text((center_text(text3), 20), text3, font=font, fill=255)

def failure_known_delete_view():
    """Display the failure known delete view."""
    item = config.data['networks'][config.data['current_index']]
    text1 = "Failed to DELETE"
    text2 = item["ssid"]
    text3 = "Push to continue"
    draw.text((center_text(text1), 0), text1, font=font, fill=255)
    draw.text((center_text(text2), 10), text2, font=font, fill=255)
    draw.text((center_text(text3), 20), text3, font=font, fill=255)