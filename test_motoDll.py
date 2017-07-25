from time import sleep
from unittest import TestCase
from main import MotoDll


class TestMotoDll(TestCase):
    moto = MotoDll()

    def test_motoDll(self):
        self.moto.initParser()
        repeatCount = 10
        count = 0
        while repeatCount > 0:
            count = self.moto.enumDevices(True)
            if count > 0:
                break
            repeatCount -= 1
        self.assertEqual(count, 1)
        self.moto.openPort(1)
        val = self.moto.readVal(1, b'cp1')
        self.assertEqual(val, 4.0)
        self.moto.writeVal(1, b'cp1', 3.0)
        val = self.moto.readVal(1, b'cp1')
        self.assertEqual(val, 3.0)
        self.moto.writeVal(1, b'cp1', 4.0)
        self.moto.startPLC(1, 3)
        sleep(2)
        val = self.moto.readVal(1, b'ip2')
        self.assertEqual(val, 3.0)
        val = self.moto.readVal(1, b'ip11')
        self.assertEqual(val, 0.0)
        self.moto.stopPLC(1)
        sleep(2)
        val = self.moto.readVal(1, b'ip2')
        self.assertEqual(val, 255.0)
        self.moto.closePort(1)
        self.moto.closeParser()
