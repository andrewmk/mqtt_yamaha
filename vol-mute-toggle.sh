#!/bin/sh

YAMMUTE=`curl -s -d "<YAMAHA_AV cmd=\"GET\"><Main_Zone><Basic_Status>GetParam</Basic_Status></Main_Zone></YAMAHA_AV>" http://yamaha-amp.local/YamahaRemoteControl/ctrl | grep -P -o "(?<=</Lvl><Mute>).*?(?=</Mute>)"`

if [ "$YAMMUTE" = "Off" ]; then 
    ./vol-mute-on.sh
else
    ./vol-mute-off.sh
fi;

