import random
import time 
import json
from bomba import Bomba

bombas = [Bomba("P101", 50), Bomba("P102", 45), Bomba("P103", 40)]

try:
    while True: 
        for bomba in bombas:
            if random.random () < 0.1:
                bomba.mudar_velocidade(random.randint(35, 50))
            mensagem = json.dumps(bomba.ler())
            print (mensagem)
        time.sleep(1)
except KeyboardInterrupt:
    print ("Simulador parado.")

