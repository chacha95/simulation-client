"""
paho mqtt main function
"""

from python_mqtt.world_set import WorldSet
from data_structure.data import CustomQueue
from visualization.bokeh_visualizer import show_map
from typing import List

import paho.mqtt.client as mqtt
import numpy as np
import json
import time


class Mqtt:
    def __init__(self, topic: List[str], address: str, port: int) -> None:
        self.client: mqtt.Client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.topic: List[str] = topic
        self.address: str = address
        self.port: int = port

    def __call__(self) -> None:
        self.client.connect(self.address, self.port)
        self.client.subscribe(self.topic, 1)
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc) -> None:
        print("Connected with result code " + str(rc))
        client.subscribe(self.topic)

    def on_message(self):
        pass


class LGSVLMqtt(Mqtt):
    def __init__(
        self,
        topic: List[str],
        address: str = "localhost",
        port: int = 1883,
        world_set: WorldSet = None,
        plot=None,
        map_info=None,
        out_dir=None,
        img_dir=None,
        trans_scale=None,
        history: int = 10,
    ) -> None:
        super(LGSVLMqtt, self).__init__(topic, address, port)

        self.vehicle_que = CustomQueue(100)
        self.obstacle_que = CustomQueue(100)

        self.world_set: WorldSet = world_set
        self.plot = plot
        self.map_info = map_info
        self.out_dir = out_dir
        self.img_dir = img_dir
        self.trans_scale = trans_scale

    def on_message(self, client, userdata, msg) -> None:
        topic = msg.topic
        payload = json.loads(str(msg.payload.decode("utf-8")))
        payload["topic"] = topic
        self.parse_data(topic, payload)

        time.sleep(0.2)
        if len(self.vehicle_que) != 0 and len(self.obstacle_que) != 0:
            show_map(self.plot, self.map_info, self.vehicle_que, self.obstacle_que,
                     self.out_dir, self.img_dir, self.trans_scale)

    def parse_data(self, topic: str, payload: dict) -> None:
        try:
            if topic == "/apollo/sensor/gnss/odometry":
                x = payload["localization"]["position"]["x"] - \
                    self.world_set.get_x_0()
                y = payload["localization"]["position"]["y"] - \
                    self.world_set.get_y_0()
                v_pos = np.array([x, y])
                self.vehicle_que.push(v_pos)
            elif topic == "/apollo/perception/obstacles":
                obstacles = payload["perceptionObstacle"]
                polygons = []
                for obstacle in obstacles:
                    poly_pos = np.zeros((0, 2))
                    for pp in obstacle["polygonPoint"]:
                        x = pp["x"] - self.world_set.get_x_0()
                        y = pp["y"] - self.world_set.get_y_0()
                        poly_pos = np.vstack((poly_pos, [x, y]))
                    polygons.append(poly_pos)
                self.obstacle_que.push(np.array(polygons))
            else:
                raise Exception("topic does not existed.")
        except Exception as e:
            print(e)
