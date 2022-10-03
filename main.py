# Copyright (c) 2020, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
# See https://docs.pycom.io for more information regarding library specif


import machine
import time
import pycom
import struct
import socket
import ubinascii
from network import WLAN
from machine import RTC
from pycoproc_1 import Pycoproc
from LTR329ALS01 import LTR329ALS01
from LIS2HH12 import LIS2HH12

import config
import json
from mqtt import MQTTClient
from MQTTLib import AWSIoTMQTTShadowClient
from MQTTLib import AWSIoTMQTTClient

from network import MDNS
MDNS.init()
MDNS.set_name(hostname ="pycom", instance_name="pycom")
MDNS.add_service("_http",MDNS.PROTO_TCP, 80)
MDNS.add_service("_telnetd", MDNS.PROTO_TCP, 23)


# Make sure heartbeat is disabled before setting RGB LED
pycom.heartbeat(False)
pycom.rgbled(0x0000FF) # Blue

RGB_BRIGHTNESS = 0x8

RGB_RED = (RGB_BRIGHTNESS << 16)
RGB_GREEN = (RGB_BRIGHTNESS << 8)
RGB_BLUE = (RGB_BRIGHTNESS)

pyscan = Pycoproc(Pycoproc.PYSCAN)


# Connect to wifi to get time
wlan = WLAN(mode=WLAN.STA)
wlan.connect(config.WIFI_SSID, auth=(None, config.WIFI_PASS), timeout=5000)
while not wlan.isconnected():
    time.sleep(2)
time.sleep(2)
print('\n')
print('WiFi connected succesfully to: ', config.WIFI_SSID)
print(wlan.ifconfig()) # Print IP configuration
pycom.rgbled(0xFFFF00) # Yellow
time.sleep(5)


# setup rtc
rtc = machine.RTC()
rtc.ntp_sync('pool.ntp.org')
time.sleep(0.75)
print('\nRTC Set from NTP to UTC:', rtc.now())
time.timezone(-14200)
print('Adjusted from UTC to EST timezone', time.localtime(), '\n')
print("Local time: ", time.localtime())
a = rtc.synced()
print('RTC is synced to "pool.ntp.org": ', a)

def settimeout(duration): 
    pass

def sub_cb(topic, msg):
   print(msg)

# # user specified callback function
# def customCallback(client, userdata, message):
# 	print("Received a new message: ")
# 	print(message.payload)
# 	print("from topic: ")
 
# 	print(message.topic)
# 	print("--------------\n\n")
 

# configure the MQTT client
pycomAwsMQTTClient = AWSIoTMQTTClient(config.CLIENT_ID)
pycomAwsMQTTClient.configureEndpoint(config.AWS_HOST, config.AWS_PORT)
pycomAwsMQTTClient.configureCredentials(config.AWS_ROOT_CA, config.AWS_PRIVATE_KEY, config.AWS_CLIENT_CERT)

pycomAwsMQTTClient.configureOfflinePublishQueueing(config.OFFLINE_QUEUE_SIZE)
pycomAwsMQTTClient.configureDrainingFrequency(config.DRAINING_FREQ)
pycomAwsMQTTClient.configureConnectDisconnectTimeout(config.CONN_DISCONN_TIMEOUT)
pycomAwsMQTTClient.configureMQTTOperationTimeout(config.MQTT_OPER_TIMEOUT)
pycomAwsMQTTClient.configureLastWill(config.LAST_WILL_TOPIC, config.LAST_WILL_MSG, 1)

pycomAwsMQTTClient.DEBUG = True
# pycomAwsMQTTClient.set_callback(sub_cb)
pycomAwsMQTTClient.settimeout = settimeout
pycomAwsMQTTClient.connect()

# Connect to MQTT Host
if pycomAwsMQTTClient.connect():
    print('\nAWS connection succeeded (MQTT Client)')
    pycom.rgbled(0xFFA500) # Orange

# # Subscribe to topic
# pycomAwsMQTTClient.subscribe(config.TOPIC, 1, customCallback)
# time.sleep(10)

voltage = pyscan.read_battery_voltage() # Read board voltage
ltr329als01 = LTR329ALS01() # Digital Ambient Light Sensor
light = ltr329als01.light()[0] # Lumen
lux = ltr329als01.lux() # Lux
LIGHTMess = str(light)
LUXMess = str(lux)

lis2hh12 = LIS2HH12() # 3-Axis Accelerometer
acceleration = lis2hh12.acceleration()
acceleration_x = lis2hh12.acceleration_x() # Axis x
acceleration_y = lis2hh12.acceleration_y() # Axis y
acceleration_z = lis2hh12.acceleration_z() # Axis z
roll = lis2hh12.roll() # Roll
pitch = lis2hh12.pitch() # Pitch

# Send message to host
while True:
    # user specified callback function
    def customCallback(client, userdata, message):
        print('Received a new message: ')
        print(message.payload)
        print('From topic: ', config.TOPIC_1) # Subscribe topic
        print(message.topic)
        print('--------------\n\n')
        
    # Read sensor data
    print('\nVoltage: {}, Lumen: {}, Lux: {}'.format(voltage, light, lux))
    print('\nRoll: {}, Pitch: {}, Acceleration: {}'.format(roll, pitch, acceleration))
    print('\nAcceleration x: {}, Acceleration y: {}, Acceleration z: {}'.format(acceleration_x, acceleration_y, acceleration_z))
    print('\nSending Voltage: ', voltage)
    print('Sending lumen: ', LIGHTMess)
    print('Sending Lux: ', LUXMess)
    print('Sending Acceleration: ', acceleration)
    print('Sending Roll: ', roll)
    print('Sending Pitch: ', pitch)
    pycom.rgbled(0x00FF00) # Green
    
    # Publisg to topic
    pycomAwsMQTTClient.publish(config.TOPIC, str(voltage), 1)
    pycomAwsMQTTClient.publish(config.TOPIC, str(LIGHTMess), 1)
    pycomAwsMQTTClient.publish(config.TOPIC, str(LUXMess), 1)
    pycomAwsMQTTClient.publish(config.TOPIC, str(acceleration_x), 1)
    pycomAwsMQTTClient.publish(config.TOPIC, str(acceleration_y), 1)
    pycomAwsMQTTClient.publish(config.TOPIC, str(acceleration_z), 1)
    pycomAwsMQTTClient.publish(config.TOPIC, str(roll), 1)
    pycomAwsMQTTClient.publish(config.TOPIC, str(pitch), 1)

    time.sleep(10)  
    print('\nSleeping for 10 secs')
    
    # Subscribe to topic
    pycomAwsMQTTClient.subscribe(config.TOPIC_1, 1, customCallback)
    pycom.rgbled(0xFF0000) # Red
    time.sleep(10)
    print('\nSleeping for 10 secs')

