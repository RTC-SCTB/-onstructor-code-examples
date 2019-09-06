#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Сервер, установленный на малине """
from bot import config
from bot.control import Control
import time


control = Control()

control.connectToEvent(config.turnForward, "turnForward")
control.connectToEvent(config.turnAll, "turnAll")
control.connectToEvent(config.rotate, "rotate")
control.connectToEvent(config.move, "move")
control.connectToEvent(config.setCamera, "setCamera")

try:
    control.connect('', config.PORT)
except Exception as e:
    raise ConnectionError("Не удалось подключиться к ", (config.IP, config.PORT), str(e))

while True:     # бесконечный цикл
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        control.disconnect()
        break
