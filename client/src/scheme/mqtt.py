from typing import List, Optional, Any, Union
from pydantic import BaseModel
from collections import deque

from bokeh.models import ColumnDataSource

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


class WorldSet(BaseModel):
    x_0: float
    y_0: float
    longitude: Optional[float] = None
    latitude: Optional[float] = None


class TransScale(BaseModel):
    map_margin: int = None
    trans_factor_x: int = None
    trans_factor_y: int = None
    scale_factor: int = None


class LGSVLMqttInfo(BaseModel):
    topic: List[tuple] = None
    address: str = "localhost"
    port: int = 1883
    plot: Any = None
    out_dir: str = None
    img_dir: str = None
    history: Optional[int] = 10
    map_info: ColumnDataSource = None
    world_set: Optional[WorldSet] = None
    trans_scale: Optional[TransScale] = None

    class Config:
        arbitrary_types_allowed = True


class DrawMapInfo(BaseModel):
    plot: Any = None
    out_dir: str = None
    img_dir: str = None
    trans_scale: Optional[TransScale] = None
    vehicle_que: CustomQueue = None
    obstacle_que: CustomQueue = None
    map_info: Any = None

    class Config:
        arbitrary_types_allowed = True
