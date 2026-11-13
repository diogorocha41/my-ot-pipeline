import json
import psycopg
import paho.mqtt.client as mqtt


def ao_ligar(client, userdata, flags, reason_code, properties):
    print("Ligado ao broker!")
    client.subscribe("estacao/#")


def ao_receber(client, userdata, msg):
    texto = msg.payload.decode()
    leitura = json.loads(texto)

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO leituras (time, bomba, velocidade_hz, caudal_m3h, pressao_bar, potencia_kw)
            VALUES (%s, %s, %s, %s, %s, %s);
            """,
            (
                leitura["timestamp"],
                leitura["bomba"],
                leitura["velocidade_hz"],
                leitura["caudal_m3h"],
                leitura["pressao_bar"],
                leitura["potencia_kw"],
            ),
        )

    print(f"Guardado: {leitura['bomba']} {leitura['caudal_m3h']} m3/h")

URL_BD = "postgresql://postgres:estacao@localhost:5433/estacao"
conn = psycopg.connect(URL_BD, autocommit=True)

cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
cliente.on_connect = ao_ligar
cliente.on_message = ao_receber

cliente.connect("localhost", 1883)
try:
    cliente.loop_forever()
except KeyboardInterrupt:
    print("Recetor parado.")
    cliente.disconnect()
    conn.close()