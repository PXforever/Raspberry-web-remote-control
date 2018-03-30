#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera_pi import Camera

from flask import Flask, render_template , request
import RPi.GPIO as GPIO 
import time 
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.output(11, GPIO.HIGH)
GPIO.output(13, GPIO.HIGH)
GPIO.output(3, GPIO.LOW)
time.sleep(1)
GPIO.output(3, GPIO.HIGH)
GPIO.output(5, GPIO.LOW)
time.sleep(1)
GPIO.output(5, GPIO.HIGH)
time.sleep(0.1)
GPIO.output(5, GPIO.LOW)
GPIO.output(3, GPIO.LOW)
GPIO.output(13, GPIO.LOW)
GPIO.output(11, GPIO.LOW)
time.sleep(1)
GPIO.output(5, GPIO.HIGH)
GPIO.output(3, GPIO.HIGH)
GPIO.output(13, GPIO.HIGH)
GPIO.output(11, GPIO.HIGH)
    
# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)
a = 'checked'

@app.route('/',methods=['GET','POST'])
def index():
    if request.method =='POST':
        GPIO.output(5, GPIO.LOW)
        time.sleep(0.001)
        GPIO.output(5, GPIO.HIGH)
        a = request.form["on2"]
        b = request.form["radio"]
        if b == 'one':
            if a == 'on':
                GPIO.output(11, GPIO.HIGH)
                return render_template('index.html',i = 'ON',a = 'checked')
            else:
               GPIO.output(11, GPIO.LOW)
               return render_template('index.html',i = 'OFF',a = 'checked')
        if b == 'two':
            if a == 'on':
                GPIO.output(13, GPIO.LOW)
                return render_template('index.html',j = 'ON',b = 'checked')
            else:
                GPIO.output(13, GPIO.HIGH)
                return render_template('index.html',j = 'OFF',b = 'checked')
        else:
            return render_template('index.html',w = 'please choose the botton!')
    else:
        GPIO.output(3, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(3, GPIO.HIGH)
        return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
