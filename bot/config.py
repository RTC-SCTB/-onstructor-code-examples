""" Конфигурация робота """
from bot.RPiPWM import *
from bot.bldcbot import BLDCbot, WorkMode
import smbus
from bot import rpicam

"""
    F - Front
    B - Backside
    L - Left
    R - Right
"""
IP = "192.168.42.100"
PORT = 8004
RTP_PORT = 5000

VIDEO_FORMAT = rpicam.VIDEO_MJPEG  # поток MJPEG
VIDEO_RESOLUTION = (640, 360)
VIDEO_FRAMERATE = 20

bus = smbus.SMBus(1)
motorsF = BLDCbot(bus, addr=0x27)
motorsF.setWorkMode(WorkMode.WORK_MODE_PID_I2C)
motorsB = BLDCbot(bus, addr=0x29)
motorsB.setWorkMode(WorkMode.WORK_MODE_PID_I2C)

chanSrvFL = 1  # канал для передней левой сервы
chanSrvFR = 2  # канал для передней правой сервы
chanSrvBL = 3  # канал для задней левой сервы
chanSrvBR = 4  # канал для задней правой сервы
chanSrvCAM = 5  # канал для сервы с камерой

chanSrvM1A = 6  # канал 1 оси манипулятора
chanSrvM2A = 7  # канал 2 оси манипулятора
chanSrvM3A = 8  # канал 3 оси манипулятора
chanSrvM4A = 9  # канал 4 оси манипулятора
chanSrvM5A = 10  # канал 5 оси манипулятора

srvResolutionMcs = (800, 2200)  # центр в 1500
rotateAngleScale = 0.643     # угол в mcs, на который надо повернуть сервы, чтобы робот крутился\
#  на месте (тут примено 57 градусов) для квадратных роботов это 45 градусов (примерно 1850 mcs)


SrvFL = Servo270(chanSrvFL)  # передняя левая
SrvFR = Servo270(chanSrvFR)  # передняя правая
SrvBL = Servo270(chanSrvBL)  # задняя левая
SrvBR = Servo270(chanSrvBR)  # задняя правая
SrvCAM = Servo90(chanSrvCAM)    # серва камеры

SrvM1A = Servo270(chanSrvM1A)   # сервы манипулятора
SrvM2A = Servo270(chanSrvM2A)
SrvM3A = Servo270(chanSrvM3A)
SrvM4A = Servo270(chanSrvM4A)
SrvM5A = Servo270(chanSrvM5A)


def getMcsByScale(scale):
    """ получаем нужные значения мкс(srvResolutionMcs[0], srvResolutionMcs[1]) из значения scale (-1:1) """
    scale = min(max(-1.0, scale), 1.0)  # проверяем еще раз значение scale
    return int(((scale + 1)/2) * (srvResolutionMcs[1] - srvResolutionMcs[0]) + srvResolutionMcs[0])


def turnForward(scale):
    SrvFL.setMcs(getMcsByScale(scale))
    SrvFR.setMcs(getMcsByScale(scale))
    SrvBR.setMcs(getMcsByScale(0))
    SrvBL.setMcs(getMcsByScale(0))


def move(speed):
    motorsF.setParrotA(-speed)
    motorsF.setParrotB(speed)
    motorsB.setParrotA(-speed)
    motorsB.setParrotB(speed)


def rotate(speed):
    if abs(speed) < 10:     # если скорость меньше 10, то возвращаемся из состояния поворота на месте
        SrvFL.setMcs(getMcsByScale(0))
        SrvFR.setMcs(getMcsByScale(0))
        SrvBR.setMcs(getMcsByScale(0))
        SrvBL.setMcs(getMcsByScale(0))
        move(0)
    else:
        SrvFL.setMcs(getMcsByScale(rotateAngleScale))
        SrvFR.setMcs(getMcsByScale(-rotateAngleScale))
        SrvBR.setMcs(getMcsByScale(rotateAngleScale))
        SrvBL.setMcs(getMcsByScale(-rotateAngleScale))
        move(speed)


def turnAll(scale):
    pass


def setCamera(scale):
    SrvCAM.setMcs(getMcsByScale(scale))


def turnFirstAxisArg(scale):
    SrvM1A.setMcs(getMcsByScale(scale))


def turnSecondAxisArg(scale):
    SrvM2A.setMcs(getMcsByScale(scale))


def turnThirdAxisArg(scale):
    SrvM3A.setMcs(getMcsByScale(scale))


def turnFourthAxisArg(scale):
    SrvM4A.setMcs(getMcsByScale(scale))


def turnFifthAxisArg(scale):
    SrvM5A.setMcs(getMcsByScale(scale))


def initializeAll():
    move(0)
    SrvFL.setMcs(getMcsByScale(0))
    SrvFR.setMcs(getMcsByScale(0))
    SrvBR.setMcs(getMcsByScale(0))
    SrvBL.setMcs(getMcsByScale(0))
    time.sleep(1)
    SrvM1A.setMcs(getMcsByScale(0))
    time.sleep(1)
    SrvM2A.setMcs(getMcsByScale(0))
    time.sleep(1)
    SrvM3A.setMcs(getMcsByScale(0))
    time.sleep(1)
    SrvM4A.setMcs(getMcsByScale(0))
    time.sleep(1)
    SrvM5A.setMcs(getMcsByScale(0))
    time.sleep(1)
