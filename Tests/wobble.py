import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from PyPhys import *
from PyPhys.util import Vector2D

def dragBox(box, cam):
	pos = cam.posFromPygame(cam.getMousePos())
	box.apply_impulse((pos - box.center) / constants.FPS)

cam = display.Camera()
a = geometry.Rectangle(Vector2D(0,0), 1, 1, 0)

cam.addHandle("MOUSE", ("E", dragBox))
cam.addMouseValue(0, a)
while 1:
	cam.update([a])
	a.update_physics()