import numpy as np


def rot_mat(degree: int) -> np.ndarray:
    """
    make (2, 2) rotation matrix

    Args:
        degree: degree, e.g. 90

    Return:
        (2, 2) numpy rotation matrix
    """
    theta = np.radians(degree)
    c, s = np.cos(theta), np.sin(theta)
    R = np.array(((c, -s), (s, c)))
    return R
