from flask import Flask, send_file
import json
import sqlite3

import random


app = Flask(__name__)
conn = sqlite3.connect('dados.db')

@app.route("/")
def index():
    return send_file('web/index.html')

@app.route("/web/tablestyles.css")
def table_styles():
    return send_file('web/tablestyles.css')




@app.route("/update")
def update():
    cur = conn.cursor()
    cur.execute(
'''
SELECT DISTINCT Umidade.valor, Umidade.horario, Dispositivos.localizacao, Dispositivos.id  
                    FROM Umidade JOIN Dispositivos
                        ON Dispositivos.id = Umidade.id_dispositivo 
				GROUP BY Umidade.id_dispositivo
                ORDER BY Umidade.id_dispositivo DESC, Umidade.horario DESC
                LIMIT 4
'''
                )
    data = [list(tup) for tup in cur.fetchall()]
    print(data)

    cur.close()

    return json.dumps(data)

app.run('0.0.0.0')
