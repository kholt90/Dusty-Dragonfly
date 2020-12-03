import math
import numpy as np
import random
import pygame
import Common as CC

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from blocks.BaseBlock import BaseBlock

# Fun Fact: Tetris shapes are called Tetrominos
from Mino.Mino import Mino
from Mino.ITetromino import ITetromino
from Mino.OTetromino import OTetromino
from Mino.TTetromino import TTetromino
from Mino.STetromino import STetromino
from Mino.ZTetromino import ZTetromino
from Mino.LTetromino import LTetromino
from Mino.JTetromino import JTetromino

cubes = []
shapes = None
# _current = Mino(color=_tetromino[0], offsets=_tetromino[1])
_pos = np.asfarray([-1, 7, -1])
_pos *= CC.scale
_angles = [0, 0, 0]

def Init():
    global shapes
    global cubes

    I = ITetromino()
    O = OTetromino()
    T = TTetromino()
    S = STetromino()
    Z = ZTetromino()
    L = LTetromino()
    J = JTetromino()
    shapes = (I, O, T, S, Z, L, J)

    CC.current_shape = random.choice(shapes)
    CC.next_shape = random.choice(shapes)

    NextPiece = Mino()
    NextPiece.y_pos = 8
    NextPiece.x_pos = 3
    NextPiece.scale = 0.5
    CC.next_shape_disp = NextPiece

    # cubes.append(BaseBlock(scale = 1,color=[1,0.843,0]))

def ProcessEvent(event):
    global _pos
    global _angles

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            _pos[0] -= 2 * CC.scale
        elif event.key == pygame.K_RIGHT:
            _pos[0] += 2 * CC.scale
        elif event.key == pygame.K_UP:
            _pos[2] -= 2 * CC.scale
        elif event.key == pygame.K_DOWN:
            _pos[2] += 2 * CC.scale
        elif event.key == pygame.K_a:
            _angles[0] += 90
        elif event.key == pygame.K_s:
            _angles[1] += 90
        elif event.key == pygame.K_d:
            _angles[2] += 90
        elif event.key == pygame.K_ESCAPE:
            CC.Paused = False if CC.Paused else True
        else:
            return False
    return True

_tmp_pos = 0
def Update(deltaTime):
    global shapes
    global _pos
    global _tmp_pos

    _tmp_pos += 1 * deltaTime
    if _tmp_pos >= 1:
        _pos[1] -= 1 * CC.scale
        _tmp_pos = 0

    if _pos[1] <= -10 * CC.scale:
        _pos = np.asfarray([-1, 7, -1])
        _pos *= CC.scale
        CC.current_shape = CC.next_shape
        CC.next_shape = random.choice(shapes)

    CC.current_shape.Update(deltaTime)


def Render():
    global _pos
    global _angles

    m = glGetDouble(GL_MODELVIEW_MATRIX)
    glTranslate(*_pos)
    glRotatef(_angles[0], 1, 0, 0)
    glRotatef(_angles[1], 0, 1, 0)
    glRotatef(_angles[2], 0, 0, 1)
    CC.current_shape.Render()
    glLoadMatrixf(m)
