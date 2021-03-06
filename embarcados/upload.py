'''
Equipe IF-ELSE - Hackathon CIASC 2017
Pedro von Hertwig Batista - pedrovhb@gmail.com
================================================

Pequeno script de utilidade para upload de arquivos MicroPython via copicola.
'''


filename = 'main.py'
s = r"""

from machine import Pin
import time

led = Pin(2, Pin.OUT)

while True:
    led.value(not led.value())
    time.sleep_ms(500)
    
"""


with open(filename, 'w') as f:
    f.write(s)
