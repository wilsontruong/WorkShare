#Do pip install websocket-client

import socketio
import time

beepDistance = 10
sio = socketio.Client()
sio.connect('http://"ENTER_IP":3000')

@sio.event
def distanceUpdate(data):
    global beepDistance
    beepDistance = data

def sensorCheck():
    ## background task that runs while not recieving data
    while True:
        global beepDistance
        sio.emit('sensorUpdate', beepDistance)
        time.sleep(1)

task = sio.start_background_task(sensorCheck)