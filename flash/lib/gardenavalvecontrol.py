from machine import Pin
import pycom
import time

#------------------------------------------------------
# Define Class for Ventil
#------------------------------------------------------
class valve:
    def __init__(self, PinON, PinOFF):
        self._status = False
        self._PinON = Pin(PinON, mode=Pin.OUT, pull=Pin.PULL_UP)
        self._PinOFF = Pin(PinOFF, mode=Pin.OUT, pull=Pin.PULL_UP)
        self._statusColor = (0x000000)
        self._needUpdate = True

    def setValveStatus(self, status):
        self._status = status

    def getValveStatus(self):
        return self._status
    
    def set_needUpdate(self, state = True):
        self._needUpdate = state
    
    def get_needUpdate(self):
        return self._needUpdate
    
    def set_statusColor(self,color):
        self._statusColor = color

    def get_statusColor(self):
        return self._statusColor    
    
    def openValve(self):
        self._PinON.value(1)
        pycom.rgbled(0x00FF00)
        time.sleep(0.250)
        self._PinON.value(0)
        pycom.rgbled(0x001100)

    def closeValve(self):
        self._PinOFF.value(1)
        pycom.rgbled(0xFF0000)
        time.sleep(0.0625)
        self._PinOFF.value(0)
        pycom.rgbled(0x110000)
    
    def updateValve(self):
        if self._status == True:
            self.openValve()
        elif self._status == False:
            self.closeValve()
        self._needUpdate = False
