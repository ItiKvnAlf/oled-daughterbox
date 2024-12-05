ETHERNET_INTERFACE = 'eth0'
WIRELESS_INTERFACE = 'wlan0'

ETHERNET_CONNECTION = 'ETH'

DEVICE_MODE_FILE_PATH = '/home/capstone/mode'

REBOOT_SYSTEM = "sudo reboot"
SHUTDOWN_SYSTEM = "sudo shutdown now"

NMCLI_CONNECTION_UP = "nmcli connection up {}"
NMCLI_GET_IP4_ADDRESS = "nmcli -f ipv4.addresses connection show {}"
NMCLI_SET_IP4_ADDRESS = "nmcli connection modify {} ipv4.addresses {}/{} ipv4.method manual"
NMCLI_GET_IP4_ADDRESS_WIRELESS = "nmcli device show {}"
NMCLI_SCAN_WIFI_NETWORKS = "nmcli -t -f ACTIVE,SSID,SIGNAL device wifi"
NMCLI_REFRESH = "nmcli -t device wifi"
NMCLI_GET_WIFI_CONNECTIONS = "nmcli -t -f NAME connection show"
NMCLI_LINK_TO_NEW_AP = "nmcli dev wifi connect '{}' password '{}'"
NMCLI_LINK_TO_KNOWN_WIFI_CONNECTION = "nmcli connection up '{}'"
NMCLI_UNLINK_FROM_WIFI_CONNECTION = "nmcli connection down '{}'"
NMCLI_DELETE_KNOWN_WIFI_CONNECTION = "nmcli connection delete {}"
NMCLI_GET_AUTOCONNECT = "nmcli -f connection.autoconnect connection show '{}'"
NMCLI_SET_AUTOCONNECT_TO_WIFI_CONNECTION = "nmcli connection modify '{}' connection.autoconnect {}"
