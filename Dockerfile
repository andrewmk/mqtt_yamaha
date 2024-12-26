FROM python:3.9-alpine
RUN pip install mqtt-client
ADD yamaha.py yamaharemote.py vol-up.sh vol-down.sh vol-mute-on.sh vol-mute-off.sh .
CMD ["python", "./yamaha.py"] 
