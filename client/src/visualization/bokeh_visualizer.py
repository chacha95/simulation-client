"""
bokeh visualizer
"""
from typing import Union, List
import numpy as np

from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, ImageURL, Label

from scheme.mqtt import DrawMapInfo


def init_map_info(img_dir: str, h: int, w: int) -> ColumnDataSource:
    return ColumnDataSource(
        dict(
            H=[h],
            W=[w],
            origin_x=[-1 * w // 2],
            origin_y=[-1 * h // 2],
            url=[img_dir],
        )
    )


def draw_map(
    draw_map_info: DrawMapInfo,
    vehicle: np.ndarray,
    obstacle: tuple,
) -> figure:

    plot = draw_map_info.plot
    map_info = draw_map_info.map_info
    trans_scale = draw_map_info.trans_scale

    # draw image
    map_img = ImageURL(
        url="url", x="origin_x", y="origin_y", w="W", h="H", anchor="bottom_left"
    )
    plot.add_glyph(map_info, map_img)

    # translation with rotation
    v_trans = np.array(
        [trans_scale.trans_factor_x, trans_scale.trans_factor_y],
        dtype=np.float64,
    )
    v = np.matmul(trans_scale.rot_mat, vehicle.T) * trans_scale.scale_factor + v_trans
    # draw vehicle
    plot.circle(
        v[0],
        v[1],
        legend_label="vehicle",
        line_color="green",
        fill_color="green",
        size=5,
    )

    # obstacle translation, rotation
    o_trans = np.array(
        [[trans_scale.trans_factor_x] * 4, [trans_scale.trans_factor_y] * 4]
    )

    # tuple(list, np.ndarray)
    obstacle_ids = obstacle[0]
    obstacle_pps = obstacle[1]
    # draw obstacle
    num, _, _ = np.shape(obstacle_pps)
    for n in range(num):
        id = obstacle_ids[n]
        points = (
            np.matmul(trans_scale.rot_mat, obstacle_pps[n, :, :].T)
            * trans_scale.scale_factor
            + o_trans
        )
        xs = points[0, :]
        ys = points[1, :]

        # draw id text
        id_tag = Label(x=xs[0], y=ys[1], text=str(id), text_color="orange")
        plot.add_layout(id_tag)

        # draw polygon
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
