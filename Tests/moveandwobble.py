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

def dragObject(obj, cam):
	pos = cam.posFromPygame(cam.getMousePos())
	obj.apply_impulse((pos - obj.center) / constants.FPS)

def setPosToInterp(towards, original, cam, frame, numframes):
	cam.pos = original.interpolate(towards, (frame+1.0)/numframes, "cosine")

def handleGlide(event, cam):
	if event.key == pygame.K_c and cam.pos and not cam.cinematic:
		original = cam.pos
		cam.enableCinematic()
		cam.runEveryFrame(setPosToInterp, (Vector2D(0,0),original,cam,"frame","numframes"), 60, cam.disableCinematic)

cam = display.Camera()
a = geometry.Rectangle(Vector2D(0,0), 1, 1, 0)
b = geometry.Circle(Vector2D(1,0), .5)

cam.addHandles({pygame.KEYDOWN:         ("E", handleGlide),
				"KEY":                  ("I", cam.translateRelative),
				pygame.MOUSEBUTTONDOWN: ("E", buttonSwitch),
				"MOUSE":                ("E", dragObject),
				})
cam.addKeyValues({pygame.K_LEFT: (-10,  0),
				  pygame.K_RIGHT:( 10,  0),
				  pygame.K_UP:   (  0, 10),
				  pygame.K_DOWN: (  0,-10),
				  })
cam.addMouseValue(0, a)
cam.addMouseValue(2, b)

while 1:
	cam.update([a, b])
	a.update_physics()
	b.update_physics()