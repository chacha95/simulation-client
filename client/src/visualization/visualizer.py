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
    img_dir = '/home/cha/py-mongo/client/resources/cubetown_white.png'

    # create plot
    p = figure(title="cube town", x_axis_label='x', y_axis_label='y')

    # draw image
    p.image_url(url=[img_dir], x=[origin['x']], y=[origin['y']], w=[W], h=[H], anchor="bottom_left")
    curdoc().add_root(p)

    # draw vehicle
    frame = 0
    p.circle(0, -400, legend_label='vehicle', line_color= "green", fill_color="green", size=5)

    # draw obstacle
    num, _, _ = np.shape(obstacle[frame])
    colors = itertools.cycle(palette)
    for n, color in zip(range(num), colors):
        xs = obstacle[frame][n, :, 0] * 8
        ys = obstacle[frame][n, :, 1] * 8
        p.multi_polygons(xs=[[[xs]]], 
                         ys=[[[ys]]], 
                         legend_label='obstacle', line_color= 'blue', fill_color='blue')

    # show plot
    show(p)