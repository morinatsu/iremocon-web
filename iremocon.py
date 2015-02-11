# -*- coding: utf-8 -*-
"""
iremocon.py: Send and Recieve Messages with i-remocon
"""
import socket
import json
import configparser
from logging import getLogger, StreamHandler, INFO, DEBUG
from threading import RLock

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)
lock = RLock()

class IRemocon(object):
    """
    Command Sender class
    """

    def __init__(self, config_file):
        """
        Make a New Instance
        """
        def invert_dict(src_dict, inverted_dict, key_list):
            """ make invert dict from dict """
            for k in src_dict:
                new_list = key_list[:]
                new_list.append(k)
                if not (isinstance(src_dict[k], dict)):
                    inverted_dict[str(src_dict[k])] = new_list
                else:
                    inverted_dict = invert_dict(src_dict[k], inverted_dict,
                        new_list)
            logger.debug(str(inverted_dict))
            return inverted_dict


        config = configparser.ConfigParser()
        config.read(config_file)
        self._host = config.get('network', 'HOST')
        self._port = int(config.get('network', 'PORT'))
        self._remocon_filename = config.get('remocon code', 'filename')
        logger.info(
            ''.join(['remocon code file:', self._remocon_filename]))
        f = open(self._remocon_filename, encoding='utf-8')
        self.code = json.load(f)
        f.close()
        self.inverted_code = invert_dict(self.code, {}, [])

    def SendCommand(self, message):
        with lock:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(60)
            s.connect((self._host, self._port))
            s.sendall(message)

            chunks = []
            while True:
                chunk = s.recv(1024)
                chunks.append(chunk)
                if chunk.endswith(b'\r\n'):
                    break
            s.close()
            return b''.join(chunks)
