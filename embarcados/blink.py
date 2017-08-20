'''
Equipe IF-ELSE - Hackathon CIASC 2017
Pedro von Hertwig Batista - pedrovhb@gmail.com
================================================

Pisca pisca de testes.
'''

from machine import Pin
import time

led = machine.Pin(2, Pin.OUT)

while True:
    led.value(not led.value())
    time.sleep_ms(500)