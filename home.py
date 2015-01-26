#!/usr/bin/env python
#! -*- coding: utf-8 -*-
"""
Display Info of Sencers in i-remocon
"""

import datetime
from logging import getLogger, StreamHandler, DEBUG, INFO
from flask import Flask, render_template
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
    div =[]
    remocon = IRemocon('iremocon.yaml')
    # send command
    answer = remocon.SendCommand(b'*se\r\n').decode('ascii')
    logger.info(''.join(['Recieved: ', answer]))
    # parse answer
    if answer.startswith('se;ok;'):
        illuminance = float(answer.rstrip('\r\n').split(';')[2])
        humidity = float(answer.rstrip('\r\n').split(';')[3])
        temperature = float(answer.rstrip('\r\n').split(';')[4])
        div.append('illuminance: {illum:.0f}lx'.format(illum=illuminance))
        div.append('humidity: {humidity:.0f}%'.format(humidity=humidity))
        div.append('temperature: {temper:.1f}C'.format(temper=temperature))
    else:
        div.append('Error: cannot recieve sensors info.')
    return div

def list_timers():
    """
    List Timers Has Set
    """
    def reparse_time(seconds):
        date_time = datetime.datetime(1970, 1, 1, 9, 0, 0) + \
            datetime.timedelta(seconds=int(seconds))
        return date_time.strftime('%Y/%m/%d %H:%M:%S')
    div = []
    remocon = IRemocon('iremocon.yaml')
    # send command
    answer = remocon.SendCommand(b'*tl\r\n').decode('ascii')
    logger.info(''.join(['Recieved: ', answer]))
    # parse answer
    if answer.startswith('tl;ok;'):
        head = answer.rstrip('\r\n').split(';')[0:2]
        body = answer.rstrip('\r\n').split(';')[3:]
        while len(body) > 0:
            seq = body.pop(0)
            code = repr([s for s in remocon.inverted_code[body.pop(0)]])
            time = reparse_time(body.pop(0))
            repeat = body.pop(0)
            div.append('Seq: {seq}, Code: {code}, Time: {time}'.format(seq=seq, code=code, time=time))
    elif answer.startswith('tl;err;001'):
        div.append('no timers has set.')
    else:
        div.append('Error: cannot recieve timers list.')
    return div

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

@app.route('/')
def home():

    return render_template('iremocon.html', sensors_info = display_sensors_info(),
            list_timers = list_timers(),
            firmware_version = display_firmware_version())

if __name__ == '__main__':
    app.run(debug=True)
