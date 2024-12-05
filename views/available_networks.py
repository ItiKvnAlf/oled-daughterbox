import display.config as config
from display.icons import draw_rssi_bars
from utils.center_text import center_text
from utils.scroll_text import start_scrolling_text
from display.config import draw, width, font

def networks_info_view():
    """Display the networks info view."""
    item = config.data['networks']
    text1 = f"MOTHERS DETECTED: {len(item)}"
    text2 = "Push to refresh"
    draw.text((0, 0), text1, font=font, fill=255)
    draw.text((0, 20), text2, font=font, fill=255)
    
def networks_detected_view():
    """Display the networks detected view."""
    item = config.data['networks'][config.data['current_index']]
    ssid = item["ssid"]
    rssi = item["rssi"]
    known = item["known"]
    linked = item["linked"]

    if known:  # If the network is known
        status_text = "KNOWN (Linked)" if linked else "KNOWN (Unlinked)"
        # Draw white background for status text
        draw.rectangle((0, 11, draw.textlength(status_text) + 1, 19), fill=255)  # White background
        draw.text((1, 10), status_text, font=font, fill=0)  # Black text
        draw.text((0, 20), f"Push to config", font=font, fill=255)
    else:
        # Display RSSI if the network is not known
        draw.text((0, 10), f"RSSI: {rssi}%", font=font, fill=255)
        draw.text((0, 20), f"Push to link", font=font, fill=255)
    draw_rssi_bars(int(rssi))  # Draw signal strength bars

    # Display SSID and additional message
    draw.text((0, 0), f"SSID: ", font=font, fill=255)
    
    # Scrolling text for SSID
    start_scrolling_text(
        config.data['current_state'],
        config.data['current_index'],
        f"{ssid}",
        (width - (draw.textlength("SSID: "))),
        (draw.textlength("SSID: ")),
        0
    )

def no_networks_view():
    """Display the no networks view."""
    text1 = "NO MOTHERS"
    text2 = "DETECTED"
    text3 = "Push to refresh"
    draw.text((center_text(text1), 0), text1, font=font, fill=255)
    draw.text((center_text(text2), 10), text2, font=font, fill=255)
    draw.text((center_text(text3), 20), text3, font=font, fill=255)