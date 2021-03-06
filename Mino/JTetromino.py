
import numpy as np
from Mino.Mino import Mino
from Common import scale

class JTetromino(Mino):
    def __init__(self):
        super().__init__()
        self.color = np.asfarray([0, 0, 1])

        self.vertices = np.asfarray([(0, 3, 1),
                                     (2, 3, 1),
                                     (-2, -1, 1),
                                     (0, -1, 1),
                                     (-2, -3, 1),
                                     (0, -3, 1),
                                     (2, -3, 1),
                                     (0, 3, -1),
                                     (2, 3, -1),
                                     (-2, -1, -1),
                                     (0, -1, -1),
                                     (-2, -3, -1),
                                     (0, -3, -1),
                                     (2, -3, -1)])

        self.surfaces = np.array([(0, 1, 6, 5),  # Front
                                  (2, 3, 5, 4),  # Front
                                  (7, 8, 13, 12),  # Back
                                  (9, 10, 12, 11),  # Back
                                  (7, 0, 3, 10),  # Left
                                  (9, 2, 4, 11),  # Left
                                  (1, 8, 13, 6),  # Right
                                  (7, 8, 1, 0),  # Top
                                  (9, 10, 3, 2),  # Top
                                  (4, 5, 12, 11),  # Bottom
                                  (5, 6, 13, 12)])  # Bottom

        self.normals = np.asfarray([(0, 0, 1),  # Front
                                    (0, 0, 1),  # Front
                                    (0, 0, -1),  # Back
                                    (0, 0, -1),  # Back
                                    (-1, 0, 0),  # Left
                                    (-1, 0, 0),  # Left
                                    (1, 0, 0),  # Right
                                    (0, 1, 0),  # Top
                                    (0, 1, 0),  # Top
                                    (0, -1, 0),  # Bottom
                                    (0, -1, 0)])  # Bottom

        self.vertices *= scale
