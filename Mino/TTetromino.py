
import numpy as np
from Mino.Mino import Mino


class TTetromino(Mino):
    def __init__(self):
        super().__init__()
        self.color = np.asfarray([.5, 0, .5])

        self.vertices = np.asfarray([(-3, 2, 1),
                                     (3, 2, 1),
                                     (-3, 0, 1),
                                     (-1, 0, 1),
                                     (1, 0, 1),
                                     (3, 0, 1),
                                     (-1, -2, 1),
                                     (1, -2, 1),
                                     (-3, 2, -1),
                                     (3, 2, -1),
                                     (-3, -0, -1),
                                     (-1, 0, -1),
                                     (1, 0, -1),
                                     (3, -0, -1),
                                     (-1, -2, -1),
                                     (1, -2, -1)])

        self.surfaces = np.array([(0, 1, 5, 2),  # Front
                                  (3, 4, 7, 6),  # Front
                                  (8, 9, 13, 10),  # Back
                                  (11, 12, 15, 14),  # Back
                                  (8, 0, 2, 10),  # Left
                                  (11, 3, 6, 14),  # Left
                                  (1, 9, 13, 5),  # Right
                                  (4, 12, 15, 7),  # Right
                                  (8, 9, 1, 0),  # Top
                                  (2, 3, 11, 10),  # Bottom
                                  (6, 7, 15, 14),  # Bottom
                                  (4, 5, 13, 12)])  # Bottom

        self.normals = np.asfarray([(0, 0, 1),  # Front
                                    (0, 0, 1),  # Front
                                    (0, 0, -1),  # Back
                                    (0, 0, -1),  # Back
                                    (-1, 0, 0),  # Left
                                    (-1, 0, 0),  # Left
                                    (1, 0, 0),  # Right
                                    (1, 0, 0),  # Right
                                    (0, 1, 0),  # Top
                                    (0, -1, 0),  # Bottom
                                    (0, -1, 0),  # Bottom
                                    (0, -1, 0)])  # Bottom

        self.x_pos = 0
