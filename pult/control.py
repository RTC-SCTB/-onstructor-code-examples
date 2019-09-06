""" Модуль описывающий управление роботом """
import threading
import time
from pult import config
from pult import socketrobot


class Control(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        self.robot = socketrobot.SocketRobot()
        self._joystick = None
        self._cameraPos = False  # позиция камеры
        self.__exit = False

    def setJoystick(self, joystick):  # устанавливаем джойстик, которым будем управлять
        self._joystick = joystick
        self.connectHandlers()

    def connectHandlers(self):  # привязка обработчиков кнопок
        def addSpeed(w):
            if w:
                self.robot.motorSpeed += config.SPEED_CHANGE_STEP  # прибавляем скорость

        def subSpeed(w):
            if w:
                self.robot.motorSpeed -= config.SPEED_CHANGE_STEP  # уменьшаем скорость

        def rotateCamera(w):
            if w:
                self._cameraPos = not self._cameraPos
                self.robot.setCamera(int(self._cameraPos))  # True - 1, False - 0

        self._joystick.onButtonClick(config.ADD_SPEED_BUTTON, addSpeed)
        self._joystick.onButtonClick(config.SUB_SPEED_BUTTON, subSpeed)
        self._joystick.onButtonClick(config.ROTATE_CAMERA_BUTTON, rotateCamera)

    def exit(self):
        self.__exit = True
        self.robot.disconnect()

    def run(self):
        while not self.__exit:
            #try:
                if self.robot.exist and (self._joystick is not None):  # если клиент и джойстик созданы
                    if not (self._joystick.buttons[config.ROTATE_LEFT_BUTTON] or self._joystick.buttons[config.ROTATE_RIGHT_BUTTON]):
                        # если нет разворота на месте
                        self.robot.rotate(0.0)  # убираем поворот
                        self.robot.turnForward(self._joystick.axis.get(config.TURN_STICK))  # поворот
                        self.robot.move(self._joystick.axis.get(config.MOVE_STICK))  # движение
                    else:
                        if self._joystick.buttons[config.ROTATE_RIGHT_BUTTON]:
                            self.robot.rotate(1.0)
                        elif self._joystick.buttons[config.ROTATE_LEFT_BUTTON]:
                            self.robot.rotate(-1.0)

            #except Exception as e:
            #    print("Ошибка управления: " + str(e))
                time.sleep(config.SEND_DELAY)
