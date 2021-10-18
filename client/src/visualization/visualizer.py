from bokeh.io import curdoc
from bokeh.plotting import figure, show
from bokeh.palettes import Dark2_5 as palette
from data import obstacle, vehicle

import itertools  
import numpy as np


H = W = 800
scale_factor = 10
origin = {'x': -400, 'y': -400}


if __name__ == "__main__":
    root_dir = "/home/cha/simulation-client/client/resources"
    img_dir = f"{root_dir}/cubtwon_post_processing.png"

    # create plot
    p = figure(title="cube town", x_axis_label='x', y_axis_label='y')

    # draw image
    p.image_url(url=[img_dir], x=[origin['x']], y=[origin['y']], w=[W], h=[H], anchor="bottom_left")
    curdoc().add_root(p)

    trans_factor = (20, -270)
    scale_factor = 8

    # draw vehicle
    frame = 0
    p.circle(vehicle[0][0] + trans_factor[0], vehicle[0][1] + trans_factor[1], legend_label='vehicle', line_color= "green", fill_color="green", size=5)

    # draw obstacle
    num, _, _ = np.shape(obstacle[frame])
    colors = itertools.cycle(palette)

    trans_mat = np.array([trans_factor[1], trans_factor[1], trans_factor[1], trans_factor[1]])
    for n, color in zip(range(num), colors):
        xs = obstacle[frame][n, :, 0] * scale_factor 
        ys = obstacle[frame][n, :, 1] * scale_factor + trans_mat
        p.multi_polygons(xs=[[[xs]]], 
                         ys=[[[ys]]], 
                         legend_label='obstacle', line_color= 'blue', fill_color='blue')

    # show plot
    show(p)