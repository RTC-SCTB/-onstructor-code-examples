""" Модуль описывающий управление роботом """
import threading
import time
from pult import config
from pult import socketrobot
from pynput import keyboard


def remapScale(scale):
    """ защита от дурака ограничивает значение scale до диапазона (-1; 1) """
    return min(max(-1.0, scale), 1.0)


class Control(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        self.robot = socketrobot.SocketRobot()
        self._joystick = None
        self._keyboard = None
        self._cameraPos = False  # позиция камеры
        self._moveScale = 0.0   # данные о движении робота
        self._turnScale = 0.0
        self._manipulatorScaleAxis = [0.0, 0.0, 0.0, 0.0, 0.0]  # позиция манипулятора
        self._manipulatorMoveStep = 0.01     # шаг движения манипулятора
        self._selectedAxis = 1  # выбранная ось поворота манипулятора
        self.__exit = False

    def setJoystick(self, joystick):  # устанавливаем джойстик, которым будем управлять
        self._joystick = joystick
        self._connectJoystickHandlers()

    def fromKeyboard(self):
        self._connectKeyboardHandlers()

    def _connectJoystickHandlers(self):  # привязка обработчиков кнопок
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

    def _connectKeyboardHandlers(self):  # привязка обработчиков кнопок клавиатуры
        def onPress(key):
            try:
                if key.char == 'w':
                    self._moveScale = 1.0
                elif key.char == 's':
                    self._moveScale = -1.0
                if key.char == 'a':
                    self._turnScale = -0.5
                elif key.char == 'd':
                    self._turnScale = 0.5
                # вращаем выбранную ось манипулятора
                if key.char == 'q':
                    self._manipulatorScaleAxis[self._selectedAxis - 1] = remapScale(
                        self._manipulatorScaleAxis[self._selectedAxis - 1] - self._manipulatorMoveStep)
                    self.robot.moveManipulator(*self._manipulatorScaleAxis)
                elif key.char == 'e':
                    self._manipulatorScaleAxis[self._selectedAxis - 1] = remapScale(
                        self._manipulatorScaleAxis[self._selectedAxis - 1] + self._manipulatorMoveStep)
                    self.robot.moveManipulator(*self._manipulatorScaleAxis)
            except AttributeError:
                pass

        def onRelease(key):
            try:
                if (key.char == 'w') or (key.char == 's'):
                    self._moveScale = 0.0
                if (key.char == 'a') or (key.char == 'd'):
                    self._turnScale = 0.0
                # выбираем ось манипулятора
                if key.char == '1':
                    self._selectedAxis = 1
                if key.char == '2':
                    self._selectedAxis = 2
                if key.char == '3':
                    self._selectedAxis = 3
                if key.char == '4':
                    self._selectedAxis = 4
                if key.char == '5':
                    self._selectedAxis = 5

            except AttributeError:
                pass

        self._keyboard = keyboard.Listener(on_press=onPress, on_release=onRelease)
        self._keyboard.start()

    def exit(self):
        self.__exit = True
        self.robot.disconnect()

    def run(self):
        while not self.__exit:
            try:
                if self.robot.exist and (self._joystick is not None):  # если клиент и джойстик созданы
                    pass  # тут можно сделать управление с джойстика
                elif self.robot.exist and (self._keyboard is not None):  # если клиент и клавиатура созданы:
                    self.robot.move(self._moveScale)
                    self.robot.turnForward(self._turnScale)
                else:
                    time.sleep(3)
            except Exception as e:
                print("Ошибка управления: " + str(e))
            time.sleep(config.SEND_DELAY)
