import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import Border
import Gameplay

# Fun Fact: Tetris shapes are called Tetrominos
from Mino.Mino import Mino
from Mino.ITetromino import ITetromino
from Mino.OTetromino import OTetromino
from Mino.TTetromino import TTetromino
from Mino.STetromino import STetromino
from Mino.ZTetromino import ZTetromino
from Mino.LTetromino import LTetromino
from Mino.JTetromino import JTetromino

from blocks.BaseBlock import BaseBlock
from blocks.IBlock import IBlock
from UI.UIText import UIText

pygame.init()
size = width, height = 640, 900
screen = pygame.display.set_mode(size, DOUBLEBUF|OPENGL)

# Each font size requires one call on LoadFonts. It also has to come before UIText().
# For now, only font size 64px is needed. We can always scale it.
UIText.LoadFonts(64)
UIText.LoadShaders()



# Available modes: 'ortho' and 'perspective'
def SwitchMode(m = 'ortho'):
	global width
	global height

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity() # This is needed to reset the display mode (ortho or perspective), otherwise the render will stop after 1 tick.
	if m == 'ortho':
		gluOrtho2D(0,width,height,0)
	elif m == 'perspective':
		gluPerspective(45, (width/height), 0.1, 50.0)
	glMatrixMode(GL_MODELVIEW)
	if m == 'ortho':
		glDisable(GL_DEPTH_TEST)
	elif m == 'perspective':
		glEnable(GL_DEPTH_TEST)

SwitchMode('perspective')
glDepthFunc(GL_LESS)
glTranslate(0.0,0.0,-20)
# glRotatef(-15, 0, 1, 0)
# glRotatef(30, 1, 0, 0)

# Note that 0,0 is the center of the world, NOT top-left
# Also note that +ve y-pos means going UP. Like how you usually draw a graph!
cube = BaseBlock(scale = 0.1)
cube_i = IBlock(scale = 0.2,color=[1,0.843,0])

Block = Mino()
I = ITetromino()
O = OTetromino()
T = TTetromino()
S = STetromino()
Z = ZTetromino()
L = LTetromino()
J = JTetromino()

hw = UIText(text="Hello World", color=[1,1,0], pos=[0, 240], anchor=[0.5,1.0], scale=0.2)
#ys = UIText(text="Yu sugg*@...", color=[1,0,0], pos=[0, 0], anchor=[0,0], scale=0.2)

#hw.SetText("Actually no.")

cubes = [I, O, T, S, Z, L, J]
texts = [hw]

def Update(deltaTime):
	global cubes

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			return False
	for i in cubes:
		i.Update(deltaTime)
	
	return True

def Render():
	global cubes
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

	Border.Render()

	for i in cubes:
		i.Render()
	SwitchMode('ortho')
	for i in texts:
		i.Render()
	SwitchMode('perspective')

	
	
	pygame.display.flip()

clock = pygame.time.Clock()
_gTickLastFrame = pygame.time.get_ticks()
_gDeltaTime = 0.0
while Update(_gDeltaTime):
	Render()
	t = pygame.time.get_ticks()
	_gDeltaTime = (t - _gTickLastFrame) / 1000.0
	_gTickLastFrame = t
print('(Casually pushing those useless logging down...)' + "\n"*50)
# When running self.vbo.bind, 19 lines of dict_keys appeared (at least on my side).
