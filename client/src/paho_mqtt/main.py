from callback import on_connect, on_message
from world_set import WorldSet
from data import Vehicle, Obstacle

import paho.mqtt.client as mqtt
import time


class LGSVLMqtt:
    def __init__(self) -> None:
        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.connect(WorldSet.host, WorldSet.port)
        
    def connect(self) -> None:
        self.client.loop_start()
        
        time.sleep(1)
        save_frame()
        
        self.client.loop_stop()


def save_frame() -> None:
    import threading
    threading.Timer(2, save_frame).start()
    print(Vehicle.frames)
    print(Obstacle.frames)


if __name__ == "__main__":
    WorldSet.host = '192.168.10.72'
    WorldSet.port = 1883

    lg_mqtt = LGSVLMqtt()
    lg_mqtt.connect()