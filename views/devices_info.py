import display.config as config
from display.icons import draw_rssi_bars
from utils.center_text import center_text
from utils.screen import display_screen
from utils.scroll_text import start_scrolling_text
from display.config import draw, width, font

def daughter_info_view():
    """Display the DAUGHTER info view."""
    item = config.data['db']
    draw.text((2, 0), f"NAME: ", font=font, fill=255)
    draw.text((2, 10), f"IP (ETHERNET):", font=font, fill=255)
    draw.text((10, 20), f"{item['ip']}", font=font, fill=255)

    # Scrolling text for name
    max_width = (width - (draw.textlength("NAME: ")))
    x_pos = (draw.textlength("NAME: ")) + 4
    start_scrolling_text(config.data['current_state'], config.data['current_index'], f"{item['name']}", max_width, x_pos, 0)

def daughter_webpage_info_view():
    """Display the info for the DAUGHTER webpage"""
    item = config.data['db']

    text1 = f"{item['ip']}:81"
    text2 = "Use the URL to"
    text3 = "access via ETHERNET"
    draw.text((center_text(text1), 0), text1, font=font, fill=255)
    draw.text((center_text(text2), 10), text2, font=font, fill=255)
    draw.text((center_text(text3), 20), text3, font=font, fill=255)

def daughter_wlan_info_view():
    """Display the DAUGHTER WLAN info view."""
    item = config.data['db']
    draw.text((2, 10), f"DAUGHTER IP (WIFI):", font=font, fill=255)

    # Check if the WLAN IP is available
    if item['wlan_ip'] is not None:
        text1 = "Webpage access in MH"
        draw.text((center_text(text1), 0), text1, font=font, fill=255)
        draw.text((10, 20), f"{item['wlan_ip']}", font=font, fill=255)
    else:
        text1 = "Connect to get IP"
        draw.text((center_text(text1), 0), text1, font=font, fill=255)
        draw.text((10, 20), f"N/A", font=font, fill=255)

def mother_info_view():
    """Display the mother info view."""
    item = config.data['mh']
    ssid = item.get('ssid', None)
    rssi = item.get('rssi', None)

    # Check if the Mother Hub is linked
    if ssid is not None and rssi is not None:
        draw.text((0, 0), f"LINKED TO: ", font=font, fill=255)
        draw.text((0, 10), f"RSSI: {item['rssi']}%", font=font, fill=255)
        draw.text((0, 20), f"Push to unlink", font=font, fill=255)
        draw_rssi_bars(int(rssi))

        # Scrolling text for SSID
        max_width = (width - (draw.textlength("LINKED TO: ")))
        x_pos = (draw.textlength("LINKED TO: "))
        start_scrolling_text(config.data['current_state'], config.data['current_index'], f"{ssid}", max_width, x_pos, 0)
    else:
        text1 = "NO MOTHER HUB LINKED"
        text2 = "Push to search"
        text3 = "for networks"
        draw.text((center_text(text1), 0), text1, font=font, fill=255)
        draw.text((center_text(text2), 10), text2, font=font, fill=255)
        draw.text((center_text(text3), 20), text3, font=font, fill=255)
        display_screen()