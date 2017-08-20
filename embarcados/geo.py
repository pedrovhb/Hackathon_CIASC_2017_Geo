'''
Equipe IF-ELSE - Hackathon CIASC 2017
Pedro von Hertwig Batista - pedrovhb@gmail.com
================================================

Esse é o programa principal que vai no ESP32 embarcado no Geo, sistema de monitoramento de umidade do solo.
'''


from umqtt2 import MQTTClient
from machine import ADC, DAC, Pin
import network
import time

# LED
led = Pin(14, Pin.OUT)

# Determinar id do Geo
id_dispositivo = 4

# Conectar-se a rede WiFi predefinida
sta_if = network.WLAN(network.STA_IF)
sta_ssid = 'IF-ELSE'
sta_pwd = 'hackathon2017'
sta_if.active(True)
sta_if.connect(sta_ssid, sta_pwd)

# Esperar conexão
while not sta_if.isconnected():
    led.value(not led.value())
    time.sleep_ms(250)

# Conectar-se ao broker MQTT
c = MQTTClient("geo-1", '13.82.145.247')
c.connect()

# Criar e configurar saída digital-analógica para alimentação
# do higrômetro (entrada analógica-digital suporta no máximo 1V)
# Porta G25
higrometro_alimentacao = DAC(Pin(25, Pin.OUT))
higrometro_alimentacao.write(int(255/3.3))

# Configurar pino de leitura do higrômetro
# Porta G32
higrometro_leitura = ADC(Pin(32, Pin.IN))

# Configurar tempo entre leituras, em ms
periodo_aquisicao = 1000

# Loop principal
while True:
    # Aqui deve-se fazer uma calibração de acordo com o solo sendo lido para traduzir o valor lido em decorrência
    # da resistência oferecida pelo higrômetro em valores reais de umidade. Como ainda não pudemos fazer essa
    # calibração, publicamos os valores brutos lidos.
    c.publish('/monitoramento/geo-{}'.format(id_dispositivo), str(higrometro_leitura.read()))
    time.sleep_ms(periodo_aquisicao)
    led.value(time.tick_ms()%500>250)


