import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from SlowCube import SlowCube


pygame.init()
size = width, height = 640, 480
screen = pygame.display.set_mode(size, DOUBLEBUF|OPENGL)

glMatrixMode(GL_PROJECTION)
gluPerspective(45, (width/height), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)

glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)

glTranslate(0.0,0.0,-5)
cube = SlowCube()

def Update(deltaTime):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			return False
	cube.Update(deltaTime)
	return True

def Render():
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	cube.Render()
	pygame.display.flip()

clock = pygame.time.Clock()
_gTickLastFrame = pygame.time.get_ticks()
_gDeltaTime = 0.0
while Update(_gDeltaTime):
	Render()
	t = pygame.time.get_ticks()
	_gDeltaTime = (t - _gTickLastFrame) / 1000.0
	_gTickLastFrame = t
