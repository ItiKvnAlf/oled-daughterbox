import RPi.GPIO as GPIO # type: ignore
import display.config as config
from navigate.up import navigate_up
from navigate.down import navigate_down
from navigate.left import navigate_left
from navigate.right import navigate_right
from navigate.middle import push_button

def setup_gpio(pin: int):
    """
    Set up a GPIO pin as an input with a pull-up resistor.
    Args:
        pin (int): The pin number to set up.
    """
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def setup_buttons(up_pin: int, down_pin: int, left_pin: int, right_pin: int, middle_pin: int):
    """
    Set up the GPIO pins for the buttons.
    Args:
        up_pin (int): The GPIO pin number for the up button.
        down_pin (int): The GPIO pin number for the down button.
        left_pin (int): The GPIO pin number for the left button.
        right_pin (int): The GPIO pin number for the right button.
        middle_pin (int): The GPIO pin number for the middle button.
    """
    GPIO.setmode(GPIO.BCM)
    setup_gpio(up_pin)
    setup_gpio(down_pin)
    setup_gpio(left_pin)
    setup_gpio(right_pin)
    setup_gpio(middle_pin)

def handle_buttons(up_pin: int, down_pin: int, left_pin: int, right_pin: int, middle_pin: int):
    """
    Handle button presses.
    Args:
        up_pin (int): The GPIO pin number for the up button.
        down_pin (int): The GPIO pin number for the down button.
        left_pin (int): The GPIO pin number for the left button.
        right_pin (int): The GPIO pin number for the right button.
        middle_pin (int): The GPIO pin number for the middle button.
    """
    current_state = config.data['current_state']
    
    if GPIO.input(up_pin) == GPIO.LOW:
        if current_state != "info_mh" and current_state != "info_db":
            navigate_up()
    elif GPIO.input(down_pin) == GPIO.LOW:
        if current_state != "networks_detected" and current_state != "info_db" and current_state != "info_db_wlan_ip":
            navigate_down()
    elif GPIO.input(left_pin) == GPIO.LOW:
        if current_state != "info_db_wlan_ip":
            navigate_left()
    elif GPIO.input(right_pin) == GPIO.LOW:
        if current_state != "info_mh" and current_state != "info_db_wlan_ip":
            navigate_right()
    elif GPIO.input(middle_pin) == GPIO.LOW and config.data['prev_m_btn_state'] == GPIO.HIGH:  # Detect transition
        if current_state != "info_db" and current_state != "info_db_wlan_ip":
            config.data['m_btn_pressed'] = True
            config.data['prev_m_btn_state'] = GPIO.LOW  # Update previous state

    # Check if the middle button has been released
    if config.data['m_btn_pressed']:
        push_button()
        config.data['m_btn_pressed'] = False

    # Update previous state of the middle button
    if GPIO.input(middle_pin) == GPIO.HIGH:
        config.data['prev_m_btn_state'] = GPIO.HIGH
