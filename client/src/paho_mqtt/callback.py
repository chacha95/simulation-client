from world_set import WorldSet
from data import Obstacle, Vehicle

import numpy as np
import json


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    topic = [("/apollo/sensor/gnss/odometry/#", 0), ("/apollo/perception/obstacles/#", 0)]
    client.subscribe(topic)


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = json.loads(msg.payload)
    try:
        if topic == '/apollo/sensor/gnss/odometry':
            v_pos = np.array([payload['localization']['position']['x'] - WorldSet.x_0, 
                              payload['localization']['position']['y'] - WorldSet.y_0])
            Vehicle.add_frame(v_pos)
        elif topic == '/apollo/perception/obstacles':
            obstacles = payload['perceptionObstacle']
            # chagne to np.array
            
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