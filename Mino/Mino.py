
import math
import numpy as np
from OpenGL.GL import *

_lightVector = np.asfarray([0, 0, 1])


class Mino:
    def __init__(self):
        self.color = np.asfarray([0, 0, 1])

        self.vertices = np.asfarray([(-1, 1, 1),
                                     (1, 1, 1),
                                     (-1, -1, 1),
                                     (1, -1, 1),
                                     (-1, 1, -1),
                                     (1, 1, -1),
                                     (-1, -1, -1),
                                     (1, -1, -1)])

        self.surfaces = np.array([(0, 1, 3, 2),
                                  (4, 5, 7, 6),
                                  (4, 0, 2, 6),
                                  (1, 5, 7, 3),
                                  (4, 5, 1, 0),
                                  (2, 3, 7, 6)])

        self.normals = np.asfarray([(0, 0, 1),
                                    (0, 0, -1),
                                    (-1, 0, 0),
                                    (1, 0, 0),
                                    (0, 1, 0),
                                    (0, -1, 0)])

        self.ang = 0
        self.x_axis = 0
        self.y_axis = 1
        self.z_axis = .1
        self.x_pos = 0
        self.y_pos = 0

        self.scale = 1 # You don't have to use it. But I do. > 1+1=2

    def Update(self, deltaTime):
        self.ang += 50.0 * deltaTime

    def DrawBlock(self, invT):
        global _lightVector

        glBegin(GL_QUADS)
        for n, surface in enumerate(self.surfaces):
            for vertex in surface:
                norm = np.append(self.normals[n], 1)
                modelNorm = np.matmul(norm, invT)
                modelNorm = np.delete(modelNorm, 3)
                length = math.sqrt(np.sum(modelNorm * modelNorm))
                modelNorm /= length

                dot = np.sum(_lightVector * modelNorm)
                mult = max(min(dot, 1), 0)

                glColor3fv(self.color * mult)
                glVertex3fv(self.vertices[vertex])
        glEnd()

    def Render(self):
        m = glGetDouble(GL_MODELVIEW_MATRIX)  # save matrix
        glTranslatef(self.x_pos, self.y_pos, -30)
        glRotatef(self.ang, self.x_axis, self.y_axis, self.z_axis)
        view = glGetDouble(GL_MODELVIEW_MATRIX)
        invT = np.linalg.inv(view).transpose()
        self.DrawBlock(invT)
        glLoadMatrixf(m)  # restore matrix
