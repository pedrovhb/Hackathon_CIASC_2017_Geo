'''
Equipe IF-ELSE - Hackathon CIASC 2017
Pedro von Hertwig Batista - pedrovhb@gmail.com
================================================

Programa para o microcontrolador embarcado na sirene de aviso de desastre iminente.
Projetado para ESP8266 com MicroPython.
'''


from umqtt2 import MQTTClient
from machine import Pin
import network
import time

# Determinar id da Sirene
id_dispositivo = 1

# Conectar-se a rede WiFi predefinida
sta_if = network.WLAN(network.STA_IF)
sta_ssid = 'IF-ELSE'
sta_pwd = 'hackathon2017'
sta_if.active(True)
sta_if.connect(sta_ssid, sta_pwd)

# Esperar conexão
while not sta_if.isconnected():
    time.sleep_ms(100)

# Definir callback ao receber um alerta
def mensagem_recebida(topico, payload):
    print('Alerta!')
    # Guardar tempo de início da mensagem
    comeco = time.ticks_ms()

    # Enquanto o valor da sirene não for atingido, alternamos os leds vermelho e azul
    while comeco + tempo_sirene > time.ticks_ms():
        led_vermelho.value(time.tick_ms() % 500 > 250)
        led_azul.value(time.tick_ms() % 500 <= 250)


# Conectar-se ao broker MQTT
c = MQTTClient("sirene-{}".format(id_dispositivo), '13.82.145.247')
c.connect()
c.set_callback(mensagem_recebida)
c.subscribe('/alertas/sirene-1')

# Para fins de simulação, alternaremos dois LEDs para indicar acionamento da sirene.
# Aqui declaram-se os LEDs.
led_vermelho = Pin(4, Pin.OUT)  # D2
led_azul = Pin(5, Pin.OUT)  # D1

# Tempo pelo qual a sirene deve soar, em ms
tempo_sirene = 3000

# Loop principal; só esperamos por mensagens (ação é executada no callback definido acima)
print('Esperando...')
while True:
    c.wait_msg()

