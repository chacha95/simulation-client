class Obstacle:
    """
    frames: {0: (n, 4, 2),
             1: (m, 4, 2), }
    """

    frames: dict = {}
    idx: int = 0

    @classmethod
    def add_frame(cls, obstacles):
        cls.frames[cls.idx] = obstacles
        cls.idx += 1


class Vehicle:
    """
    frames: {0: (2,),
             1: (2,)}
    """

    frames: dict = {}
    idx: int = 0

    @classmethod
    def add_frame(cls, v_pos):
        cls.frames[cls.idx] = v_pos
        cls.idx += 1
