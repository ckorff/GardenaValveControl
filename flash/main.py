from gardenavalvecontrol import valve

#------------------------------------------------------
# Initialize Valve 1 as GardenaValve1
#------------------------------------------------------
GardenaValve1 = valve(PinON = 'P7', PinOFF = 'P6')
GardenaValve2 = valve(PinON = 'P5', PinOFF = 'P4')

#------------------------------------------------------
# Define global variables
#------------------------------------------------------
SecondInterruptHappened = False

#------------------------------------------------------
# Initialize and configure subroutine for 1 second timer
#------------------------------------------------------
def seconds_handler(alarm):
   global SecondInterruptHappened
   SecondInterruptHappened = True   

#------------------------------------------------------
# Instantiate object for Second Timer
#------------------------------------------------------
everySecond = Timer.Alarm(seconds_handler, 1, periodic=True)
        
#------------------------------------------------------
# MQTT subroutine to handle incoming messages
# on subscribed topics
#------------------------------------------------------
def sub_cb(topic, msg):
    print('MQTT empfangen')
    try:
        receivedMessage = ujson.loads(msg)
        if str(receivedMessage['device']) == DeviceID:
            receivedMessage['valve'] = int(receivedMessage['valve'])
            receivedMessage['status'] = bool(receivedMessage['status'])
            if receivedMessage['valve'] == 1:
                GardenaValve1.setValveStatus(receivedMessage['status'])
                GardenaValve1.set_needUpdate(True)
            if receivedMessage['valve'] == 2:
                GardenaValve2.setValveStatus(receivedMessage['status'])
                GardenaValve2.set_needUpdate(True)
            return
        else:
            print('not for me')
            return
    except:
        print('wrong message format received')
        print(msg)
        return
    
#------------------------------------------------------
# Initialize watchdog counter to ensure stability
#------------------------------------------------------
wdt = WDT(timeout=2000)  # enable it with a timeout of 2 second

#------------------------------------------------------
# Initialize MQTT client and subscribe to Cmd topic
#------------------------------------------------------
MQTT_Server = ConfigData['MQTT_Server']
MQTT_Port = int(ConfigData['MQTT_Port'])
MQTT_Status_Topic = ConfigData['MQTT_Status_Topic']
MQTT_CMD_Topic = ConfigData['MQTT_CMD_Topic']

client = MQTTClient(MQTTDeviceID, MQTT_Server,port=MQTT_Port, user=None, password=None, keepalive=30, ssl=False, ssl_params={})
client.set_callback(sub_cb)
client.connect()

#------------------------------------------------------
# Publish retain "off" message & subscribe to CMD topic
#------------------------------------------------------
msg = {
        'device': '30aea478eb20',
        'valve': '1',
        'status': False
       }

client.publish(MQTT_CMD_Topic, ujson.dumps(msg), retain=True, qos=1)
client.subscribe(MQTT_CMD_Topic)

#------------------------------------------------------
# Starting main program
#------------------------------------------------------
while 1:
    # construct MQTT status message
    MQTTstatusMessage = {
                            'valve1': GardenaValve1.getValveStatus(),
                            'valve2': GardenaValve2.getValveStatus(),
                            'device': DeviceID
                        }
    
    # run code if any valve status needs to be updated
    if GardenaValve1.get_needUpdate() == True:
        GardenaValve1.updateValve()
        client.publish(MQTT_Status_Topic, ujson.dumps(MQTTstatusMessage))

    if GardenaValve2.get_needUpdate() == True:
        GardenaValve2.updateValve()
        client.publish(MQTT_Status_Topic, ujson.dumps(MQTTstatusMessage))
    
    # run code every second
    if SecondInterruptHappened == True:
        if GardenaValve1.get_statusColor() == 0:
            if GardenaValve1.getValveStatus() == True:
                GardenaValve1.set_statusColor(0x001100)
            else:
                GardenaValve1.set_statusColor(0x110000)
        else:
            GardenaValve1.set_statusColor(0)
        pycom.rgbled(GardenaValve1.get_statusColor())
        client.publish(MQTT_Status_Topic, ujson.dumps(MQTTstatusMessage))
        SecondInterruptHappened = False
    
    gc.collect()        # collect garbage to safe heap memory
    wdt.feed()          # feed watchdog timer for resiliancy; reboot if not done within 2 seconds
    client.check_msg()  #check for incoming MQTT messages
    time.sleep(0.1)