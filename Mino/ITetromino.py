
import numpy as np
from Mino.Mino import Mino
from Common import scale

class ITetromino(Mino):
    def __init__(self):
        super().__init__()
        self.color = np.asfarray([.68, .85, .9])

        self.vertices = np.asfarray([(-1, 4, 1),
                                     (1, 4, 1),
                                     (-1, -4, 1),
                                     (1, -4, 1),
                                     (-1, 4, -1),
                                     (1, 4, -1),
                                     (-1, -4, -1),
                                     (1, -4, -1)])

        self.surfaces = np.array([(0, 1, 3, 2),  # Front
                                  (4, 5, 7, 6),  # Back
                                  (4, 0, 2, 6),  # Left
                                  (1, 5, 7, 3),  # Right
                                  (4, 5, 1, 0),  # Top
                                  (2, 3, 7, 6)])  # Bottom

        self.normals = np.asfarray([(0, 0, 1),  # Front
                                    (0, 0, -1),  # Back
                                    (-1, 0, 0),  # Left
                                    (1, 0, 0),  # Right
                                    (0, 1, 0),  # Top
                                    (0, -1, 0)])  # Bottom

        self.vertices *= scale
