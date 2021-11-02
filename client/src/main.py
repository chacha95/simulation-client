from bokeh.plotting import figure

from python_mqtt.mqtt import LGSVLMqtt
from visualization.bokeh_visualizer import init_map_info
from scheme.mqtt import WorldSet, TransScale, LGSVLMqttInfo

import numpy as np
import cv2
import sys
import os

root_dir = os.getcwd()
sys.path.append(root_dir)


if __name__ == "__main__":
    # WorldSet info settting
    world_set_data = {
        'x_0': 592759.1186,
        'y_0': 4134482.1499,
    }
    world_set = WorldSet(**world_set_data)

    # bokeh visualizer
    trans_scale_data = {
        'map_margin': 100,
        'trans_factor_x': 30,
        'trans_factor_y': -350,
        'scale_factor': 10,
    }
    trans_scale = TransScale(**trans_scale_data)

    # read map image
    root_dir = "/home/cha/simulation-client"
    out_dir = f"{root_dir}/client/resources/cubetown.html"
    img_dir = f"{root_dir}/client/resources/cubetown_real_resize.png"
    img = cv2.imread(img_dir)
    h, w, _ = np.shape(img)
    map_info = init_map_info(img_dir, h, w)

    # create plot
    plot = figure(
        title="cube town",
        x_axis_label="x",
        y_axis_label="y",
        x_range=(
            -(w // 2 + trans_scale.map_margin),
            (w // 2 + trans_scale.map_margin),
        ),
        y_range=(
            -(h // 2 + trans_scale.map_margin),
            (h // 2 + trans_scale.map_margin),
        ),
    )

    lgsvlmqtt_data = {
        'topic': [("/apollo/sensor/gnss/odometry/#", 0),
                  ("/apollo/perception/obstacles/#", 0)],
        'address': "192.168.10.145",
        'port': 1883,
        'world_set': world_set,
        'plot': plot,
        'map_info': map_info,
        'out_dir': out_dir,
        'img_dir': img_dir,
        'trans_scale': trans_scale
    }

    lgsvl_mqtt_info = LGSVLMqttInfo(**lgsvlmqtt_data)
    lg_mqtt = LGSVLMqtt(lgsvl_mqtt_info)
    lg_mqtt()
