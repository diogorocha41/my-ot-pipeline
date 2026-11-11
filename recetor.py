import paho.mqtt.client as mqtt


def ao_ligar(client, userdata, flags, reason_code, properties):
    print("Ligado ao broker!")
    client.subscribe("estacao/#")


def ao_receber(client, userdata, msg):
    texto = msg.payload.decode()
    print(f"[{msg.topic}] {texto}")


cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
cliente.on_connect = ao_ligar
cliente.on_message = ao_receber

cliente.connect("localhost", 1883)
cliente.loop_forever()