from bokeh.models import ColumnDataSource, ImageURL
from bokeh.palettes import Dark2_5 as palette
from bokeh.plotting import figure, output_file, show

import numpy as np
import itertools
import cv2


class TransScale:
    def __init__(self) -> None:
        self.map_margin: int
        self.trans_factor_x: int
        self.trans_factor_y: int
        self.scale_factor: int

    def get_map_margin(self) -> int:
        return self.map_margin

    def set_map_margin(self, map_margin: int):
        self.map_margin = map_margin

    def get_trans_factor_x(self) -> int:
        return self.trans_factor_x

    def set_trans_factor_x(self, trans_factor_x: int):
        self.trans_factor_x = trans_factor_x

    def get_trans_factor_y(self) -> int:
        return self.trans_factor_y

    def set_trans_factor_y(self, trans_factor_y: int):
        self.trans_factor_y = trans_factor_y

    def get_scale_factor(self) -> int:
        return self.scale_factor

    def set_scale_factor(self, scale_factor: int):
        self.scale_factor = scale_factor


def init_map_info(img_dir: str, H: int, W: int) -> ColumnDataSource:
    return ColumnDataSource(
        dict(
            H=[H],
            W=[W],
            origin_x=[-1 * W // 2],
            origin_y=[-1 * H // 2],
            url=[img_dir],
        )
    )


def draw_map(vehicle,
             obstacle,
             plot: figure,
             map_info: ColumnDataSource(dict()),
             trans_scale: TransScale,
             ) -> figure:
    # draw image
    map_img = ImageURL(
        url="url", x="origin_x", y="origin_y", w="W", h="H", anchor="bottom_left"
    )
    plot.add_glyph(map_info, map_img)

    # draw vehicle
    plot.circle(vehicle[0] + trans_scale.get_trans_factor_x(),
                vehicle[1] + trans_scale.get_trans_factor_y(),
                legend_label='vehicle',
                line_color="green",
                fill_color="green", size=5)

    # draw obstacle
    num, _, _ = np.shape(obstacle)
    colors = itertools.cycle(palette)

    trans_x = np.array([trans_scale.get_trans_factor_x()] * 4)
    trans_y = np.array([trans_scale.get_trans_factor_y()] * 4)
    for n, color in zip(range(num), colors):
        xs = obstacle[n, :, 0] * \
            trans_scale.get_scale_factor() + trans_x
        ys = obstacle[n, :, 1] * \
            trans_scale.get_scale_factor() + trans_y
        plot.multi_polygons(
            xs=[[[xs]]],
            ys=[[[ys]]],
            legend_label="obstacle",
            line_color="blue",
            fill_color="blue",
        )

    return plot


def show_map(plot,
             map_info,
             vehicle_que,
             obstacle_que,
             out_dir: str,
             img_dir: str,
             trans_scale: TransScale) -> None:
    output_file(filename=out_dir, title="static HTML file")

    vehicle = vehicle_que.pop()
    obstacle = obstacle_que.pop()

    plot = draw_map(vehicle, obstacle, plot, map_info, trans_scale)
    show(plot)
