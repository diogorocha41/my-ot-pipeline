# ============ 1. IMPORTS ============
import json
import psycopg
import paho.mqtt.client as mqtt


# ============ 2. CONSTANTES (configurações e regras) ============
URL_BD = "postgresql://postgres:estacao@localhost:5433/estacao"

CAMPOS_OBRIGATORIOS = ["timestamp", "bomba", "velocidade_hz", "caudal_m3h", "pressao_bar", "potencia_kw"]

LIMITES = {
    "velocidade_hz": (0, 60),
    "caudal_m3h": (0, 200),
    "pressao_bar": (0, 10),
    "potencia_kw": (0, 40),
}


# ============ 3. FUNÇÕES ============
def validar_leitura(leitura):
    # Todos os campos obrigatórios estão lá?
    for campo in CAMPOS_OBRIGATORIOS:
        if campo not in leitura:
            return f"falta o campo '{campo}'"

    # Os valores são números, e estão dentro dos limites?
    for campo, (minimo, maximo) in LIMITES.items():
        valor = leitura[campo]

        if not isinstance(valor, (int, float)):
            return f"'{campo}' não é um número"

        if valor < minimo or valor > maximo:
            return f"'{campo}' = {valor} fora dos limites [{minimo}, {maximo}]"

    # Está tudo bem
    return None


def ao_ligar(client, userdata, flags, reason_code, properties):
    print("Ligado ao broker!")
    client.subscribe("estacao/#")


def ao_receber(client, userdata, msg):
    texto = msg.payload.decode()

    # Controlo 1: é JSON?
    try:
        leitura = json.loads(texto)
    except json.JSONDecodeError:
        print(f"Rejeitada (não é JSON): {texto}")
        return

    # Controlo 2: os dados fazem sentido?
    erro = validar_leitura(leitura)
    if erro is not None:
        print(f"Rejeitada ({erro}): {texto}")
        return

    # Passou nos dois controlos: guardar
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


# ============ 4. ARRANQUE DO PROGRAMA ============
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