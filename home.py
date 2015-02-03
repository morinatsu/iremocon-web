#!/usr/bin/env python
#! -*- coding: utf-8 -*-
"""
Display Info of Sencers in i-remocon
"""

import datetime
import json
from logging import getLogger, StreamHandler, DEBUG, INFO
from flask import Flask, render_template, redirect, request
from iremocon import IRemocon


logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)

app = Flask(__name__)

def display_sensors_info():
    """
    Display Information of iRemocon Built-In Sensors
    """
    sensors_info = {}
    remocon = IRemocon('iremocon.yaml')
    # send command
    answer = remocon.SendCommand(b'*se\r\n').decode('ascii').rstrip('\r\n')
    logger.info(''.join(['Recieved: ', answer]))
    # parse answer
    if answer.startswith('se;ok;'):
        sensors_info['illuminance'] = \
            '{illum:.0f}lx'.format(illum=float(answer.split(';')[2]))
        sensors_info['humidity'] = \
            '{humid:.0f}%'.format(humid=float(answer.split(';')[3]))
        sensors_info['temperature'] = \
            '{temper:.1f}C'.format(temper=float(answer.split(';')[4]))
    else:
        sensors_info['alt_msg']= 'Error: cannot recieve sensors info.'
    return sensors_info

def list_timers():
    """
    List Timers Has Set
    """
    def reparse_time(seconds):
        date_time = datetime.datetime(1970, 1, 1, 9, 0, 0) + \
            datetime.timedelta(seconds=int(seconds))
        return date_time.strftime('%Y/%m/%d %H:%M:%S')
    timers = []
    alt_msg = ''
    remocon = IRemocon('iremocon.yaml')
    # send command
    answer = remocon.SendCommand(b'*tl\r\n').decode('ascii').rstrip('\r\n')
    logger.info(''.join(['Recieved: ', answer]))
    # parse answer
    if answer.startswith('tl;ok;'):
        head = answer.split(';')[0:2]
        body = answer.split(';')[3:]
        while len(body) > 0:
            timer = {}
            timer['seq'] = body.pop(0)
            timer['code'] = str(remocon.inverted_code[body.pop(0)])
            timer['time'] = reparse_time(body.pop(0))
            repeat = body.pop(0)
            timers.append(timer)
    elif answer.startswith('tl;err;001'):
        alt_msg = 'no timers has set.'
    else:
        alt_msg = 'Error: cannot recieve timers list.'
    logger.info(repr(timers))
    return (timers, alt_msg)

def display_firmware_version():
    """
    Display Firmware Version of iRemocon
    """
    div =[]
    remocon = IRemocon('iremocon.yaml')
    # send command
    answer = remocon.SendCommand(b'*vr\r\n').decode('ascii')
    div.append(''.join(['Firmware Version: ', answer]))
    return '\n'.join(div)

@app.route('/api/auto_update')
def auto_update():
    """
    api for autoupdate info on home
    """
    sensors_info = display_sensors_info()
    return json.dumps(sensors_info)

@app.route('/api/cancel_timer', methods=['POST'])
def cancel_timer():
    """
    api for cancel a timer
    """
    timer_number = request.form['timer_number']
    if not (timer_number.isdecimal()):
        logger.info('Invalid request. timer_number:', timer_number)
        redirect('/')
    remocon = IRemocon('iremocon.yaml')
    # send command
    command = b''.join([b'*td;', timer_number.encode('ascii'), b'\r\n'])
    answer = remocon.SendCommand(command).decode('ascii').rstrip('\r\n')
    logger.info(''.join(['Recieved: ', answer]))
    # redirect to home, if success or not.
    return redirect('/')

@app.route('/')
def home():
    return render_template('iremocon.html', sensors_info=display_sensors_info(),
            timers=list_timers(),
            firmware_version=display_firmware_version())

if __name__ == '__main__':
    app.run(debug=True)
