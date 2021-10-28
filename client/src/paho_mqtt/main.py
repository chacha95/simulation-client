"""
paho mqtt main function
"""

import json
import os
import sys
from collections import deque
from typing import List

import numpy as np
import paho.mqtt.client as mqtt

root_dir = os.getcwd()
sys.path.append(root_dir)

from data import Obstacle, Vehicle
from world_set import WorldSet


class CustomQueue():
    def __init__(self, size: int):
        self.size: int = size
        self.que: deque = deque()

    def push(self, data):
        if len(self.que) == self.size:
            self.que.popleft()
        self.que.append(data)

    def pop(self):
        if len(self.que) == 0:
            print('[queue empty error]')
            sys.exit()
        return self.que.popleft()


class LGSVLMqtt():
    def __init__(self,
                 topic: List[str],
                 address: str = 'localhost',
                 port: int = 1883,
                 history: int = 10) -> None:

        self.data: CustomQueue = CustomQueue(10)

        self.topic: List[str] = topic
        self.address: str = address
        self.port: int = port

        self.client: mqtt.Client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def __call__(self) -> None:
        self.client.connect(self.address, self.port)
        self.client.subscribe(self.topic, 1)
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        topic = [("/apollo/sensor/gnss/odometry/#", 0),
                 ("/apollo/perception/obstacles/#", 0)]
        client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        self.data.push(json.loads(msg))
        parse_data(self.data.pop().topic, self.data.pop().payload)


def parse_data(topic, payload):
    try:
        if topic == '/apollo/sensor/gnss/odometry':
            nx = payload['localization']['position']['x'] - WorldSet.get_x_0()
            ny = payload['localization']['position']['y'] - WorldSet.get_y_0()
            v_pos = np.array([nx, ny])
            Vehicle.add_frame(v_pos)
        elif topic == '/apollo/perception/obstacles':
            obstacles = payload['perceptionObstacle']
            polygons = []
            for obstacle in obstacles:
                poly_pos = np.zeros((0, 2))
                for pp in obstacle['polygonPoint']:
                    x = pp['x'] - WorldSet.get_x_0()
                    y = pp['y'] - WorldSet.get_y_0()
                    poly_pos = np.vstack((poly_pos, [x, y]))
                polygons.append(poly_pos)
            Obstacle.add_frame(np.array(polygons))
        else:
            raise Exception("topic does not existed.")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    WorldSet.set_host('192.168.10.72')
    WorldSet.set_port(1883)
    WorldSet.set_x_0(592759.1186)
    WorldSet.set_y_0(4134482.1499)
    WorldSet.set_topic([("/apollo/sensor/gnss/odometry/#", 0),
                        ("/apollo/perception/obstacles/#", 0)])
    lg_mqtt = LGSVLMqtt(topic=WorldSet.get_topic(),
                        address=WorldSet.get_host(),
                        port=WorldSet.get_port())
    lg_mqtt()
