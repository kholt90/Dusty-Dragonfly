from OpenGL.GL import *
from OpenGL.GLU import *
from freetype import *
from OpenGL.GL import shaders
import numpy as np
import math

class UIText:



	@classmethod
	def LoadShaders(cls):
		# Shader credits: https://stackoverflow.com/a/63837079
		cls.VERTEX_SHADER = shaders.compileShader(
		"""
		#version 330 core
        layout (location = 0) in vec4 vertex; // <vec2 pos, vec2 tex>
        out vec2 TexCoords;

        uniform mat4 projection;

        void main()
        {
            gl_Position = projection * vec4(vertex.xy, 0.0, 1.0);
            TexCoords = vertex.zw;
        }""", GL_VERTEX_SHADER)

		cls.FRAGMENT_SHADER = shaders.compileShader(
		"""
		#version 330 core
        in vec2 TexCoords;
        out vec4 color;

        uniform sampler2D text;
        uniform vec3 textColor;

        void main()
        {    
            vec4 sampled = vec4(1.0, 1.0, 1.0, texture(text, TexCoords).r);
            color = vec4(textColor, 1.0) * sampled;
        }""", GL_FRAGMENT_SHADER)

	# The dict will look something like this:
	# Atm, we'll just load ASCII char 32-127. That should cover all the commonly-used chars.
	# {'12':{'a':(<bitmap>,<texture>,<char width>), 'b':(<bitmap>,<texture>,<char width>), ...}}
	_LoadedFonts = {}
	_font = "Data/OpenSans-Regular.ttf"
	_font_size = '0'

	@classmethod
	def LoadFonts(cls,size):
		glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
		ff = Face(UIText._font)
		ff.set_pixel_sizes(size,size)
		size = str(size)
		UIText._font_size = size # One font size for now.
		UIText._LoadedFonts[size] = {}
		for i in range(32,128):
			x = chr(i)
			ff.load_char(x)
			fg = ff.glyph
			fb = ff.glyph.bitmap

			# This print served me well, so I kept it here.
			#print(x, "|W",fb.width, "|H",fb.rows, "|BL",fg.bitmap_left, "|BT",fg.bitmap_top, "|A",fg.advance.x / 64)

			t = glGenTextures(1)
			glBindTexture(GL_TEXTURE_2D, t)
			glTexImage2D(
				GL_TEXTURE_2D,
				0, GL_RED,
				fb.width,
				fb.rows,
				0, GL_RED,
				GL_UNSIGNED_BYTE,
				fb.buffer)

			# These 2 parameters are essential for the text to show
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)      
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)

			fdict = {
				"bitmap": fb,
				"w": fb.width,
				"h": fg.bitmap_top,
				"x_off": fg.bitmap_left,
				"y_off": fb.rows - fg.bitmap_top, # +ve = render lower
				"w_full": fg.advance.x / 64,
				"h_full": fb.rows
			}

			UIText._LoadedFonts[size][x] = (fdict,t)
		glBindTexture(GL_TEXTURE_2D, 0) # Basically a cleanup function...?



	def __init__(self,text="",color=[0,0,0],pos=[0,0],anchor=[0,0],scale=1):
		self.orig_verts = np.float32([
			(0,-1,0,0),
			(0,0,0,1),
			(1,0,1,1),
			(0,-1,0,0),
			(1,0,1,1),
			(1,-1,1,0)
		])
		self.verts = self.orig_verts

		self.shader = shaders.compileProgram(UIText.VERTEX_SHADER, UIText.FRAGMENT_SHADER)
		glUseProgram(self.shader)
		self.uniformInvT = glGetUniformLocation(self.shader, "projection")
		invT = np.linalg.inv(glGetDouble(GL_MODELVIEW_MATRIX)).transpose()
		glUniformMatrix4fv(self.uniformInvT, 1, False, invT)

		self.vao = glGenVertexArrays(1)
		self.vbo = glGenBuffers(1)
		glBindVertexArray(self.vao)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
		glBufferData(GL_ARRAY_BUFFER, 6 * 16, None, GL_DYNAMIC_DRAW)
		glEnableVertexAttribArray(0) # Must be enabled for the text to show
		glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, 0)
		glBindVertexArray(0)

		self.color = np.asfarray(color)
		self.scale = scale
		self.text = text
		self.visible = True

		self.pos = np.asfarray(pos) # For simplicity measures, the anchor of the text starts at the middle of the screen.
		self.aligned_pos = self.pos # This is equivalent to running CalcPos() with [0,0] anchor
		self.dim = np.asfarray([0,0]) # Can't find a way to change the font size yet
		# Few notes on this anchor since it works differently:
		# 1. Both x-anchor and y-anchor ranges from 0.0 to 1.0, and 0.5 means center.
		# 2. This anchor ONLY ALIGNS WITH THE TEXT. If you need to center the text in worls position, calculate it yourself.
		self.anchor = np.asfarray(anchor)
		self.CalcDim()

	def GetVert(self,x,y,w,h):
		temp = self.scale / 64	# 64 is hardcoded to suit the screen 
		x = (x) * temp
		y = (y - self.dim[1]) * temp
		w *= temp
		h *= temp
		return np.float32([
			(x,y+h,0,0),
			(x,y,0,1),
			(x+w,y,1,1),
			(x,y+h,0,0),
			(x+w,y,1,1),
			(x+w,y+h,1,0),
		])

	def Update(self, deltaTime):
		pass

	# For convenience
	def SetText(self,t):
		self.text = t
		self.CalcDim()

	# You technically only need to run this when you change the text
	def CalcDim(self):
		self.dim[0], self.dim[1] = 0, 0
		for i in self.text:
			self.dim[0] += UIText._LoadedFonts[UIText._font_size][i][0]["w_full"]
			h = UIText._LoadedFonts[UIText._font_size][i][0]["h"]
			if h > self.dim[1]:
				self.dim[1] = h # This one means that the tallest character decides the height.
		if self.anchor[0] != 0 or self.anchor[1] != 0:
			self.CalcPos()

	# You run this when you moved the text or changed the anchor.
	# This will also be called by CalcDim if the anchor is not [0,0], since different size means different aligned pos.
	def CalcPos(self):
		self.aligned_pos[0] = self.pos[0] - self.dim[0] * self.anchor[0]
		self.aligned_pos[1] = self.pos[1] + self.dim[1] * self.anchor[1] # Not sure why aligned_pos[1] is still equal to pos[1]
		#print(self.aligned_pos[1], self.pos[1] + self.dim[1] * self.anchor[1]) # Kept alive for now...
		
	def DrawText(self):
		if len(self.text) == 0:
			return

		shaders.glUseProgram(self.shader)
		glUniform3f(glGetUniformLocation(self.shader, "textColor"),
			self.color[0],self.color[1],self.color[2])
		glActiveTexture(GL_TEXTURE0)
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glBindVertexArray(self.vao)

		total_off = self.aligned_pos[0]
		for i in self.text:
			temp = UIText._LoadedFonts[UIText._font_size]
			t = temp[i][1]
			fdict = temp[i][0]
			verts = self.GetVert(total_off,self.aligned_pos[1] - fdict["y_off"],fdict["w"],fdict["h_full"])
			total_off += fdict["w_full"]

			glBindTexture(GL_TEXTURE_2D, t)
			glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
			glBufferSubData(GL_ARRAY_BUFFER, 0, verts.nbytes, verts)
			glBindBuffer(GL_ARRAY_BUFFER, 0)
			glDrawArrays(GL_TRIANGLES, 0, 6)
		
		glBindVertexArray(0)
		glBindTexture(GL_TEXTURE_2D, 0)
		glUseProgram(0)

	def Render(self):
		if self.visible:
			m = glGetDouble(GL_MODELVIEW_MATRIX)
			self.DrawText()
			glLoadMatrixf(m)