#------------------------------------------------------
# GardenaValveControl
# Version 1.1
# Author: Christian Korff
# email: ckorff@web.de
#------------------------------------------------------

from mqtt import MQTTClient
from machine import Pin
from machine import WDT
import usyslog

#------------------------------------------------------
# Initialize Syslog Server & send boot message
#------------------------------------------------------
SYSLOG_SERVER_IP = '192.168.1.150'
s = usyslog.UDPClient(ip=SYSLOG_SERVER_IP)
s.info('GardenaValveControl:Booting Version 1.1')

#------------------------------------------------------
# Declare global variable
#------------------------------------------------------
valve_status = ""
valve_desired_status = b'OFF'

#------------------------------------------------------
# Declare physical pin's
#------------------------------------------------------
p_ON = Pin('P6', mode=Pin.OUT, pull=Pin.PULL_UP)
p_OFF = Pin('P7', mode=Pin.OUT, pull=Pin.PULL_UP)
p_ON.value(0)
p_OFF.value(0)

#------------------------------------------------------
# MQTT subroutine to handle incoming messages
# on subscribed topics
#------------------------------------------------------
def sub_cb(topic, msg):
   global valve_desired_status
   valve_desired_status = (msg)


#------------------------------------------------------
# Subroutine to open valve
#------------------------------------------------------
def sub_open_valve():
    global valve_status
    p_ON.value(1)
    pycom.rgbled(0x00FF00)
    time.sleep(0.250)
    p_ON.value(0)
    pycom.rgbled(0x000000)
    valve_status = b'ON'

#------------------------------------------------------
# Subroutine to close valve
#------------------------------------------------------
def sub_close_valve():
    global valve_status
    p_OFF.value(1)
    pycom.rgbled(0xFF0000)
    time.sleep(0.0625)
    p_OFF.value(0)
    pycom.rgbled(0x000000)
    valve_status = b'OFF'

#------------------------------------------------------
# Initialize watchdog counter to ensure stability
#------------------------------------------------------
wdt = WDT(timeout=2000)  # enable it with a timeout of 2 second

#------------------------------------------------------
# Initialize MQTT client and subscribe to Cmd topic
#------------------------------------------------------
client = MQTTClient("PyComGardena", "192.168.1.151",port=1883)
client.set_callback(sub_cb)
client.connect()
client.subscribe(topic="/Keller/PyComGardena/Cmd")
client.publish(topic="/Keller/PyComGardena/Cmd", msg=b'OFF', retain=True, qos=1)

#------------------------------------------------------
# Starting main program
#------------------------------------------------------
while True:
    loop_counter = 1
    while loop_counter <= 20:
        client.check_msg()
        if valve_status != valve_desired_status:
            if valve_desired_status == b'ON': sub_open_valve()
            if valve_desired_status == b'OFF': sub_close_valve()

        if loop_counter == 1:
            client.publish(topic="/Keller/PyComGardena/Status", msg=valve_status)
            pycom.rgbled(0x000011)
        if loop_counter == 11:
            pycom.rgbled(0x000000)
        loop_counter +=1
        wdt.feed()
        time.sleep(0.1)
