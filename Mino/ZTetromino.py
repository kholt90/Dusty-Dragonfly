
import numpy as np
from Mino.Mino import Mino


class ZTetromino(Mino):
    def __init__(self):
        super().__init__()
        self.color = np.asfarray([1, 0, 0])

        self.vertices = np.asfarray([(-3, 2, 1),
                                     (1, 2, 1),
                                     (-3, 0, 1),
                                     (-1, 0, 1),
                                     (1, 0, 1),
                                     (3, 0, 1),
                                     (-1, -2, 1),
                                     (3, -2, 1),
                                     (-3, 2, -1),
                                     (1, 2, -1),
                                     (-3, 0, -1),
                                     (-1, 0, -1),
                                     (1, 0, -1),
                                     (3, 0, -1),
                                     (-1, -2, -1),
                                     (3, -2, -1)])

        self.surfaces = np.array([(0, 1, 4, 2),  # Front
                                  (3, 5, 7, 6),  # Front
                                  (8, 9, 12, 10),  # Back
                                  (11, 13, 15, 14),  # Back
                                  (8, 0, 2, 10),  # Left
                                  (11, 3, 6, 14),  # Left
                                  (1, 9, 12, 4),  # Right
                                  (5, 13, 15, 7),  # Right
                                  (8, 9, 1, 0),  # Top
                                  (12, 13, 5, 4),  # Top
                                  (2, 3, 11, 10),  # Bottom
                                  (6, 7, 15, 14)])  # Bottom

        self.normals = np.asfarray([(0, 0, 1),  # Front
                                    (0, 0, 1),  # Front
                                    (0, 0, -1),  # Back
                                    (0, 0, -1),  # Back
                                    (-1, 0, 0),  # Left
                                    (-1, 0, 0),  # Left
                                    (1, 0, 0),  # Right
                                    (1, 0, 0),  # Right
                                    (0, 1, 0),  # Top
                                    (0, 1, 0),  # Top
                                    (0, -1, 0),  # Bottom
                                    (0, -1, 0)])  # Bottom

        self.x_pos = 7
        self.y_pos = -3
