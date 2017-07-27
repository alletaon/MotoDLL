from time import sleep
from main import MotoDll

# EXAMPLE USAGE:
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
# read params cp1 from drive
val = moto.readVal(1, b'cp1')
print('cp1 = ', val)
moto.writeVal(1, b'cp1', 3.0)
val_new = moto.readVal(1, b'cp1')
print('cp1 = ', val_new)
moto.writeVal(1, b'cp1', val)
position = moto.readVal(1, b'dd8')
print('Pos: ', position)
moto.startPLC(1, 0)
# read current program bank must be 3
print(moto.readVal(1, b'ip2'))
print(moto.readVal(1, b'ip11'))
sleep(5)
# read current plc status
print(moto.readVal(1, b'ip11'))
moto.stopPLC(1)
sleep(2)
# read current program bank must be 255
print(moto.readVal(1, b'ip2'))
print(moto.getPortName(1))
position = moto.readVal(1, b'dd8')
print('Pos: ', position)
moto.closePort(1)
moto.closeParser()
