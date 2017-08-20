'''
Equipe IF-ELSE - Hackathon CIASC 2017
Pedro von Hertwig Batista - pedrovhb@gmail.com
================================================

Esse código é o 'consumidor' das mensagens MQTT provindas de cada Geo. Ele se inscreve nos tópicos de monitoramento
e joga os dados relevantes em um banco de dados, que também contém tabela com identificação mais precisa
sobre a localização de cada dispositivo.
'''


from datetime import datetime
import paho.mqtt.client as mqtt
import sqlite3

# Callback de conexão.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/monitoramento/#")


# Callback de quando uma mensagem é recebida.
def on_message(client, userdata, msg):
    geo_id = int(msg.topic.split('-')[-1])     # Pegar a identificação do dispositivo
    valor = float(msg.payload)                 # Pegar valor lido pelo Geo
    dt = datetime.now()

    cur = conn.cursor()
    cur.execute('INSERT INTO Umidade (valor, horario, id_dispositivo) VALUES (?, ?, ?)',
                (valor, dt.__str__(), geo_id))
    conn.commit()
    cur.close()




# Instanciar e conectar cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("13.82.145.247", 1883, 60)

# Instanciar conexão com banco de dados
conn = sqlite3.connect('dados.db')

# Função blocante que espera eternamente por mensagens e as processa com o callback setado.
client.loop_forever()