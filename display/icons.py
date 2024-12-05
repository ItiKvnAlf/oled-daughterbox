import display.config as config
from display.config import draw, width, height

def set_icon_bottom_right(direction: str, size: int = 2, circle_radius: int = 2, distance_from_circle: int = 7):
    """
    Set the icon on the OLED display based on the direction.
    Args:
        direction: The direction for the icon (up, down, left, right, middle).
        size: The size of the icon (default: 2).
        circle_radius: The radius of the circle for the 'middle' direction (default: 2).
        distance_from_circle: The distance of the triangle from the circle (default: 7).
    """
    # Define the base coordinates for the icon
    base_x = width - 8
    base_y = height - 8

    if direction == 'middle':
        # Draw a circle at the center for 'middle' direction
        icon = [(base_x - circle_radius, base_y - circle_radius),
                (base_x + circle_radius, base_y + circle_radius)]
        draw.ellipse(icon, fill=255)
    else:
        # Define the triangle points based on the direction
        direction_offsets = {
            'up':   (0, -1, 1, 0),    # Move up along Y
            'down': (0, 1, 1, 0),     # Move down along Y
            'left': (-1, 0, 0, 1),    # Move left along X
            'right': (1, 0, 0, 1)     # Move right along X
        }

        # Get the direction offsets
        dx, dy, size_x, size_y = direction_offsets[direction]
         
        # Define the triangle points
        icon = [
            (base_x + dx * distance_from_circle, base_y + dy * distance_from_circle),  # Top point
            (base_x + dx * (distance_from_circle - size) - size_x * size, base_y + dy * (distance_from_circle - size) - size_y * size),  # Bottom-left point
            (base_x + dx * (distance_from_circle - size) + size_x * size, base_y + dy * (distance_from_circle - size) + size_y * size)   # Bottom-right point
        ]
        
        # Draw the triangle
        draw.polygon(icon, fill=255)

def set_icon_center(direction: str):
    """
    Set the icon in the center of the OLED display based on the direction.
    Args:
        direction: The direction for the icon (up, down, left, right, middle).
    """
    width_icon = width // 2 + 10
    height_icon = height // 2

    if direction == 'middle':
        # Center icon is a little circle
        center_icon = [(width_icon - 2, height_icon - 2), (width_icon + 2, height_icon + 2)]
        draw.ellipse(center_icon, fill=255)
    elif direction == 'up':
        up_icon = [(width_icon - 2, height_icon - 6), (width_icon, height_icon - 8), (width_icon + 2, height_icon - 6)]
        draw.polygon(up_icon, fill=255)
    elif direction == 'down':
        down_icon = [(width_icon - 2, height_icon + 6), (width_icon, height_icon + 8), (width_icon + 2, height_icon + 6)]
        draw.polygon(down_icon, fill=255)
    elif direction == 'left':
        left_icon = [(width_icon - 8, height_icon), (width_icon - 6, height_icon - 2), (width_icon - 6, height_icon + 2)]
        draw.polygon(left_icon, fill=255)
    elif direction == 'right':
        right_icon = [(width_icon + 8, height_icon), (width_icon + 6, height_icon - 2), (width_icon + 6, height_icon + 2)]
        draw.polygon(right_icon, fill=255)

def draw_icons_bottom_right():
    """
    Draw the icons on the bottom right of the OLED display based on the current state.
    """
    current_state = config.data['current_state']
    # Draw up, down, left, right triangles and the circle based on current state
    if current_state == "menu":  # Main Page
        set_icon_bottom_right('down')
        set_icon_bottom_right('right')
        set_icon_bottom_right('middle')

    elif current_state == "info_db":  # DAUGHTER BOX information
        set_icon_bottom_right('left')
        set_icon_bottom_right('right')

    elif current_state == "info_db_wlan_ip" or current_state == "db_webpage_info":  # DAUGHTER BOX Webpage access information
        set_icon_bottom_right('up')

    elif current_state == "info_mh":  # Linked MOTHER HUB information
        set_icon_bottom_right('left')
        set_icon_bottom_right('middle')
        set_icon_bottom_right('down')
    
    elif current_state == "unlinked":  # Unlinked from MOTHER HUB
        set_icon_bottom_right('middle')

    elif current_state == "no_networks":  # No Networks Detected
        set_icon_bottom_right('up')
        set_icon_bottom_right('middle')

    elif current_state == "networks_info":  # Networks
        set_icon_bottom_right('up')
        set_icon_bottom_right('down')
        set_icon_bottom_right('middle')

    elif current_state == "networks_detected":  # Cameras
        set_icon_bottom_right('up')
        set_icon_bottom_right('middle')
        if len(config.data['networks']) > 1:
            set_icon_bottom_right('left')
            set_icon_bottom_right('right')

    elif current_state == "link_success" or current_state == "incorrect_password" or current_state == "no_router" or current_state == "no_ssid_found" or current_state == "failed_linking" or current_state == "same_ip" or current_state == "ip_applied":
        set_icon_bottom_right('middle') 

def draw_rssi_bars(rssi: int):
    """
    Draws a bar chart with 5 bars on an OLED screen based on an RSSI value in the range [0, 100].

    Args:
        rssi (int): RSSI value [0-100]
    """
    num_bars = 5

    # Bar dimensions
    bar_width = 1
    spacing = 2
    start_x = width - (num_bars * (bar_width + spacing)) - 18
    bottom_y = height

     # Heights of the bars (increasing height for each bar)
    bar_heights = [3, 7, 11, 15, 19] 

    # Clamp the RSSI value to the range [0, 100]
    rssi_clamped = max(0, min(rssi, 100))

    # Determine how many bars should be displayed based on the RSSI value
    max_active_bars = int((rssi_clamped / 100) * num_bars)

    # Draw the bars
    for i in range(num_bars):
        if i < max_active_bars:  # Only draw active bars
            x1 = start_x + i * (bar_width + spacing)
            y1 = bottom_y - bar_heights[i]
            x2 = x1 + bar_width
            y2 = bottom_y
            draw.rectangle([x1, y1, x2, y2], fill=255)