#!/bin/sh

curl -s -d "<YAMAHA_AV cmd=\"PUT\"><Main_Zone><Input><Input_Sel>HDMI4</Input_Sel></Input></Main_Zone></YAMAHA_AV>" http://yamaha-amp.local/YamahaRemoteControl/ctrl
