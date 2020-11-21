
import numpy as np
from Mino.Mino import Mino


class LTetromino(Mino):
    def __init__(self):
        super().__init__()
        self.color = np.asfarray([1, .65, 0])

        self.vertices = np.asfarray([(-2, 3, 1),
                                     (0, 3, 1),
                                     (0, -1, 1),
                                     (2, -1, 1),
                                     (-2, -3, 1),
                                     (0, -3, 1),
                                     (2, -3, 1),
                                     (-2, 3, -1),
                                     (0, 3, -1),
                                     (0, -1, -1),
                                     (2, -1, -1),
                                     (-2, -3, -1),
                                     (0, -3, -1),
                                     (2, -3, -1)])

        self.surfaces = np.array([(0, 1, 5, 4),  # Front
                                  (2, 3, 6, 5),  # Front
                                  (7, 8, 12, 11),  # Back
                                  (9, 10, 13, 12),  # Back
                                  (7, 0, 4, 11),  # Left
                                  (1, 8, 9, 2),  # Right
                                  (3, 10, 13, 6),  # Right
                                  (7, 8, 1, 0),  # Top
                                  (9, 10, 3, 2),  # Top
                                  (4, 5, 12, 11),  # Bottom
                                  (5, 6, 13, 12)])  # Bottom

        self.normals = np.asfarray([(0, 0, 1),  # Front
                                    (0, 0, 1),  # Front
                                    (0, 0, -1),  # Back
                                    (0, 0, -1),  # Back
                                    (-1, 0, 0),  # Left
                                    (1, 0, 0),  # Right
                                    (1, 0, 0),  # Right
                                    (0, 1, 0),  # Top
                                    (0, 1, 0),  # Top
                                    (0, -1, 0),  # Bottom
                                    (0, -1, 0)])  # Bottom

        self.x_pos = 14
        self.y_pos = 4
