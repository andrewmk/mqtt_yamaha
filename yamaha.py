# MIT License
#
# Copyright (c) 2020 Oli Wright <oli.wright.github@gmail.com>
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

# skyremote_mqtt.py
#
# MQTT client wrapper for sky remote control 

from skyremote import SkyRemote
import paho.mqtt.client as mqtt
import os

class Sky():
  def __init__(self, ipaddr):
    self.base_topic = "sky"
    self.subscribe_topic = self.base_topic + "/#"
    self.remote_topic = self.base_topic + "/remote"
    self.set_state_topic = self.base_topic + "/set-state"
    self.status_topic = self.base_topic + "/status"
    self.state = "Off"
    self.sky = SkyRemote(ipaddr)

  def publish_status(self, client):
    json = '{{"state":"{state}" }}'.format(state = self.state)
    client.publish(self.status_topic, payload = json, retain = True)

  def set_state(self, state):
    state = state.decode("utf-8")
    print("Setting sky box to " + state)
    if self.state == state:
      return
    if state == "Off":
      self.sky.press("power_off")
      pass
    elif state == "On":
      self.sky.press("power_on")
      pass
    else:
      print("Unknown state: " + state)
    self.state = state

  def on_message(self, client, userdata, message):
    if message.topic == self.remote_topic:
      self.sky.press(message.payload.decode('utf-8'))
    elif message.topic == self.set_state_topic:
      self.set_state(message.payload)
      self.publish_status(client)
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
    self.client.on_message = sky.on_message

  def connect_mqtt(self) -> mqtt:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id)
    client.on_connect = sky.on_connect
    client.connect(broker, port)
    return client

  def run(self):
    self.client = sky.connect_mqtt()
    self.client.loop_forever()

if __name__ == '__main__':
  SKYBOX_IP = os.getenv('SKYBOX_IP')
  MOSQUITTO_IP = os.getenv('MOSQUITTO_IP')
  MOSQUITTO_PORT = int(os.getenv('MOSQUITTO_PORT'))
  sky = Sky(SKYBOX_IP)
  broker = MOSQUITTO_IP
  port = MOSQUITTO_PORT
  topic = sky.subscribe_topic
  client_id = 'mqtt_sky'
  sky.run()
