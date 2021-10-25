import sys
import os
root_dir = os.getcwd()
sys.path.insert(1, root_dir)

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider, ImageURL
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Dark2_5 as palette
from bokeh.io import curdoc

from data import obstacle, vehicle
from utils import x_trans, y_trans, scale

import numpy as np
import itertools


TRANS_FACTOR_X=20
TRANS_FACTOR_Y=-270
SCALE_FACTOR=10


def init_layout(plot, source, SLIDE_VALUE=0):
    # set slider
    x_slider = Slider(start=-10, end=10, value=SLIDE_VALUE, step=1, title="x translation")
    y_slider = Slider(start=-10, end=10, value=SLIDE_VALUE, step=1, title="y translation")
    scale_slider = Slider(start=1, end=10, value=SLIDE_VALUE, step=1, title="scale")

    x_slider.js_on_change('value', x_trans(source))
    y_slider.js_on_change('value', y_trans(source))
    scale_slider.js_on_change('value', scale(source))

    layout = column(x_slider, y_slider, scale_slider, plot)
    return layout


def init_map_info(img_dir) -> ColumnDataSource:
    return ColumnDataSource(dict(
        H = [800],
        W = [800],
        origin_x = [-400], 
        origin_y = [-400],
        url = [img_dir],
    ))


def draw_map(plot, map_info):
    # draw image
    map_img = ImageURL(url="url", x="origin_x", y="origin_y", w="W", h="H", anchor="bottom_left")
    plot.add_glyph(map_info, map_img)

    # draw vehicle
    frame = 0
    plot.circle(vehicle[0][0] + TRANS_FACTOR_X, vehicle[0][1] + TRANS_FACTOR_Y, 
                legend_label='vehicle', line_color= "green", fill_color="green", size=5)

    # draw obstacle
    num, _, _ = np.shape(obstacle[frame])
    colors = itertools.cycle(palette)       

    trans_x = np.array([TRANS_FACTOR_X] * 4)
    trans_y = np.array([TRANS_FACTOR_Y] * 4)
    for n, color in zip(range(num), colors):
        xs = obstacle[frame][n, :, 0] * SCALE_FACTOR + trans_x
        ys = obstacle[frame][n, :, 1] * SCALE_FACTOR + trans_y
        plot.multi_polygons(xs=[[[xs]]], 
                         ys=[[[ys]]], 
                         legend_label='obstacle', line_color= 'blue', fill_color='blue')

    return plot


if __name__ == "__main__":
    out_dir = f"{root_dir}/client/resources/cubetown.html"
    output_file(filename=out_dir, title="static HTML file")

    # create plot
    plot = figure(
        title="cube town",
        x_axis_label='x', 
        y_axis_label='y',
        x_range=(-550, 550),
        y_range=(-550, 550),
    )

    data = {'x': np.array([0, 1]),
            'y': np.array([0, 1]),
            'nx': np.array([0, 1]),
            'ny': np.array([0, 1]),
            }

    source = ColumnDataSource(data=data)

    img_dir = f"{root_dir}/client/resources/cubetown_post_processing.png"
    map_info = init_map_info(img_dir)
    plot = draw_map(plot, map_info)
    layout = init_layout(plot, source)
    show(layout)
