from typing import List


class WorldSet:
    _host: str
    _port: int
    _x_0: float
    _y_0: float
    _longitude: float
    _latitude: float
    _topic: List[str]

    @classmethod
    def get_host(cls):
        return cls._host

    @classmethod
    def set_host(cls, host: str):
        cls._host = host

    @classmethod
    def get_port(cls):
        return cls._port

    @classmethod
    def set_port(cls, port: int):
        cls._port = port

    @classmethod
    def get_x_0(cls):
        return cls._x_0

    @classmethod
    def set_x_0(cls, x_0: float):
        cls._x_0 = x_0

    @classmethod
    def get_y_0(cls):
        return cls._y_0

    @classmethod
    def set_y_0(cls, y_0: float):
        cls._y_0 = y_0

    @classmethod
    def get_longitude(cls):
        return cls._longitude

    @classmethod
    def set_longitude(cls, longitude: float):
        cls._longitude = longitude

    @classmethod
    def get_latitude(cls):
        return cls._latitude

    @classmethod
    def set_latitude(cls, latitude: float):
        cls._latitude = latitude

    @classmethod
    def get_topic(cls):
        return cls._topic

    @classmethod
    def set_topic(cls, topic: List[str]):
        cls._topic = topic
