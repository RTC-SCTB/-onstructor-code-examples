#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import time
from PIL import Image       # библиотеки для рисования на дисплее
from PIL import ImageDraw
from PIL import ImageFont
import Adafruit_SSD1306

time.sleep(10)

file = subprocess.Popen(["cat", "/etc/hostapd/hostapd.conf"], stdout=subprocess.PIPE)
ssid = subprocess.Popen(["grep", "-w", "ssid"], stdin=file.stdout, stdout=subprocess.PIPE).stdout.read().decode("utf-8")
ssid = ssid.split('=')[1].split()

file = subprocess.Popen(["cat", "/etc/hostapd/hostapd.conf"], stdout=subprocess.PIPE)
psw = subprocess.Popen(["grep", "wpa_passphrase"], stdin=file.stdout, stdout=subprocess.PIPE).stdout.read().decode("utf-8")
psw = psw.split('=')[1].split()

cmd = 'hostname -I'
ip = subprocess.check_output(cmd, shell=True).decode("utf-8")     # получаем IP
ip = ip.split()     # удаляем \n, переводим в текст

disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)
disp.begin()    # запускаем дисплей
disp.clear()    # очищаем буффер изображения
width, height = disp.width, disp.height  # получаем высоту и ширину дисплея

image = Image.new('1', (width, height))     # создаем изображение из библиотеки PIL для вывода на экран
draw = ImageDraw.Draw(image)    # создаем объект, которым будем рисовать
top = -2    # сдвигаем текст вверх на 2 пикселя
x = 0   # сдвигаем весь текст к левому краю
font = ImageFont.load_default()     # загружаем стандартный шрифт


draw.rectangle((0, 0, width, height), outline=0, fill=0)  # прямоугольник, залитый черным - очищаем дисплей
draw.text((x, top), "ssid: " + ssid[0], font=font, fill=255)        # формируем текст
draw.text((x, top + 8), "psw: " + psw[0], font=font, fill=255)     # высота строки - 8 пикселей

for i in range(len(ip)):
    draw.text((x, top + 16 + 8*i), "ip: " + ip[i], font=font, fill=255)

disp.image(image)   # записываем изображение в буффер
disp.display()      # выводим его на экран
