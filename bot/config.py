""" Конфигурация робота """
# from RPiPWM import *
import time

"""
    F - Front
    B - Backside
    L - Left
    R - Right
"""
IP = "127.0.0.1"
PORT = 8004
RTP_PORT = 5000

# TODO: тут ф-ии управления все прописываются
srvResolutionMcs = (800, 2200)  # центр в 1500


def getMcsByScale(scale):
    """ получаем нужные значения мкс(srvResolutionMcs[0], srvResolutionMcs[1]) из значения scale (-1:1) """
    scale = min(max(-1.0, scale), 1.0)  # проверяем еще раз значение scale
    return int(((scale + 1)/2) * (srvResolutionMcs[1] - srvResolutionMcs[0]) + srvResolutionMcs[0])


def turnForward(scale):
    print("turnForward", scale)


def move(speed):
    print("move", speed)


def rotate(scale):
    print("rotate", scale)


def turnAll(scale):
    print("turnAll", scale)


def setCamera(scale):
    print("setCamera", scale)


def initializeAll():
    pass
    time.sleep(1)
