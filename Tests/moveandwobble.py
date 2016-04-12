import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from PyPhys import *
from PyPhys.util import Vector2D
import pygame

def buttonSwitch(event, cam):
	if event.button == 4:
		cam.scale(1.1)
	if event.button == 5:
		cam.scale(1/1.1)

def dragBox(box, cam):
	pos = cam.posFromPygame(cam.getMousePos())
	box.apply_impulse((pos - box.center) / constants.FPS)

cam = display.Camera()
a = geometry.Rectangle(Vector2D(0,0), 1, 1, 0)

cam.addHandles({"KEY":                  ("I", cam.translateRelative),
				pygame.MOUSEBUTTONDOWN: ("E", buttonSwitch),
				"MOUSE":                ("E", dragBox),
				})
cam.addKeyValues({pygame.K_LEFT: (-10,  0),
				  pygame.K_RIGHT:( 10,  0),
				  pygame.K_UP:   (  0, 10),
				  pygame.K_DOWN: (  0,-10),
				  })
cam.addMouseValue(0, a)
while 1:
	cam.update([a])
	a.update_physics()