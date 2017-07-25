from ctypes import *

class MotoDll:
    """
    Python wrapper для библиотеки moto_dll2.

    Библиотека moto_dll2 предоставляет программный интерфейс для работы с приводами СПШ/СПС,
    подключенными к компьютеру по одному из следующих интерфейсов:

    - USB
    - CAN через плату SL06.A
    - CAN с использованием функции ретрансляции CAN-USB приводов СПШ/СПС
    - CAN с использованием функции ретрансляции CAN-Ethernet СЧПУ СервоКон
    - CAN через шлюз CAN-Ethernet ECG01/ECG02
    - Ethernet (только СПС)

    Библиотека позволяет выполнять следующие действия:

    - Чтение текущих значений параметров приводов
    - Запись значений параметров приводов
    - Управление выполнением программ ПЛК
    - Управление и опрос данных встроенного осциллографа(!!!YET NOT IMPLEMENTED!!!)

    ЗАМЕЧАНИЕ:
    Предварительно необходимо установить МотоМастер.
    Для работы библиотеки необходимо, чтобы в директории с python.exe
    находился файл описания параметров привода tree_ru.dev или tree_en.dev.
    """

    errorCode = {-1: 'CAN`T OPEN PORT',
                 -2: 'CAN`T GET PARAMS',
                 -3: 'CAN`T_SET_BUFSIZE',
                 -4: 'CAN`T_SET_PARAMS',
                 -5: 'CAN`T SET TIMEOUTS',
                 -6: 'INTERNAL FAULT',
                 -7: 'INVALID_PARAM',
                 -8: 'PORT CLOSED',
                 -300: 'INTERNAL FAULT',
                 -301: 'INVALID PARAM',
                 -302: 'PORT CLOSED',
                 -303: 'PORT ALREADY OPEN',
                 -600: 'INVALID INVERTER NUMBER',
                 -700: 'BUSY',
                 -701: 'EMPTY SCRIPT',
                 -702: 'OBSOLETE',
                 -703: 'GENERIC ERROR',
                 -704: 'NOT IMPLEMENTED',
                 -16: 'PORT DEAD',
                 -17: 'TIMEOUT',
                 -18: 'BAD_ADDR',
                 -19: 'TOO LONG',
                 -20: 'FRAMING_ERROR'}

    def __init__(self):
        self.lib = cdll.LoadLibrary('./moto_dll2.dll')
        self.lib.InitParser.restype = c_int
        self.lib.EnumDevices.restype = c_int
        self.lib.OpenPort.restype = c_int
        self.lib.ClosePort.restype = c_int
        self.lib.ReadVal.argtypes = (c_int, c_char_p, POINTER(c_double))
        self.lib.ReadVal.restype = c_int
        self.lib.WriteVal.argtypes = (c_int, c_char_p, c_double)
        self.lib.WriteVal.restype = c_int
        self.lib.StartPLC.argtypes = (c_int, c_int)
        self.lib.StartPLC.restype = c_int
        self.lib.StopPLC.restype = c_int

    def initParser(self):
        """
        Инициализирует библиотеку.
        Эта функция должна быть вызвана до вызова других функций библиотеки
        Возвращает 1 при успешной инициализации.
        """
        result = self.lib.InitParser()
        self.__chekResult(result)

    def enumDevices(self, doClosePorts):
        """
        Производит поиск подключенных приводов.
        После вызова можно использовать остальные функции связи, указывая номер привода.
        Если параметр имеет значение false, то оставляет открытыми порты USB.
        Возвращает общее количество обнаруженных приводов.
        """
        result = self.lib.EnumDevices(c_bool(doClosePorts))
        self.__chekResult(result)
        return result

    def openPort(self, num):
        """
        Начать работу с приводом.
        """
        result = self.lib.OpenPort(c_int(num))
        self.__chekResult(result)

    def closePort(self, num):
        """
        Завершить работу с приводом.
        """
        result = self.lib.ClosePort(c_int(num))
        self.__chekResult(result)

    def readVal(self, inv, name):
        """
        Считать значение параметра привода с именем name в переменную по адресу val.
        Имя параметра задается в виде zero-terminated ASCII string, чувствительно к регистру.
        Имена параметров см. в файле tree_en.dev
        """
        val = c_double(0.0)
        result = self.lib.ReadVal(c_int(inv), c_char_p(name), byref(val))
        self.__chekResult(result)
        return val.value

    def writeVal(self, inv, name, val):
        """
        Записать значение val в параметр привода с именем name.
        Имя параметра задается в виде zero-terminated ASCII string, чувствительно к регистру.
        Имена параметров см. в файле tree_en.dev
        """
        result = self.lib.WriteVal(c_int(inv), c_char_p(name), c_double(val))
        self.__chekResult(result)

    def startPLC(self, inv, index):
        """
        Запустить программу ПЛК с номером index. Библиотека не проверяет наличие и правильность программы.
        """
        result = self.lib.StartPLC(c_int(inv), c_int(index))
        self.__chekResult(result)

    def stopPLC(self, inv, index):
        """
        Остановить выполнение программы ПЛК.
        """
        result = self.lib.StartPLC(c_int(inv), c_int(index))
        self.__chekResult(result)

    def loadProgram(self, motor, bank, program, version):
        """
        !!!YET NOT IMPLEMENTED!!!
        Считать программу из банка bank привода motor. Программа записывается в буфер program,
        длина программы не более 256 слов.
        По адресу version записывается версия программы (текущая версия 3).
        Указатели program и version должны быть корректными.
        Программа возвращается в бинарном виде.
        """
        pass

    def writeProgram(self, motor, bank, program):
        """
        !!!YET NOT IMPLEMENTED!!!
        Записать программу в банк bank привода motor. Длина программы не должна превышать 256 слов.
        """
        pass

    def getPortName(self, inv, buf):
        """
        !!!YET NOT IMPLEMENTED!!!
        Получить текстовое имя интерфейса подключения привода. Длина имени не более 32 символов.
        """
        pass

    def addParamToStream(self, inv, name, onPointCallBack):
        """
        !!!YET NOT IMPLEMENTED!!!
        Добавить параметр с именем name в осциллограф.
        При получении очередного значения будет вызвана функция обратного вызова onPoint,
        в качестве параметров которой передаются номер привода, адрес параметра, значение параметра,
        данные пришедшего пакета и их длина.
        """
        pass

    def removeParamFromStream(self, inv, name):
        """
        !!!YET NOT IMPLEMENTED!!!
        Удалить параметр с именем name из осциллографа.
        """
        pass

    def startStream(self, inv):
        """
        !!!YET NOT IMPLEMENTED!!!
        Запустить осциллограф. В непрерывном режиме осциллограф будет захватывать и передавать
        значения параметров с частотой порядка 100Гц пока не будет остановлен.
        В режиме реального времени привод выполнит сбор 1500 точек с указанной в параметрах частотой
        и затем передаст собранные значения
        Примечание: необходимо предварительно вызвать функцию OpenPort.
        """
        pass

    def stopStream(self, inv):
        """
        !!!YET NOT IMPLEMENTED!!!
        Остановить осциллограф.
        """
        pass

    def closeParser(self):
        """
        Завершает работу с библиотекой
        Функцию необходимо вызывать обязательно для корректного завершения работы драйвера CAN.
        """
        result = self.lib.CloseParser()
        self.__chekResult(result)

    def __chekResult(self, result):
        if int(result) < 0:
            raise Exception(self.errorCode[int(result)])

# EXAMPLE USAGE:
moto = MotoDll()
moto.initParser()
count = moto.enumDevices(True)
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
moto.startPLC(1, 0)
moto.stopPLC(1, 0)
moto.closePort(1)
moto.closeParser()
