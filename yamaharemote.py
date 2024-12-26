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

# skyremote.py
#
# Python version of https://github.com/dalhundal/sky-remote/blob/master/sky-remote.js
# Allows IP remote-control of Sky HD and Sky Q boxes.

import socket

codes = {
	"power": 0,
	"select": 1,
	"backup": 2,
	"dismiss": 2,
	"channelup": 6,
	"channeldown": 7,
	"interactive": 8,
	"sidebar": 8,
	"help": 9,
	"services": 10,
	"search": 10,
	"tvguide": 11,
	"home": 11,
	"i": 14,
	"text": 15, 
	"up": 16,
	"down": 17,
	"left": 18,
	"right": 19,
	"red": 32,
	"green": 33,
	"yellow": 34,
	"blue": 35,
	"0": 48,
	"1": 49,
	"2": 50,
	"3": 51,
	"4": 52,
	"5": 53,
	"6": 54,
	"7": 55,
	"8": 56,
	"9": 57,
	"play": 64,
	"pause": 65,
	"stop": 66,
	"record": 67,
	"fastforward": 69,
	"rewind": 71,
	"boxoffice": 240,
	"sky": 241
}

# Commands that translate into multiple button presses
meta_commands = {
	"power_on": ["sky"],
	"power_off": ["sky", "power"],
	"planner" : ["tvguide", "green"],
	"subtitles" : ["help", "down", "right", "select"],
	"channel" : ["sky"], # Prefix to send before entering a channel number
	"bbc1": ["channel", 115],
}

class SkyRemote():
	def __init__(self, ipaddr):
		self.ipaddr = ipaddr
		self.connect()

	def connect(self):
		self.connected = False
		try:
			self.socket = socket.socket()
			self.socket.connect((self.ipaddr, 49160))

			# Strange dance to initialise the connection
			print("Initialising connection to Sky+ HD box " + self.ipaddr)
			l = 12
			while True:
				received = self.socket.recv(31)
				if len(received) < 24:
					self.socket.send(received[0:l])
					l = 1
					print("Received {0} ({1}bytes), echoed {2}".format(received, len(received), l))
				else:
					break
			self.connected = True
		except:
			print("Error trying to connect to Sky box")

	def press(self, command):
		if command is None:
			return

		if not self.connected:
			self.connect()
			if not self.connected:
				print("Unable to send message to Sky box")
				return

		# Figure out what to do based on the type of 'command'
		command_type = type(command)
		if command_type is int:
			# Send an integer number as a series of numeric keypresses
			value = command
			num_digits = len(str(value))
			units = 1
			for i in range(num_digits - 1):
				units = units * 10
			while units != 0:
				digit = value // units
				value -= (digit * units)
				units = units // 10
				self.press(str(digit))
		elif command_type is list:
			# Send each entry in the list as its own command
			for button in command:
				self.press(button)
		elif command_type is str:
			# Is this a meta-command, or a single button press?
			global meta_commands
			meta_command = meta_commands.get(command, None)
			if meta_command is not None:
				self.press(meta_command)
			elif command == "reconnect":
				self.connect()
			else:
				# Now we can assume that the string command is an actual button
				global codes
				code = codes.get(command, None)
				if code is None:
					print("Unknown button: " + command)
					return

				print("Pressing " + command)
				command_bytes = bytearray([4,1,0,0,0,0, 224 + (code >> 4), code & 15]);
				try:
					sent = self.socket.send(command_bytes)
				except:
					print("Exception sending message to Sky box")
					# Try again
					self.connect()
					if self.connected:
						try:
							sent = self.socket.send(command_bytes)
						except:
							print("Giving up")
							self.connected = False
							return

				# We just succeeded, so let's just assume this will work too
				command_bytes[1] = 0;
				sent = self.socket.send(command_bytes)
		else:
			print("Unknown command type: " + str(command_type))

if __name__ == '__main__':
	# Example usage...
	sky = SkyRemote("192.168.1.194")
	sky.press("sky")
	sky.press("tvguide")
