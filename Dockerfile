FROM python:3.9-alpine
RUN pip install mqtt-client
RUN apk add --no-cache curl grep
ADD yamaha.py vol-up.sh vol-down.sh vol-mute-on.sh vol-mute-off.sh .
CMD ["python", "./yamaha.py"] 
