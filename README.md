Gardena Valve Control
## Overview
Pycom WiPy 3.0 project to control a 9V Gardena valve via MQTT

	- Based on [Pycom WiPy 3.0](https://docs.pycom.io/datasheets/development/wipy3/) (ESP32) running Micropython
	- Listen to MQTT commands
	- Sends status via MQTT
	- Uses h-bridge circuit to generate switching signal for valve

## Description
The German Manufacturing Company [Gardena](https://en.wikipedia.org/wiki/Gardena_(company)) is producing garden equipment including controller based watering systems. The main downside of the entry-level 9V series is the missing remote control capability.
The purpose of the project is to replace the control unit with a 5V powered circuit that connects to WLAN and provides MQTT connectivity as well as a REST API.
The chosen platform is a WiPy 3.0 from Pycom. The main reason is my personal interest in running a project in Micropython to gain experience in this field.
One of the key objectives has been to not use a 9V  battery nor a special power supply. The idea has been to leverage frequently available 5V MicroUSB as the main power supply. To generate the required 9V the circuit uses a step-up device.
All files (KiCad) will be in the Hardware section including the required datasheets for the components.

## Version 1.0
Initial test release for prototype.
- Running only a single valve
- simplified command structure (pure txt string)
- simplified status update structure (pure txt string)

## Version 2.0
Initial production release
- Drives two independent channels to control two valves
- Desired command structure via JSON
- Desired status structure via JSON

## Version 2.1
Feature upgrade release
- Implements a physical switch to locally toggle the state of each valve

## Version 2.2
- Implements a REST API to control the valves (no authentication)


