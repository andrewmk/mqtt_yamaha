FROM python:3.9-alpine
RUN pip install mqtt-client
ADD yamaha.py yamaharemote.py .
CMD ["python", "./yamaha.py"] 
