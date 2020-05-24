#------------------------------------------------------
# GardenaValveControl
# Version 2.0
# Author: Christian Korff
# email: ckorff@web.de
#------------------------------------------------------
import machine
from machine import Pin
from machine import WDT
from machine import Timer
import os
import pycom
import ubinascii
import usyslog
import ujson
from network import WLAN
from mqtt import MQTTClient
import time
import gc 

pycom.heartbeat(False)


#------------------------------------------------------
# Get config.json into python dictonary GardenaValveConfig
#------------------------------------------------------
with open('config.json', 'r') as myfile:
    ConfigData=myfile.read() #read config.json file

ConfigData = ujson.loads(ConfigData) #convert json in Python dictionary all properties stored in ConfigData

#------------------------------------------------------
# Get physical device adress and define unique MQTT name
#------------------------------------------------------
DeviceID = ubinascii.hexlify(machine.unique_id())
DeviceID = DeviceID.decode('utf-8')
MQTTDeviceID = 'PyComGardena{}'.format(DeviceID)
print ('MQTTDeviceID = {}'.format( MQTTDeviceID))

#------------------------------------------------------
# Connect to WLAN either with fixed IP in config.json or DHCP
#------------------------------------------------------
try:
    DeviceIP = ConfigData['Devices'][DeviceID]
    print ('DeviceIP = {}'.format( DeviceIP))
    WLANconfig = (DeviceIP, ConfigData['subnet_mask'], ConfigData['gateway'], ConfigData['DNS_server'])
except KeyError:
    print("Device IP not configured revert to DHCP")
    WLANconfig = 'dhcp'

wlan = WLAN() # get current object, without changing the mode

if machine.reset_cause() != machine.SOFT_RESET:
    wlan.init(mode=WLAN.STA)
    # configuration below MUST match your home router settings!!
    wlan.ifconfig(config=WLANconfig)

if not wlan.isconnected():
    # change the line below to match your network ssid, security and password
    wlan.connect(ConfigData['SSID'], auth=(WLAN.WPA2, ConfigData['WLANPSWD']), timeout=5000)
    while not wlan.isconnected():
        machine.idle() # save power while waiting

print("Connected to WiFi\n")
print(wlan.ifconfig())

#------------------------------------------------------
# Initialize Syslog Server & send boot message
#------------------------------------------------------
#s = usyslog.UDPClient(ip=ConfigData['SYSLOG_SERVER_IP'])
#s.info('GardenaValveControl:Booting Version 1.1')