import contextlib
import time
import paho.mqtt.client as mqtt

feedback = False

def send_wol_command(broker: str, topic_command: str, topic_feedback: str) -> bool:
    global feedback
    feedback = False

    def on_message(client, userdata, message):
        global feedback
        payload = message.payload.decode()
        if payload == "WOL_ENVIADO:SUCESSO":
            feedback = True

    def try_broker_connection(client: mqtt.Client, broker: str, topic_feedback: str):
        try:
            client.connect(broker, 1883, 60)
            client.loop_start()
            client.subscribe(topic_feedback, qos=1)
            time.sleep(1)
            return True
        except Exception as e:
            return False

    client = mqtt.Client(userdata={'broker': broker})
    client.on_message = on_message

    if not try_broker_connection(client, broker, topic_feedback):
        return False
    try:
        client.publish(topic_command, "ON", qos=1)

        timeout = time.time() + 12
        while time.time() < timeout and not feedback:
            time.sleep(0.1)

        return feedback

    except Exception as e:
        return False
    finally:
        client.loop_stop()
        with contextlib.suppress(Exception):
            client.disconnect()