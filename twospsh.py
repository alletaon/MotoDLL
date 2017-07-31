"""
Пример работы с двумя СПШ
"""

import time
from main import MotoDll

def init():
    moto = MotoDll()
    moto.initParser()
    repeatCount = 10
    count = 0
    while repeatCount > 0:
        count = moto.enumDevices(True)
        if count > 0:
            break
        repeatCount -= 1
    print('Count: ', count)
    if count == 0:
        print('No devices available')
        exit(1)
    moto.openPort(1)
    moto.openPort(2)
    return moto


def calibr(moto):
    moto.startPLC(1, 2)
    moto.startPLC(2, 2)


def work(moto):
    moto.startPLC(1, 3)
    moto.startPLC(2, 3)


def stop(moto):
    moto.writeVal(1, b'dd11', 1.0)
    moto.writeVal(2, b'dd11', 1.0)


def resume(moto):
    moto.writeVal(1, b'dd11', 0.0)
    moto.writeVal(2, b'dd11', 0.0)

moto = init()
calibr(moto)
work(moto)
time.sleep(20)
stop(moto)
time.sleep(2)
resume(moto)
