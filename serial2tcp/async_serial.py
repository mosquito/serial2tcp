# encoding: utf-8
import logging
import time
import serial
from threading import Thread

__author__ = 'Dmitry Orlov <me@mosquito.su>'

log = logging.getLogger('serial2tcp.SerialAsync')

class SerialAsync(object):
    def __init__(self, port=None, baudrate=9600, bytesize=8, parity='N', stopbits=1,
                 xonxoff=False, rtscts=False, writeTimeout=None, dsrdtr=False,
                 interCharTimeout=None):
        self.__port = serial.Serial(
            port=port, baudrate=baudrate, bytesize=bytesize, parity=parity, stopbits=stopbits, timeout=0,
            xonxoff=xonxoff, rtscts=rtscts, writeTimeout=writeTimeout, dsrdtr=dsrdtr, interCharTimeout=interCharTimeout
        )

        self.__write_queue = list()
        self.__callbacks = dict()

        self.__alive = True

        self.__writer_thread = Thread(target=self._writer, args=())
        self.__writer_thread.start()

    def __del__(self):
        self.__alive = False

    def open(self):
        self.__port.open()

    def _writer(self):
        while self.__alive:
            while self.__write_queue:
                id, data = self.__write_queue.pop(0)

                self.__port.write(data)
                readed = ''
                chunk = self.__port.read(1024)
                readed += chunk
                while chunk:
                    readed += chunk
                    chunk = self.__port.read(1024)

                if self.__callbacks.has_key(id):
                    try:
                        self.__callbacks[id](readed)
                    except Exception as e:
                        log.error('Callback {0} raised exception: {1}'.format(id, repr(e)))

            time.sleep(0.001)

    def write_async(self, data, callback=lambda x: x):
        id = time.time()
        self.__write_queue.append((id, data))
        self.__callbacks[id] = callback