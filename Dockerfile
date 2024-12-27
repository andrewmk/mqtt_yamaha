FROM python:3.9-alpine
RUN pip install mqtt-client
RUN apk add --no-cache curl grep
ADD yamaha.py input-hdmi1.sh input-hdmi2.sh input-hdmi3.sh input-hdmi4.sh vol-up.sh vol-down.sh vol-mute-on.sh vol-mute-off.sh .
CMD ["python", "./yamaha.py"] 
