"""
paho mqtt function
"""
from typing import List
import json
import numpy as np
import paho.mqtt.client as mqtt

from visualization.bokeh_visualizer import show_map

from scheme.mqtt import WorldSet
from scheme.mqtt import CustomQueue, DrawMapInfo, LGSVLMqttInfo


class Mqtt:
    """
    Basic Mqtt class
    """

    def __init__(self, topic: List[str], address: str, port: int) -> None:
        self.client: mqtt.Client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.topic: List[str] = topic
        self.address: str = address
        self.port: int = port

    def __call__(self) -> None:
        """
        subscribe loop forever
        """
        self.client.connect(self.address, self.port)
        self.client.subscribe(self.topic, 1)
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc) -> None:
        """
        start subscribe
        """
        print("Connected with result code " + str(rc))
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        pass


class LGSVLMqtt(Mqtt):
    """
    LGSVL Mqtt Subscriber

    Args:
        lgsvl_info (LGSVLMqttInfo): information for lgsvl subscriber and bokeh visualizer
    """

    def __init__(self, lgsvl_info: LGSVLMqttInfo) -> None:
        super().__init__(lgsvl_info.topic, lgsvl_info.address, lgsvl_info.port)

        self.vehicle_que = CustomQueue(100)
        self.obstacle_que = CustomQueue(100)

        self.world_set: WorldSet = lgsvl_info.world_set
        self.plot = lgsvl_info.plot
        self.map_info = lgsvl_info.map_info
        self.out_dir = lgsvl_info.out_dir
        self.img_dir = lgsvl_info.img_dir
        self.trans_scale = lgsvl_info.trans_scale

    def on_message(self, client, userdata, msg) -> None:
        """
        subscribe mqtt message

        Args:
            client:
            userdata:
            msg: message from mqtt publisher
        """
        topic = msg.topic
        payload = json.loads(str(msg.payload.decode("utf-8")))
        payload["topic"] = topic
        self.parse_data(topic, payload)

        if len(self.vehicle_que) != 0 and len(self.obstacle_que) != 0:
            draw_map_data = {
                "vehicle_que": self.vehicle_que,
                "obstacle_que": self.obstacle_que,
                "plot": self.plot,
                "map_info": self.map_info,
                "trans_scale": self.trans_scale,
                "out_dir": self.out_dir,
                "img_dir": self.img_dir,
            }
            draw_map_info = DrawMapInfo(**draw_map_data)
            show_map(draw_map_info)

    def parse_data(self, topic: str, payload: dict) -> None:
        """
        parse mqtt message

        Args:
            topic: topic in message
            payload: payload(body) in message
        """
        try:
            if topic == "/apollo/sensor/gnss/odometry":
                x = payload["localization"]["position"]["x"] - self.world_set.x_0
                y = payload["localization"]["position"]["y"] - self.world_set.y_0
                v_pos = np.array([x, y])
                self.vehicle_que.push(v_pos)
            elif topic == "/apollo/perception/obstacles":
                obstacles = payload["perceptionObstacle"]
                ids, polygons = [], []
                for obstacle in obstacles:
                    # add id
                    id = obstacle["id"]
                    ids.append(id)
                    # add polygon points
                    poly_pos = np.zeros((0, 2))
                    for pp in obstacle["polygonPoint"]:
                        x = pp["x"] - self.world_set.x_0
                        y = pp["y"] - self.world_set.y_0
                        poly_pos = np.vstack((poly_pos, [x, y]))
                    polygons.append(poly_pos)
                # tuple(list, np.ndarray)
                self.obstacle_que.push((ids, np.array(polygons)))
            else:
                raise Exception("topic does not existed.")
        except Exception as e:
            print(e)
