from OpenGL.GL import *
import numpy as np
import math

_lightVector = np.asfarray([0,0,1])


class BaseBlock:
	def __init__(self,scale=1,color=[0,0,0]):
		self.verts = np.asfarray([(1, -1, -1),
								(1, 1, -1),
								(-1, 1, -1),
								(-1, -1, -1),
								(1, -1, 1),
								(1, 1, 1),
								(-1, -1, 1),
								(-1, 1, 1)])

		self.surfaces = np.array([(0,1,2,3),
								(3,2,7,6),
								(6,7,5,4),
								(4,5,1,0),
								(1,5,7,2),
								(4,0,3,6)])

		self.normals = np.asfarray([(0,0,-1),
								  (-1,0,0),
								  (0,0,1),
								  (1,0,0),
								  (0,1,0),
								  (0,-1,0)])

		self.color = np.asfarray(color)
		self.ang = 0
		self.axis = (3,1,1)
		self.scale = scale

		self.colors = None

	def Update(self, deltaTime):
		self.ang += 50.0 * deltaTime

	def DrawBlock(self):
		global _lightVector

		invT = np.linalg.inv(glGetDouble(GL_MODELVIEW_MATRIX)).transpose()
		glBegin(GL_QUADS)
		for n, surface in enumerate(self.surfaces):
			col = self.color if self.colors is None else self.colors[n]

			for i, vert in enumerate(surface):
				norm = np.append(self.normals[n], 1)
				modelNorm = np.matmul(norm, invT)
				modelNorm = np.delete(modelNorm, 3)
				np.linalg.norm(modelNorm)

				dotP = np.dot(_lightVector, modelNorm)
				mult = max(min(dotP, 1), 0)
				glColor3fv(col * mult)
				glVertex3fv(self.verts[vert] * self.scale)
		glEnd()
		

	def Render(self):
		m = glGetDouble(GL_MODELVIEW_MATRIX)
		glRotatef(self.ang, *self.axis)
		self.DrawBlock()
		glLoadMatrixf(m)
		