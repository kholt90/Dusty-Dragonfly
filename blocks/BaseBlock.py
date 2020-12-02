from OpenGL.GL import *
from OpenGL.arrays import vbo
from OpenGL.GL import shaders
import numpy as np
import math

_lightVector = np.asfarray([0,0,1])

"""
Vertices:
	(-1, -1, -1),	# left-far-bottom
	(1, -1, -1),	# right-far-bottom
	(1, 1, -1),		# right-close-bottom
	(-1, 1, -1),	# left-close-bottom
			
	(-1, -1, 1),	# left-far-top
	(1, -1, 1),		# right-far-top
	(1, 1, 1),		# right-close-top
	(-1, 1, 1),		# left-close-top

Normals:
	(0,0,-1),	# center -> bottom
	(-1,0,0),	# center -> left
	(0,-1,0),	# center -> far
	(1,0,0),	# center -> right
	(0,1,0),	# center -> close
	(0,0,1)		# center -> top

self.verts component: (Vert-x, Vert-y, Vert-z, R-color, G-color, B-color, Norm-x, Norm-y, Norm-z, Texture-U, Texture-V)
"""

class BaseBlock:
	def __init__(self,scale=1,color=[0,0,0],offset=[0,0,0], inherited=False):
		self.VERTEX_SHADER = shaders.compileShader(
			"""
			#version 130
			uniform mat4 invT;
			attribute vec3 position;
			attribute vec3 color;
			attribute vec3 vertex_normal;
			out vec4 vertex_color;

			void main()
			{
				vec4 norm = invT * vec4(vertex_normal,1.0);
				gl_Position = gl_ModelViewProjectionMatrix * vec4(position, 1.0);
				vertex_color = vec4(color * min(1, max(0, norm[2])), 1.0);
			}""", GL_VERTEX_SHADER)

		self.FRAGMENT_SHADER = shaders.compileShader(
			"""
			#version 130
			in vec4 vertex_color;
			out vec4 fragColor;
			void main() {
				fragColor = vertex_color;
			}""", GL_FRAGMENT_SHADER)

		self.shader = shaders.compileProgram(self.VERTEX_SHADER, self.FRAGMENT_SHADER)
		self.uniformInvT = glGetUniformLocation(self.shader, "invT")
		self.shader_index_position = glGetAttribLocation(self.shader, "position")
		self.shader_index_color = glGetAttribLocation(self.shader, "color")
		self.shader_index_vertex_normal = glGetAttribLocation(self.shader, "vertex_normal")

		if not inherited: # Different blocks have different shapes. Hence, self.orig_verts from below must not be run when inherited.
			#color = np.asfarray([1,0.843,0])

			self.orig_verts = np.float32([(1, -1, -1, color[0], color[1], color[2], 0, 0, -1, 0, 0),
									  (1, 1, -1, color[0], color[1], color[2], 0, 0, -1, 1, 0),
									  (-1, 1, -1, color[0], color[1], color[2], 0, 0, -1, 1, 1),
									  (-1, -1, -1, color[0], color[1], color[2], 0, 0, -1, 0, 1),

									  (-1, -1, -1, color[0], color[1], color[2], -1, 0, 0, 0, 0),
									  (-1, 1, -1, color[0], color[1], color[2], -1, 0, 0, 1, 0),
									  (-1, 1, 1, color[0], color[1], color[2], -1, 0, 0, 1, 1),
									  (-1, -1, 1, color[0], color[1], color[2], -1, 0, 0, 0, 1),

									  (-1, -1, 1, color[0], color[1], color[2], 0, 0, 1, 0, 0),
									  (-1, 1, 1, color[0], color[1], color[2], 0, 0, 1, 1, 0),
									  (1, 1, 1, color[0], color[1], color[2], 0, 0, 1, 1, 1),
									  (1, -1, 1, color[0], color[1], color[2], 0, 0, 1, 0, 1),
                                  
									  (1, -1, 1, color[0], color[1], color[2], 1, 0, 0, 0, 0),
									  (1, 1, 1, color[0], color[1], color[2], 1, 0, 0, 1, 0),
									  (1, 1, -1, color[0], color[1], color[2], 1, 0, 0, 1, 1),
									  (1, -1, -1, color[0], color[1], color[2], 1, 0, 0, 0, 1),
                                  
									  (1, 1, -1, color[0], color[1], color[2], 0, 1, 0, 0, 0),
									  (1, 1, 1, color[0], color[1], color[2], 0, 1, 0, 1, 0),
									  (-1, 1, 1, color[0], color[1], color[2], 0, 1, 0, 1, 1),
									  (-1, 1, -1, color[0], color[1], color[2], 0, 1, 0, 0, 1),
                                  
									  (1, -1, 1, color[0], color[1], color[2], 0, -1, 0, 0, 0),
									  (1, -1, -1, color[0], color[1], color[2], 0, -1, 0, 1, 0),
									  (-1, -1, -1, color[0], color[1], color[2], 0, -1, 0, 1, 1),
									  (-1, -1, 1, color[0], color[1], color[2], 0, -1, 0, 0, 1)
									  ])
		self.verts = self.orig_verts # Always keep an original copy of the object...

		self.scale = scale
		self.color = color
		self.offset = offset
		self.RefreshObj() # This is the only way to change the scale, so this must run in __init__
		
		self.ang = 0
		self.axis = (3,1,1)
		

		self.colors = None

	# Used if you changed self.scale or self.color.
	def RefreshObj(self):
		for i in range(len(self.orig_verts)):
			old = list(self.orig_verts[i])
			old[0:3] = [k * self.scale + self.offset[j] for j,k in enumerate(old[0:3])]
			old[3:6] = self.color
			self.verts[i] = old
		self.vbo = vbo.VBO(self.verts)

	def Update(self, deltaTime):
		self.ang += 50.0 * deltaTime

	def DrawBlock(self):
		shaders.glUseProgram(self.shader)
		invT = np.linalg.inv(glGetDouble(GL_MODELVIEW_MATRIX)).transpose()
		glUniformMatrix4fv(self.uniformInvT, 1, False, invT)
		try:
			self.vbo.bind()
			try:
				glEnableVertexAttribArray(self.shader_index_position)
				glEnableVertexAttribArray(self.shader_index_color)
				glEnableVertexAttribArray(self.shader_index_vertex_normal)
				stride = 44 # no. of bytes in 1 line of float32 in self.verts, that makes 32/8 * 11 = 44.
				glVertexAttribPointer(self.shader_index_position, 3, GL_FLOAT, False, stride, self.vbo)
				glVertexAttribPointer(self.shader_index_color, 3, GL_FLOAT, False, stride, self.vbo + 12) # 12 = 32/8 * 3
				glVertexAttribPointer(self.shader_index_vertex_normal, 3, GL_FLOAT, False, stride, self.vbo + 24)
				glDrawArrays(GL_QUADS, 0, 24)
			finally:
				self.vbo.unbind()
				glDisableVertexAttribArray(self.shader_index_position)
				glDisableVertexAttribArray(self.shader_index_color)
				glDisableVertexAttribArray(self.shader_index_vertex_normal)
		finally:
			shaders.glUseProgram(0)

	def Render(self):
		m = glGetDouble(GL_MODELVIEW_MATRIX)
		glRotatef(self.ang, *self.axis)
		self.DrawBlock()
		glLoadMatrixf(m)
		
		