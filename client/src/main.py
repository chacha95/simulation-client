"""
this script is main script for mqtt subscriber and bokeh visualizer.
"""
from typing import Any, List

import sys
import os
import cv2
import numpy as np

from bokeh.plotting import figure

from scheme.mqtt import WorldSet, TransScale, LGSVLMqttInfo
from visualization.bokeh_visualizer import init_map_info
from python_mqtt.mqtt import LGSVLMqtt
from utils.util import rot_mat


sys.path.append(os.getcwd())


def init_bokeh() -> Any:
    """
    init bokeh information.
    this function can control visualization factors(about bokeh)
    """

    # map info
    root_dir = "/home/cha/simulation-client"
    out_dir = f"{root_dir}/client/resources/cubetown.html"
    img_dir = f"{root_dir}/client/resources/cubetown_real_resize.png"
    img = cv2.imread(img_dir)
    h, w, _ = np.shape(img)
    map_info = init_map_info(img_dir, h, w)

    # translation info
    trans_scale_data = {
        "map_margin": 100,
        "trans_factor_x": 32 + w // 2,
        "trans_factor_y": -373 + h // 2,
        "scale_factor": 9.5,
        "rot_mat": rot_mat(-90),
    }
    trans_scale = TransScale(**trans_scale_data)

    # create plot
    plot = figure(
        title="cube town",
        x_axis_label="x",
        y_axis_label="y",
        x_range=(
            0,
            (w + trans_scale.map_margin),
        ),
        y_range=(
            0,
            (h + trans_scale.map_margin),
        ),
    )

    return plot, map_info, out_dir, img_dir, trans_scale


def init_env(topic: List[tuple], address: str, port: int) -> dict():
    """
    init environment settings.
    e.g. host, port ....
    """
    # WorldSet info settting
    world_set_data = {
        "x_0": 592759.1186,
        "y_0": 4134482.1499,
    }
    world_set = WorldSet(**world_set_data)

    plot, map_info, out_dir, img_dir, trans_scale = init_bokeh()

    return {
        "topic": topic,
        "address": address,
        "port": port,
        "world_set": world_set,
        "plot": plot,
        "map_info": map_info,
        "out_dir": out_dir,
        "img_dir": img_dir,
        "trans_scale": trans_scale,
    }


if __name__ == "__main__":
    topic = [
        ("/apollo/sensor/gnss/odometry/#", 0),
        ("/apollo/perception/obstacles/#", 0),
    ]
    address = "192.168.10.145"
    port = 1883
    data = init_env(topic, address, port)
    lgsvl_mqtt_info = LGSVLMqttInfo(**data)

    lg_mqtt = LGSVLMqtt(lgsvl_mqtt_info)
    lg_mqtt()
