from bokeh.models import ColumnDataSource, ImageURL
from bokeh.palettes import Dark2_5 as palette
from bokeh.plotting import figure, output_file, show

from scheme.mqtt import DrawMapInfo

import numpy as np
import itertools


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


def draw_map(draw_map_info: DrawMapInfo,
             vehicle: np.array,
             obstacle: np.array) -> figure:
    plot = draw_map_info.plot
    map_info = draw_map_info.map_info
    trans_scale = draw_map_info.trans_scale

    # draw image
    map_img = ImageURL(
        url="url", x="origin_x", y="origin_y", w="W", h="H", anchor="bottom_left"
    )
    plot.add_glyph(map_info, map_img)

    # draw vehicle
    plot.circle(vehicle[0] + trans_scale.trans_factor_x,
                vehicle[1] + trans_scale.trans_factor_y,
                legend_label='vehicle',
                line_color="green",
                fill_color="green", size=5)

    # draw obstacle
    num, _, _ = np.shape(obstacle)
    colors = itertools.cycle(palette)

    trans_x = np.array([trans_scale.trans_factor_x] * 4)
    trans_y = np.array([trans_scale.trans_factor_y] * 4)
    for n, color in zip(range(num), colors):
        xs = obstacle[n, :, 0] * \
            trans_scale.scale_factor + trans_x
        ys = obstacle[n, :, 1] * \
            trans_scale.scale_factor + trans_y
        plot.multi_polygons(
            xs=[[[xs]]],
            ys=[[[ys]]],
            legend_label="obstacle",
            line_color="blue",
            fill_color="blue",
        )

    return plot


def show_map(draw_map_info: DrawMapInfo) -> None:
    output_file(filename=draw_map_info.out_dir, title="static HTML file")

    vehicle = draw_map_info.vehicle_que.pop()
    obstacle = draw_map_info.obstacle_que.pop()

    plot = draw_map(draw_map_info, vehicle, obstacle)
    show(plot)
