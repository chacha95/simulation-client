from typing import List, Optional
from pydantic import BaseModel
from collections import deque

from bokeh.models import ColumnDataSource
from bokeh.plotting import figure

from translation_scale import TransScale
from world_set import WorldSet

import sys


class CustomQueue:
    def __init__(self, size: int) -> None:
        self.size: int = size
        self.que: deque = deque()

    def __len__(self) -> int:
        return len(self.que)

    def push(self, data: dict) -> None:
        if len(self.que) == self.size:
            self.que.popleft()
        self.que.append(data)

    def pop(self):
        if len(self.que) == 0:
            print("[queue empty error]")
            sys.exit()
        return self.que.popleft()


class LGSVLMqttInfo(BaseModel):
    topic: List[str]
    address: str = "localhost"
    port: int = 1883
    world_set: WorldSet = None
    plot: figure = None
    map_info: ColumnDataSource(dict()) = None
    out_dir: str = None
    img_dir: str = None
    trans_scale: TransScale = None
    history: int = 10


class DrawMapInfo(BaseModel):
    vehicle_que: CustomQueue
    obstacle_que: CustomQueue
    plot: figure
    map_info: ColumnDataSource(dict())
    trans_scale: TransScale
    out_dir: str
    img_dir: str
