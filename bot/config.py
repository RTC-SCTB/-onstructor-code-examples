""" Конфигурация робота """
# from RPiPWM import *
import time
from bot import rpicam
from bot import edubot2

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

robot = edubot2.EduBot(enableDisplay=True)  # создаем обект для работы с EduBot, робот с OLED дисплеем
assert robot.Check(), 'EduBot not found!!!'  # проверяем наличие платы Edubot

robot.SetMotorMode(edubot2.MOTOR_MODE_PWM)
robot.Start()  # обязательная процедура, запуск потока отправляющего на контроллер EduBot онлайн сообщений

servoPosLen = 255
middleServoPos = int(servoPosLen / 2)

rotateSpeed = 100

robot.Beep()


def turnForward(scale):
    robot.leftMotor.SetSpeed(int(rotateSpeed*scale))
    robot.rightMotor.SetSpeed(int(rotateSpeed*scale))


def move(speed):
    robot.Beep()
    robot.leftMotor.SetSpeed(int(-speed))
    robot.rightMotor.SetSpeed(int(speed))


def rotate(scale):
    pass


def turnAll(scale):
    pass


def setCamera(scale):
    robot.servo[0].SetPosition(int(middleServoPos - scale*servoPosLen))


def initializeAll():
    robot.leftMotor.SetSpeed(0)
    robot.rightMotor.SetSpeed(0)
    robot.servo[0].SetPosition(int(middleServoPos))
    robot.servo[1].SetPosition(int(middleServoPos))
    time.sleep(1)
