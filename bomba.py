import random
import time 
import json
from datetime import datetime, timezone

class Bomba:
    def __init__(self, nome, velocidade_hz):
        self.nome = nome
        self.velocidade_hz = velocidade_hz
        self.velocidade_nominal_hz = 50
        self.caudal_nominal_m3h = 120
        self.pressao_nominal_bar = 5.5
        self.potencia_nominal_kW = 22

    def ler(self):
        s = self.velocidade_hz / self.velocidade_nominal_hz
        caudal = self.caudal_nominal_m3h * s + random.gauss(0, 0.8)
        pressao = self.pressao_nominal_bar * s**2 + random.gauss(0, 0.03)
        potencia = self.potencia_nominal_kW * s**3 + random.gauss(0, 0.1)

        return {
            "bomba": self.nome,
            "velocidade_hz": self.velocidade_hz,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "caudal_m3h": round(caudal, 1),
            "pressao_bar": round(pressao, 2),
            "potencia_kw": round(potencia, 1)
        }

    def mudar_velocidade(self, nova_velocidade):
        self.velocidade_hz = nova_velocidade



if __name__ == "__main__":
    p101 = Bomba("P101", 50)
    p102 = Bomba("P102", 40)
    
    print(p101.ler())
    print(p102.ler())

    p101.mudar_velocidade(35)

    print(p101.ler())
    print(p102.ler())