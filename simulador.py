import random
import time 
import json

from datetime import datetime, timezone

def ler_bomba():
    leitura = {
        "bomba": "P101",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "caudal_m3h": round(random.uniform(95, 105), 1),
        "pressao_bar": round(random.uniform(4.9, 5.1), 2),
        "temperatura_c": round(random.uniform(44, 46),1),
    }
    return leitura

while True: 
    mensagem = json.dumps(ler_bomba())
    print (mensagem)
    time.sleep(1)

