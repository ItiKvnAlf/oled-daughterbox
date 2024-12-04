from board import SCL, SDA # type: ignore
import busio # type: ignore
import adafruit_ssd1306 # type: ignore
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO # type: ignore

# Create the I2C interface and SSD1306 OLED class.
i2c = busio.I2C(SCL, SDA)
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear display.
disp.rotation = 2
disp.fill(0)
disp.show()

# Create blank image for drawing.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# Global data
data = {
    'current_state': "menu",
    'current_index': 0,
    'selected_digit_index': 0,
    'selected_button': 0,
    'selected_confirm_button': 0,
    'db': {'ip': None, 'wlan_ip': None, 'mask': None, 'name': None, },
    'mh': {'ssid': None, 'rssi': None},
    'selected_hub': {},
    'networks': [],
    'known_networks': [],
    'linked_networks': [],
    'temp_ip': "",
    'temp_netmask': "",
    'temp_password': [0] * 8,
    'prev_m_btn_state': GPIO.HIGH,
    'm_btn_pressed': False,
    'system_config_options': ["CHANGE IP", "REBOOT", "SHUTDOWN", "MH MODE"],
}
