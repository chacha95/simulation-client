import itertools
import os
import sys

import cv2
import numpy as np
from bokeh.models import ColumnDataSource, ImageURL
from bokeh.palettes import Dark2_5 as palette
from bokeh.plotting import figure, output_file, show

root_dir = os.getcwd()
sys.path.insert(1, root_dir)

from data import obstacle, vehicle


class TransScale:
    map_margin: int = 100
    trans_factor_x: int = -250
    trans_factor_y: int = -350
    scale_factor: int = 20

    @classmethod
    def get_map_margin(cls) -> int:
        return cls.map_margin

    @classmethod
    def set_map_margin(cls, map_margin: int):
        cls.map_margin = map_margin

    @classmethod
    def get_trans_factor_x(cls) -> int:
        return cls.trans_factor_x

    @classmethod
    def set_trans_factor_x(cls, trans_factor_x: int):
        cls.trans_factor_x = trans_factor_x

    @classmethod
    def get_trans_factor_y(cls) -> int:
        return cls.trans_factor_y

    @classmethod
    def set_trans_factor_y(cls, trans_factor_y: int):
        cls.trans_factor_y = trans_factor_y

    @classmethod
    def get_scale_factor(cls) -> int:
        return cls.scale_factor

    @classmethod
    def set_scale_factor(cls, scale_factor: int):
        cls.scale_factor = scale_factor


def init_map_info(img_dir, H, W) -> ColumnDataSource:
    return ColumnDataSource(dict(
        H=[H],
        W=[W],
        origin_x=[-1 * W//2],
        origin_y=[-1 * H//2],
        url=[img_dir],
    ))


def draw_map(plot, map_info) -> figure:
    # draw image
    map_img = ImageURL(url="url",
                       x="origin_x",
                       y="origin_y",
                       w="W",
                       h="H",
                       anchor="bottom_left")
    plot.add_glyph(map_info, map_img)

    # draw vehicle
    frame = 0
    # plot.circle(vehicle[0][0] + TransScale.get_trans_factor_x(),
    #             vehicle[0][1] + TransScale.get_trans_factor_y(),
    #             legend_label='vehicle',
    #             line_color= "green",
    #             fill_color="green", size=5)

    # draw obstacle
    num, _, _ = np.shape(obstacle[frame])
    colors = itertools.cycle(palette)

    trans_x = np.array([TransScale.get_trans_factor_x()] * 4)
    trans_y = np.array([TransScale.get_trans_factor_y()] * 4)
    for n, color in zip(range(num), colors):
        xs = obstacle[frame][n, :, 0] * TransScale.get_scale_factor() + trans_x
        ys = obstacle[frame][n, :, 1] * TransScale.get_scale_factor() + trans_y
        plot.multi_polygons(xs=[[[xs]]],
                            ys=[[[ys]]],
                            legend_label='obstacle',
                            line_color='blue',
                            fill_color='blue',)

    return plot


if __name__ == "__main__":
    TransScale.set_map_margin(100)
    TransScale.set_trans_factor_x(-250)
    TransScale.set_trans_factor_y(-350)
    TransScale.set_scale_factor(20)

    out_dir = f"{root_dir}/client/resources/cubetown.html"
    output_file(filename=out_dir, title="static HTML file")

    img_dir = f"{root_dir}/client/resources/cubetown_real_resize.png"
    img = cv2.imread(img_dir)
    h, w, _ = np.shape(img)
    map_info = init_map_info(img_dir, h, w)

    # create plot
    plot = figure(
        title="cube town",
        x_axis_label='x',
        y_axis_label='y',
        x_range=(-(w//2 + TransScale.get_map_margin()),
                  (w//2 + TransScale.get_map_margin())),
        y_range=(-(h//2 + TransScale.get_map_margin()),
                  (h//2 + TransScale.get_map_margin())),
    )

    plot = draw_map(plot, map_info)
    show(plot)
