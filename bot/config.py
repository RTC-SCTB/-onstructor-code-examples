""" Конфигурация робота """
# from RPiPWM import *
import time
from bot import rpicam
from bot import edubot
import smbus

"""
    F - Front
    B - Backside
    L - Left
    R - Right
"""

IP = "192.168.42.100"
PORT = 8010
RTP_PORT = 5000

VIDEO_FORMAT = rpicam.VIDEO_MJPEG  # поток MJPEG
VIDEO_RESOLUTION = (640, 360)
VIDEO_FRAMERATE = 20

bus = smbus.SMBus(1)
robot = edubot.EduBot(bus)


servoPosLen = 255
middleServoPos = int(servoPosLen / 2)

rotateSpeed = 100


def turnForward(scale):
    robot.setParrot0(int(rotateSpeed*scale))
    robot.setParrot1(int(rotateSpeed*scale))


def move(speed):
    robot.setParrot0(int(-speed))
    robot.setParrot1(int(speed))


def rotate(scale):
    pass


def turnAll(scale):
    pass


def setCamera(scale):
    robot.beep()
    robot.setServo0(int(middleServoPos - scale * servoPosLen))


def initializeAll():
    robot.online = True
    robot.start()
    robot.setMotorMode(edubot.MotorMode.MOTOR_MODE_PID)
    robot.setParrot0(0)
    robot.setParrot1(0)
    robot.setServo0(int(middleServoPos))
    robot.setServo1(int(middleServoPos))
