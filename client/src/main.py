"""
this script is main script for mqtt subscriber and bokeh visualizer.
"""
from typing import List

import sys
import os
import cv2
import numpy as np

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

from scheme.mqtt import WorldSet, TransScale, LGSVLMqttInfo
from visualization.bokeh_visualizer import init_map_info
from python_mqtt.mqtt import LGSVLMqtt
from utils.util import rot_mat


sys.path.append(os.getcwd())


class InitEnvironment:
    def __init__(self) -> None:
        # mqtt
        self.address: str = None
        self.port: int = None
        self.topic: List[tuple] = None
        # map
        self.out_dir: str = None
        self.img_dir: str = None
        self.img: np.ndarray = None
        self.h: int = None
        self.w: int = None
        self.map_info: ColumnDataSource = None
        # translation
        self.world_set: WorldSet = None
        self.trans: TransScale = None
        # bokeh
        self.plot = None

    def init_mqtt(self, address: str, port: int, topic: List[tuple]) -> None:
        self.address = address
        self.port = port
        self.topic = topic

    def init_map(self, out_dir: str, img_dir: str) -> None:
        self.out_dir = out_dir
        self.img_dir = img_dir
        self.img = cv2.imread(img_dir)
        self.h, self.w, _ = np.shape(self.img)
        self.map_info = init_map_info(self.img_dir, self.h, self.w)

    def init_trans(self, trans_data: dict) -> None:
        world_set_data = {
            "x_0": trans_data["x_0"],
            "y_0": trans_data["y_0"],
        }
        self.world_set = WorldSet(**world_set_data)

        trans_data = {
            "trans_factor_x": trans_data["trans_factor_x"] + self.w // 2,
            "trans_factor_y": trans_data["trans_factor_y"] + self.h // 2,
            "scale_factor": trans_data["scale_factor"],
            "rot_mat": rot_mat(trans_data["rotation"]),
            "map_margin": trans_data["map_margin"],
        }
        self.trans = TransScale(**trans_data)

    def init_bokeh(self) -> None:
        self.plot = figure(
            title="cube town",
            x_axis_label="x",
            y_axis_label="y",
            x_range=(
                0,
                (self.w + self.trans.map_margin),
            ),
            y_range=(
                0,
                (self.h + self.trans.map_margin),
            ),
        )

    def get_data(self) -> dict:
        return {
            "topic": self.topic,
            "address": self.address,
            "port": self.port,
            "world_set": self.world_set,
            "plot": self.plot,
            "map_info": self.map_info,
            "out_dir": self.out_dir,
            "img_dir": self.img_dir,
            "trans_scale": self.trans,
        }


if __name__ == "__main__":
    env = InitEnvironment()

    # init mqtt environment
    address = "192.168.10.145"
    port = 1883
    topic = [
        ("/apollo/sensor/gnss/odometry/#", 0),
        ("/apollo/perception/obstacles/#", 0),
    ]
    env.init_mqtt(address, port, topic)

    # init map environment
    root_dir = "/home/cha/simulation-client"
    out_dir = f"{root_dir}/client/resources/cubetown.html"
    img_dir = f"{root_dir}/client/resources/cubetown_line.png"
    env.init_map(out_dir, img_dir)

    # init translation, scale, rotation
    trans_data = {
        "x_0": 592759.1186,
        "y_0": 4134482.1499,
        "trans_factor_x": 32,
        "trans_factor_y": -373,
        "scale_factor": 9.5,
        "rotation": -90,
        "map_margin": 100,
    }
    env.init_trans(trans_data)

    # init bokeh environment
    env.init_bokeh()

    lgsvl_mqtt_info = LGSVLMqttInfo(**env.get_data())
    lg_mqtt = LGSVLMqtt(lgsvl_mqtt_info)
    lg_mqtt()
