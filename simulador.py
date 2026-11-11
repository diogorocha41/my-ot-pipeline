import random
import time 
import json
from bomba import Bomba
import paho.mqtt.client as mqtt

cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
cliente.connect("localhost", 1883)
cliente.loop_start()

bombas = [Bomba("P101", 50), Bomba("P102", 45), Bomba("P103", 40)]

try:
    while True: 
        for bomba in bombas:
            if random.random () < 0.1:
                bomba.mudar_velocidade(random.randint(35, 50))
            mensagem = json.dumps(bomba.ler())
            topico = f"estacao/{bomba.nome}/telemetria"
            cliente.publish(topico, mensagem)
            print(f"Publicado em {topico}")
        time.sleep(1)
except KeyboardInterrupt:
    print ("Simulador parado.")
    cliente.loop_stop()
    cliente.disconnect()
