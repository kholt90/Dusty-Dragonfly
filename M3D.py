import numpy as np
import pygame
import Common as CC
import Gameplay as GG
import Border

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from blocks.BaseBlock import BaseBlock

from UI.UIText import UIText

pygame.init()
size = width, height = 720, 1280
screen = pygame.display.set_mode(size, DOUBLEBUF|OPENGL)

# Each font size requires one call on LoadFonts. It also has to come before UIText().
# For now, only font size 64px is needed. We can always scale it.
UIText.LoadFonts(64)
UIText.LoadShaders()

_zCenter = 20 # Basically distance away from camera. The z-axis origin lies here.

# Available modes: 'ortho' and 'perspective'
def SwitchMode(m = 'ortho'):
	global width
	global height

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity() # This is needed to reset the display mode (ortho or perspective), otherwise the render will stop after 1 tick.
	if m == 'ortho':
		gluOrtho2D(0,width,height,0)
	elif m == 'perspective':
		# It's just manually set value such that all shapes render but minimilized the plane distance.
		gluPerspective(45, (width/height), _zCenter - 5, _zCenter * 3)
	glMatrixMode(GL_MODELVIEW)
	if m == 'ortho':
		glDisable(GL_DEPTH_TEST)
	elif m == 'perspective':
		glEnable(GL_DEPTH_TEST)

SwitchMode('perspective')
glDepthFunc(GL_LESS)
glTranslate(0.0,0.0,-_zCenter)
# glRotatef(-15, 0, 1, 0)
# glRotatef(30, 1, 0, 0)

# Note that 0,0 is the center of the world, NOT top-left
# Also note that +ve y-pos means going UP. Like how you usually draw a graph!
cube = BaseBlock(scale = .5,color=[1,0.843,0]) # This works fine but...

#hw = UIText(text="Hello World", color=[1,1,0], pos=[0, 240], anchor=[0.5,1.0], scale=0.2)
#ys = UIText(text="Yu sugg*@...", color=[1,0,0], pos=[0, 0], anchor=[0,0], scale=0.2)
next_txt = UIText(text="Next Block", color=[0,1,0], pos=[0, 480], anchor=[0.5,1.0], scale=0.1)
pause_txt = UIText(text="Pause", color=[1,0,0], pos=[0, 0], anchor=[0.5,0.5], scale=0.6)
cubes = [cube]
texts = [next_txt,pause_txt]

def Update(deltaTime):
	global cubes

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			return False

		if GG.ProcessEvent(event):
			continue

	for i in cubes:
		i.Update(deltaTime)

	CC.next_shape_disp.Update(deltaTime)
	if CC.Paused:
		texts[0].visible = False
		texts[1].visible = True
	else:
		texts[0].visible = True
		texts[1].visible = False
	GG.Update(deltaTime)
	
	return True

def Render():
	global cubes
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	glClearColor(0.1,0.1,1,1)

	Border.Render()

	if not CC.Paused:
		for i in cubes:
			i.Render()

		if CC.next_shape_disp != None:
			CC.next_shape_disp.color = CC.next_shape.color
			CC.next_shape_disp.vertices = CC.next_shape.vertices * CC.next_shape_disp.scale
			CC.next_shape_disp.surfaces = CC.next_shape.surfaces
			CC.next_shape_disp.normals = CC.next_shape.normals
			CC.next_shape_disp.Render()
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
