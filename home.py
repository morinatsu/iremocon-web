#!/usr/bin/env python
#! -*- coding: utf-8 -*-
"""
Display Info of Sencers in i-remocon
"""

from flask import Flask
from iremocon import IRemocon

app = Flask(__name__)


@app.route('/')
def home():
    body = []

    remocon = IRemocon('iremocon.yaml')

    # send command
    answer = remocon.SendCommand(b'*se\r\n').decode('ascii')
    body.append(''.join(['Recieved: ', answer]))
    body.append('')

    # parse answer
    if answer.startswith('se;ok;'):
        illuminance = float(answer.rstrip('\r\n').split(';')[2])
        humidity = float(answer.rstrip('\r\n').split(';')[3])
        temperature = float(answer.rstrip('\r\n').split(';')[4])
        body.append('illuminance: {illum:.0f}lx'.format(illum=illuminance))
        body.append('humidity: {humidity:.0f}%'.format(humidity=humidity))
        body.append('temperature: {temper:.0f}°C'.format(temper=temperature))
    else:
        body.append('Error')
    return '<br />'.join(body)

if __name__ == '__main__':
    app.run(debug=True)
