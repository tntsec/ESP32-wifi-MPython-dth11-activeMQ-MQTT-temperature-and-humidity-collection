import random
from machine import Pin, SPI
import time,machine
import dht11,network,mrequests
from umqtt.simple import MQTTClient
import ujson

MQTT_CLIENT_ID = f'python-mqtt-{random.randint(0, 1000)}'
MQTT_BROKER    = "10.0.10.129"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = "mqtt001"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
  
dht = dht11.DHT11(Pin(13))

print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)

print("Connected!")

while True:
    if wlan.isconnected() == False:
        print("connect WiFi")
        try:
            wlan.connect('WiFissid','wifipassword')
        except:
            print("wifi false")
            #pass
    else:
        dht.measure()
        try:
            client.connect()
            message = ujson.dumps({
    "temp": dht.temperature(),
    "humidity": dht.humidity(),
  })
            #print("Reporting to MQTT topic {}: {}".format(MQTT_TOPIC, message))
            client.publish(MQTT_TOPIC, message)
            print("mqtt push ok")
            client.disconnect()
        except:
            print("mqtt push not ok")
            #pass
        time.sleep(3)
