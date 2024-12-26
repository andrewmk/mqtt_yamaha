#!/bin/sh

YAMVOL=`curl -s -d "<YAMAHA_AV cmd=\"GET\"><Main_Zone><Basic_Status>GetParam</Basic_Status></Main_Zone></YAMAHA_AV>" http://yamaha-amp.local/YamahaRemoteControl/ctrl | grep -P -o "(?<=<Volume><Lvl><Val>).*?(?=</Val>)"`
YAMVOL=$(($YAMVOL-10))
curl -s -d "<YAMAHA_AV cmd=\"PUT\"><Main_Zone><Volume><Lvl><Val>$YAMVOL</Val><Exp>1</Exp><Unit>dB</Unit></Lvl></Volume></Main_Zone></YAMAHA_AV>" http://yamaha-amp.local/YamahaRemoteControl/ctrl
