import time
from main import MotoDll

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


def calibr():
    moto.startPLC(1, 2)
    moto.startPLC(2, 2)


def work():
    moto.startPLC(1, 3)
    moto.startPLC(2, 3)
    while True:
        pos1 = moto.readVal(1, b'dd8')
        pos2 = moto.readVal(2, b'dd8')
        print(pos1, pos2)
        time.sleep(0.1)
pos1 = moto.readVal(1, b'dd8')
pos2 = moto.readVal(2, b'dd8')
print(pos1, pos2)
# calibr()
work()
