import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from blocks.BaseBlock import BaseBlock
from blocks.IBlock import IBlock


pygame.init()
size = width, height = 640, 480
screen = pygame.display.set_mode(size, DOUBLEBUF|OPENGL)

glMatrixMode(GL_PROJECTION)
gluPerspective(45, (width/height), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)

glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)

glTranslate(0.0,0.0,-5)
cube = BaseBlock(scale = 0.1)
cube_i = IBlock(scale = 0.2,color=[1,0,0])

cubes = [cube_i]

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
	for i in cubes:
		i.Render()
	pygame.display.flip()

clock = pygame.time.Clock()
_gTickLastFrame = pygame.time.get_ticks()
_gDeltaTime = 0.0
while Update(_gDeltaTime):
	Render()
	t = pygame.time.get_ticks()
	_gDeltaTime = (t - _gTickLastFrame) / 1000.0
	_gTickLastFrame = t
