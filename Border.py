
from OpenGL.GL import *
import numpy as np
import math

_vertices = np.asfarray( 
            ((4, -6, -4),
             (4, 6, -4),
             (-4, 6, -4),
             (-4, -6, -4),
             (4, -6, 4),
             (4, 6, 4),
             (-4, -6, 4),
             (-4, 6, 4)) )

_lines = ((0, 1, 2, 3, 0, 4, 5, 7, 6, 4),
          (5, 1),
          (6, 3),
          (7, 2))

_vertices *= 0.8 # scale down a bit


def Render():
    global _vertices
    global _lines

    m = glGetDouble(GL_MODELVIEW_MATRIX)  # save matrix
    glTranslate(0.0,-1.5,0.0) # move border a bit down

    for line in _lines:
        glBegin(GL_LINES)
        for i in range(len(line)-1):
            glColor3fv((1,1,1))
            glVertex3fv(_vertices[line[i]])
            glVertex3fv(_vertices[line[i + 1]])
        glEnd()

    glLoadMatrixf(m)  # restore matrix
