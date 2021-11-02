from visualization.bokeh_visualizer import TransScale, init_map_info, figure
from data_structure.world_set import WorldSet
from data_structure.data import LGSVLMqttInfo
from python_mqtt.mqtt import LGSVLMqtt

import numpy as np
import cv2
import sys
import os

root_dir = os.getcwd()
sys.path.append(root_dir)


if __name__ == "__main__":
    # LGSVL
    world_set = WorldSet()
    world_set.set_x_0(592759.1186)
    world_set.set_y_0(4134482.1499)

    # bokeh visualizer
    root_dir = "/home/cha/simulation-client"
    out_dir = f"{root_dir}/client/resources/cubetown.html"
    img_dir = f"{root_dir}/client/resources/cubetown_real_resize.png"

    trans_scale = TransScale()
    trans_scale.set_map_margin(100)
    trans_scale.set_trans_factor_x(30)
    trans_scale.set_trans_factor_y(-350)
    trans_scale.set_scale_factor(10)

    # read map image
    img = cv2.imread(img_dir)
    h, w, _ = np.shape(img)
    map_info = init_map_info(img_dir, h, w)

    # create plot
    plot = figure(
        title="cube town",
        x_axis_label="x",
        y_axis_label="y",
        x_range=(
            -(w // 2 + trans_scale.get_map_margin()),
            (w // 2 + trans_scale.get_map_margin()),
        ),
        y_range=(
            -(h // 2 + trans_scale.get_map_margin()),
            (h // 2 + trans_scale.get_map_margin()),
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
