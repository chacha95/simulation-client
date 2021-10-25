import sys
import os
root_dir = os.getcwd()
sys.path.insert(1, root_dir)

from bokeh.models import ColumnDataSource, CustomJS, Slider
from bokeh.plotting import figure, show, output_file
from bokeh.palettes import Dark2_5 as palette
from data import obstacle, vehicle
from bokeh.io import curdoc

import itertools  
import numpy as np


if __name__ == "__main__":
    img_dir = "client/resources/cubetown_post_processing.png"
    out_dir = "client/resources/cubetown.html"
    output_file(filename=out_dir, title="static HTML file")

    # create plot
    p = figure(
        title="cube town",
        x_axis_label='x', 
        y_axis_label='y'
    )

    # draw image
    H = W = 800
    origin = {'x': -400, 'y': -400}
    p.image_url(url=[img_dir], x=[origin['x']], y=[origin['y']], w=[W], h=[H], anchor="bottom_left")
    curdoc().add_root(p)
    

    trans_factor = (20, -270)
    scale_factor = 20

    frame = 0
    # draw obstacle
    num, _, _ = np.shape(obstacle[frame])
    colors = itertools.cycle(palette)   

    trans_x = np.array([trans_factor[0]] * 4)
    trans_y = np.array([trans_factor[1]] * 4)
    for n, color in zip(range(num), colors):
        xs = obstacle[frame][n, :, 0] * scale_factor + trans_x
        ys = obstacle[frame][n, :, 1] * scale_factor + trans_y
        p.multi_polygons(xs=[[[xs]]], 
                         ys=[[[ys]]], 
                         legend_label='obstacle', line_color= 'blue', fill_color='blue')

    # show plot
    show(p)
