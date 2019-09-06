import time

from pult.joystick import Joystick
from pult import control
from pult import config

joystick = Joystick()
joystick.open("/dev/input/js0")
print(joystick)

control = control.Control()
control.setJoystick(joystick)

try:
    control.robot.connect(config.IP, config.PORT)
except Exception as e:
    raise ConnectionError("Не удалось подключиться к ", config.IP, str(e))

joystick.start()
control.start()

while True:     # бесконечный цикл
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        control.exit()
        joystick.exit()
        break

