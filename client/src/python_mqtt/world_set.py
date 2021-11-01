from typing import List


class WorldSet:
    def __init__(self) -> None:
        self._host: str
        self._port: int
        self._x_0: float
        self._y_0: float
        self._longitude: float
        self._latitude: float
        self._topic: List[str]

    def get_host(self) -> str:
        return self._host

    def set_host(self, host: str) -> None:
        self._host = host

    def get_port(self) -> int:
        return self._port

    def set_port(self, port: int) -> None:
        self._port = port

    def get_x_0(self) -> float:
        return self._x_0

    def set_x_0(self, x_0: float) -> None:
        self._x_0 = x_0

    def get_y_0(self) -> float:
        return self._y_0

    def set_y_0(self, y_0: float) -> None:
        self._y_0 = y_0

    def get_longitude(self) -> float:
        return self._longitude

    def set_longitude(self, longitude: float) -> None:
        self._longitude = longitude

    def get_latitude(self) -> float:
        return self._latitude

    def set_latitude(self, latitude: float) -> None:
        self._latitude = latitude

    def get_topic(self) -> List[str]:
        return self._topic

    def set_topic(self, topic: List[str]) -> None:
        self._topic = topic
