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

cam = display.Camera()
cam.addHandles({"KEY":                  ("I", cam.translateRelative),
				pygame.MOUSEBUTTONDOWN: ("E", buttonSwitch)})
cam.addKeyValues({pygame.K_LEFT: (-10,  0),
				  pygame.K_RIGHT:( 10,  0),
				  pygame.K_UP:   (  0, 10),
				  pygame.K_DOWN: (  0,-10),
				  })
a = geometry.Rectangle(Vector2D(0,0), 1, 1, 0)
while 1:
	cam.update([a])