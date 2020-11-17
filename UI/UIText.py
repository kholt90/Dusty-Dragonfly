from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from ctypes import c_ubyte
import numpy as np
import math


class UIText:
	def __init__(self,text="",color=[0,0,0],pos=[0,0],anchor=[0,0]):
		self.color = np.asfarray(color)
		self.font = GLUT_BITMAP_HELVETICA_18
		self.text = text
		self.btext = text.encode('utf-8')

		self.pos = np.asfarray(pos)
		self.aligned_pos = self.pos
		self.dim = np.asfarray([0,0]) # Can't find a way to change the font size yet
		self.anchor = np.asfarray(anchor) # Both ranges from 0.0 to 1.0, and 0.5 means center.
		self.CalcDim()

	def Update(self, deltaTime):
		pass

	# For convenience
	def SetText(t):
		self.text = t
		self.btext = t.encode('utf-8')
		self.CalcDim()


	# You technically only need to run this when you change the text
	def CalcDim(self):
		self.dim[0] = glutBitmapLength(self.font, (c_ubyte * len(self.text)).from_buffer_copy(self.btext)) # Credits: https://stackoverflow.com/a/21490290
		self.dim[1] = glutBitmapHeight(self.font)
		if self.anchor[0] != 0 or self.anchor[1] != 0:
			self.CalcPos()
	# You run this when you moved the text or changed the anchor.
	# This will also be called by CalcDim, since different size means different aligned pos.
	def CalcPos(self):
		self.aligned_pos = self.pos - self.dim * self.anchor
		self.aligned_pos[1] = 480 - self.aligned_pos[1] - self.dim[1] # 480 will become the screen height in the future

	def DrawText(self):
		if len(self.text) == 0:
			return
		glColor3fv(self.color)
		glWindowPos2f(*self.aligned_pos) # This must come after glColor3fv. Otherwise the color won't register.
		glutBitmapString(self.font, self.btext)

	def Render(self):
		glPushMatrix()
		gluOrtho2D(0,640,480,0) # Will change to screen size once a common file is made.
		self.DrawText()			
		glPopMatrix()