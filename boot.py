import machine
from network import WLAN
import pycom
import time

pycom.heartbeat(False)

wlan = WLAN() # get current object, without changing the mode

if machine.reset_cause() != machine.SOFT_RESET:
    wlan.init(mode=WLAN.STA)
    # configuration below MUST match your home router settings!!
    wlan.ifconfig(config=('192.168.1.205', '255.255.255.0', '192.168.1.1', '192.168.1.1'))

if not wlan.isconnected():
    # change the line below to match your network ssid, security and password
    wlan.connect('your_ssid', auth=(WLAN.WPA2, 'your_password'), timeout=5000)
    while not wlan.isconnected():
        machine.idle() # save power while waiting

print("Connected to WiFi\n")
