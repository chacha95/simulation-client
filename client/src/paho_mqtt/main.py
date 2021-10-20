from collections import deque
from typing import List

from world_set import WorldSet
from data import Vehicle, Obstacle

import numpy as np
import paho.mqtt.client as mqtt
import json


class custom_queue():
    def __init__(self, size: int):
        self.size = size
        self.que = deque()

    def push(self, data):
        if len(self.que) == self.size:
            self.que.popleft()
        self.que.append(data)

    def pop(self):
        if len(self.que) == 0:
            print('[queue empty error]')
            exit(100)
        return self.que.popleft()


class LGSVLMqtt():
    def __init__(self, topic: List[str], address: List[str] ='localhost', port: int = 1883, history:int = 10) -> None:
        self.data = custom_queue(10)
    
        self.topic = topic
        self.address = address
        self.port = port

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def __call__(self) -> None:
        self.client.connect(self.address, self.port)
        self.client.subscribe(self.topic, 1)
        self.client.loop_forever()
    
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        topic = [("/apollo/sensor/gnss/odometry/#", 0), ("/apollo/perception/obstacles/#", 0)]
        client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        self.data.push(json.loads(str(msg.payload.decode("utf-8"))))
        topic = msg.topic
        payload = json.loads(msg.payload)
        try:
            if topic == '/apollo/sensor/gnss/odometry':
                v_pos = np.array([payload['localization']['position']['x'] - WorldSet.x_0, 
                                  payload['localization']['position']['y'] - WorldSet.y_0])
                Vehicle.add_frame(v_pos)
            elif topic == '/apollo/perception/obstacles':
                obstacles = payload['perceptionObstacle']
                polygons = []
                for obstacle in obstacles:
                    poly_pos = np.zeros((0, 2))
                    for pp in obstacle['polygonPoint']:
                        x, y = pp['x'] - WorldSet.x_0, pp['y'] - WorldSet.y_0
                        poly_pos = np.vstack((poly_pos, [x, y]))
                    polygons.append(poly_pos)
                Obstacle.add_frame(np.array(polygons))
            else:
                raise Exception("topic does not existed.")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    WorldSet.host = '192.168.10.72'
    WorldSet.port = 1883
    WorldSet.x_0 = 592759.1186
    WorldSet.y_0 = 4134482.1499
    WorldSet.topic = [("/apollo/sensor/gnss/odometry/#", 0), 
                      ("/apollo/perception/obstacles/#", 0)]

    lg_mqtt = LGSVLMqtt(topic=WorldSet.topic, address=WorldSet.host, port=WorldSet.port)
    lg_mqtt()