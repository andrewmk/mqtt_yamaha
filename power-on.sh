#!/bin/sh

curl -s -d "<YAMAHA_AV cmd=\"PUT\"><Main_Zone><Power_Control><Power>On</Power></Power_Control></Main_Zone></YAMAHA_AV>" http://yamaha-amp.local/YamahaRemoteControl/ctrl
