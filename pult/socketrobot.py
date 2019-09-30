from utility import sender


def remapScale(scale):
    """ защита от дурака ограничивает значение scale до диапазона (-1; 1) """
    return min(max(-1.0, scale), 1.0)


class SocketRobot:
    def __init__(self):
        self._ip = None
        self._port = None
        self._sender = None
        self._motorSpeed = 40
        self._argDict = {
            "turnForwardArg": float(0.0),
            "moveArg": int(0.0),
            "rotateArg": int(0.0),
            "turnAllArg": float(0.0),
            "setCameraArg": float(0.0)
        }

    def connect(self, ip, port):
        self._sender = sender.Sender(ip, port)
        self._sender.packageFormat = "fiiff"
        self._sender.connect()

    def disconnect(self):
        self._sender.disconnect()

    def sendPackage(self):
        self._sender.sendPackage(self._sender.pack(
            self._argDict["turnForwardArg"], self._argDict["moveArg"],
            self._argDict["rotateArg"], self._argDict["turnAllArg"],
            self._argDict["setCameraArg"]
        ))

    def turnForward(self, scale):  # scale - значение из диапазона (-1, 1)
        # поворачиваем сервами в зависимости от значения со стика
        self._argDict["turnForwardArg"] = float(remapScale(scale))

    def move(self, scale):  # scale - значение из диапазона (-1, 1) # движемся вперед со скоростью
        # MotorSpeed*коэффициент scale
        self._argDict["moveArg"] = int(remapScale(scale) * self._motorSpeed)

    def rotate(self, scale):  # scale - значение из диапазона (-1, 1) # поворачиваемся со скоростью моторов
        # MotorSpeed*коэффициент scale
        self._argDict["rotateArg"] = int(remapScale(scale) * self._motorSpeed)

    def turnAll(self, scale):  # поворачивает всеми сервами на один и тот же угол
        self._argDict["turnAllArg"] = float(remapScale(scale))

    def setCamera(self, scale):
        self._argDict["setCameraArg"] = float(remapScale(scale))

    @property
    def exist(self):
        return bool(self._sender)

    @property
    def motorSpeed(self):
        return self._motorSpeed

    @motorSpeed.setter
    def motorSpeed(self, value):  # устанавливаем максимально возможную скорость движения, которая дальше будет
        #  изменяться в некотором диапазоне
        self._motorSpeed = min(max(0, value), 100)

