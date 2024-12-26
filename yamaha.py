# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# yamaha.py
#
# MQTT client wrapper for Yamaha AVR remote control 

import paho.mqtt.client as mqtt
import os
from subprocess import call

class Yamaha():
  def __init__(self, ipaddr):
    self.base_topic = "yamaha"
    self.subscribe_topic = self.base_topic + "/#"
    self.remote_topic = self.base_topic + "/remote"
    self.set_state_topic = self.base_topic + "/set-state"
    self.status_topic = self.base_topic + "/status"
    self.state = "Off"

  def publish_status(self, client):
    json = '{{"state":"{state}" }}'.format(state = self.state)
    client.publish(self.status_topic, payload = json, retain = True)

  def on_message(self, client, userdata, message):
    if message.topic == self.remote_topic:
      rc = call("./" + message.payload.decode('utf-8') + ".sh")
    elif message.topic == self.status_topic:
      pass
    else:
      print("Unknown topic: " + message.topic)

  def on_connect(self, client, userdata, flags, rc):
    if rc == 0:
      print("Connected to MQTT Broker!")
      self.subscribe(self.client)
      self.publish_status(self.client)
    else:
      print("Failed to connect, return code %d\n", rc)
    
  def subscribe(self, client: mqtt):
    self.client.subscribe(topic)
    self.client.on_message = yamaha.on_message

  def connect_mqtt(self) -> mqtt:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id)
    client.on_connect = yamaha.on_connect
    client.connect(broker, port)
    return client

  def run(self):
    self.client = yamaha.connect_mqtt()
    self.client.loop_forever()

if __name__ == '__main__':
  YAMAHA_IP = os.getenv('YAMAHA_IP')
  MOSQUITTO_IP = os.getenv('MOSQUITTO_IP')
  MOSQUITTO_PORT = int(os.getenv('MOSQUITTO_PORT'))
  broker = MOSQUITTO_IP
  port = MOSQUITTO_PORT
  yamaha = Yamaha(YAMAHA_IP)
  topic = yamaha.subscribe_topic
  client_id = 'mqtt_yamaha'
  yamaha.run()
