from threading import Thread, Event
from queue import Queue
import time
from typing import Optional
from paho.mqtt.client import Client, MQTTMessage

def check_connection(brokers: list[str], topic_feedback: str, timeout: int = 20) -> Optional[str]:
    result_queue = Queue()
    done_event = Event()

    def listener(broker: str):
        def on_message(client: Client, userdata, msg: MQTTMessage):
            payload = msg.payload.decode().strip()
            if payload == "PING:ONLINE":
                if not done_event.is_set():
                    result_queue.put(broker)
                    done_event.set()
                    client.disconnect()

        client = Client()
        client.on_message = on_message

        try:
            client.connect(broker, 1883, 60)
            client.subscribe(topic_feedback)
            client.loop_start()

            start = time.time()
            while not done_event.is_set() and time.time() - start < timeout:
                time.sleep(0.1)

            client.loop_stop()
            client.disconnect()
        except:
            pass

    for broker in brokers:
        Thread(target=listener, args=(broker,), daemon=True).start()
    try:
        broker_found = result_queue.get(timeout=timeout)
        return broker_found
    except:
        return None