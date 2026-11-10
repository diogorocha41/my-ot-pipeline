import random
import time 
import json
from datetime import datetime, timezone

class Bomba:
    def __init__(self, nome, velocidade_hz):
        self.nome = nome
        self.velocidade_hz = velocidade_hz

    def ler(self):
        return {
            "bomba": self.nome,
            "velocidade_hz": self.velocidade_hz,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "caudal_m3h": round(random.uniform(95, 105), 1),
        }

    def mudar_velocidade(self, nova_velocidade):
        self.velocidade_hz = nova_velocidade


p101 = Bomba("P101", 50)
p102 = Bomba("P102", 40)

print(p101.ler())
print(p102.ler())

p101.mudar_velocidade(35)

print(p101.ler())
print(p102.ler())