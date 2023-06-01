import requests
import json
import eventlet
import socketio
import RPi.GPIO as GPIO
import time
import subprocess

distance = 10 #distance in cm
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, static_files={
  '/': {'content_type': 'text/html', 'filename': 'index.html'} #default page send to clients with JS that connects to socketio instance
})
@sio.event
def connect(sid, environ):
  print('connected', sid)

def measureDistance():
  # Set up GPIO mode
  GPIO.setmode(GPIO.BCM)

  # Define GPIO pins for ultrasonic sensor
  TRIG = 23
  ECHO = 24

  print("Distance Measurement In Progress")

  # Set TRIG pin as output and ECHO pin as input
  GPIO.setup(TRIG, GPIO.OUT)
  GPIO.setup(ECHO, GPIO.IN)

  GPIO.output(TRIG, False)
  print("Waiting For Sensor")

  # Trigger ultrasonic sensor by setting TRIG pin to True for a short duration
  GPIO.output(TRIG, True)
  time.sleep(0.00001)
  GPIO.output(TRIG, False)

  # Measure time for ultrasonic pulse to travel to the target and back
  while GPIO.input(ECHO) == 0:
    pulseStart = time.time()
  while GPIO.input(ECHO) == 1:
    pulseEnd = time.time()
  pulseDuration = pulseEnd - pulseStart

  # Calculate distance based on the pulse duration
  distance = pulseDuration * 17150
  distance = round(distance, 2)
  print("Distance:", distance, "cm")

  # Clean up GPIO
  GPIO.cleanup()

  return distance

#Gets the constantly running sensor call and sends out the current distance measured from the device.
@sio.event
def sensorUpdate(sid, data):
  #send all the data to the connected clients
  x = measureDistance()
  sio.emit("deviceUpdate", x)

#Receives the updated distance from the client and sends it back to the client (weird, but it just works this way)
@sio.event
def updateDistance(sid, data):
    sio.emit("distanceUpdate",float(data))

if __name__ == '__main__':
  eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 3000)), app)